from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Movie, WatchedMovie, LikedMovie
from .serializers import MovieSerializer, WatchedMovieSerializer, LikedMovieSerializer
import requests
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.cloud import speech, language_v2
import os
from google.cloud import speech_v1
from google.cloud import language_v1
import json


TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# 인기순 영화 40개 조회
@api_view(['GET'])
def get_popular_movies(request):
    movies = Movie.objects.all().order_by('-popularity')[:40]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# 시청중인 영화 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def watched_movies(request):
    watched = WatchedMovie.objects.filter(user=request.user).order_by('-watched_at')
    serializer = WatchedMovieSerializer(watched, many=True)
    return Response(serializer.data)


# 찜한 영화 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_movies(request):
    liked = LikedMovie.objects.filter(user=request.user).order_by('-liked_at')
    serializer = LikedMovieSerializer(liked, many=True)
    return Response(serializer.data)


# 시청중인 영화 목록에서 제거
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_watch(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    watched = WatchedMovie.objects.filter(user=request.user, movie=movie)
    
    if watched.exists():
        watched.delete()
        return Response({'message': '시청 목록에서 제거됨'})
    else:
        WatchedMovie.objects.create(user=request.user, movie=movie)
        return Response({'message': '시청 목록에 추가됨'})


# 영화 찜하기 취소
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    liked = LikedMovie.objects.filter(user=request.user, movie=movie)
    
    if liked.exists():
        liked.delete()
        return Response({'message': '찜 목록에서 제거됨'})
    else:
        LikedMovie.objects.create(user=request.user, movie=movie)
        return Response({'message': '찜 목록에 추가됨'})

# 영화 시청 상태 업데이트
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_movie_status(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    status = request.data.get('status')
    if status in ['미시청', '시청 중', '시청 완료']:
        movie.status = status
        movie.save()
        return Response({'message': '상태가 업데이트되었습니다.'})
    return Response({'error': '잘못된 상태 값입니다.'}, status=400)

# 영화 상세 정보 조회
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    # 현재 사용자의 재생/찜 상태 확인
    response_data = MovieSerializer(movie).data
    if request.user.is_authenticated:
        response_data['is_liked'] = LikedMovie.objects.filter(
            user=request.user, 
            movie=movie
        ).exists()
        watched_movie = WatchedMovie.objects.filter(
            user=request.user, 
            movie=movie
        ).first()
        response_data['status'] = '시청 중' if watched_movie else '미시청'
    # 장르 한글명 추가
    response_data['genres'] = [genre.name for genre in movie.genres.all()]

    
    # YouTube에서 예고편 검색
    youtube_api_key = settings.YOUTUBE_API_KEY
    youtube_url = 'https://www.googleapis.com/youtube/v3/search'
    youtube_response = requests.get(youtube_url, params={
        'key': youtube_api_key,
        'q': f'{movie.title} 예고편',
        'part': 'snippet',
        'maxResults': 1,
        'type': 'video'
    })
    youtube_data = youtube_response.json()
    if youtube_data.get('items'):
        response_data['trailer_id'] = youtube_data['items'][0]['id']['videoId']
    
    return Response(response_data)
    return Response(response_data)


#음성인식

# 음성 파일을 텍스트로 변환하는 함수
def transcribe_file(audio_file: str) -> str:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
    
    client = speech.SpeechClient()

    with open(audio_file, "rb") as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,  # WebM OPUS 형식으로 변경
        sample_rate_hertz=48000,  # 48000Hz로 변경
        language_code="ko",
        enable_automatic_punctuation=True,  # 자동 문장부호 추가
    )

    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript

# 감정 분석 함수
def sample_analyze_sentiment(text_content: str):
    client = language_v2.LanguageServiceClient()
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT
    language_code = "ko"

    document = {
        "content": text_content,
        "type_": document_type_in_plain_text,
        "language_code": language_code,
    }

    encoding_type = language_v2.EncodingType.UTF8
    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )

    sentiment_score = response.document_sentiment.score
    sentiment_magnitude = response.document_sentiment.magnitude
    return sentiment_score, sentiment_magnitude

# TMDB API 호출 함수
def search_movies(query: str):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

@csrf_exempt
def analyze_voice(request):
    # 환경 변수 명시적 설정
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
    
    if request.method == "POST" and request.FILES.get("audio_file"):
        audio_file = request.FILES["audio_file"]
        # 오디오 파일을 임시로 저장
        audio_path = "audio.wav"
        with open(audio_path, "wb") as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # 음성을 텍스트로 변환
        transcript = transcribe_file(audio_path)
        print(transcript)

        # 텍스트에 대해 감정 분석 수행
        sentiment_score, sentiment_magnitude = sample_analyze_sentiment(transcript)

        # 감정 분석 점수에 따라 TMDB에서 영화 검색 (예: 긍정적일 때 로맨스 장르, 부정적일 때 액션 영화)
        if sentiment_score > 0:
            movies = search_movies("romance")
        else:
            movies = search_movies("action")
        return JsonResponse({
            "transcript": transcript,
            "sentiment_score": sentiment_score,
            "sentiment_magnitude": sentiment_magnitude,
            "movies": movies,
        })
    

    return JsonResponse({"error": "No audio file provided"}, status=400)