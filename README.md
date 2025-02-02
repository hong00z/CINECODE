# CineCode-PJT

## 개발 기간
2024.11.17 ~ 2024.11.27

## 팀원
#### 김민주 : (FE&BE) MovieDetail, Review CRUD, Navbar <br>
#### 최연지 : (FE&BE) Login, Signup, Profile, Home, Search, 음성인식

---

## 개발 환경
- Python 3.11.X
- Django 4.2.X
- Vue 3.X

---

## ERD
![ERD](./images/ERD.png)

---

## 영화 추천 알고리즘
#### AI를 활용한 사용자 음성 인식 기반 감정 분석 추천
1. Web Speech API와 MediaRecorder API를 활용하여 사용자의 음성을 녹음하고 실시간으로 텍스트로 변환하며, 5초간의 음성 데이터를 수집합니다. (back/moveis/views.py analyze_sentiment 참고)
2. 수집된 음성 데이터는 서버로 전송되어 감정 분석(sentiment analysis)을 수행하고, 분석된 감정 점수를 기반으로 영화를 추천합니다. (back/moveis/views.py recommend_movies 참고)
3. 분석 결과는 프론트엔드에서 캐러셀 형태로 표시되며, localStorage를 통해 검색 결과를 저장하여 페이지 새로고침 시에도 이전 검색 결과를 유지합니다. (front/src/views/movies/SearchView.vue 참고)

---

## 핵심 기능
- 영화 추천 알고리즘
- 영화 리뷰 작성, 수정, 삭제
- 영화 리뷰 조회
- 영화 검색

---

## Daily Report
### 1117(일) 
>[민주]
>- [X] 피그마&컴포넌트 구조 작성 - 로그인, 회원가입
>
>[연지]
>- [x] ERD 설계

### 1118(월)
>[민주]
>- [X] DB - 초기 영화, 장르 데이터 생성
>- [X] 피그마&컴포넌트 구조 작성 - 홈
>
>[연지]
>- [X] 프로젝트 생성
>- [X] 로그인,회원가입 프론트

### 1119(화)
>[민주]
>- [X] HomeView -  프론트, 백엔드
>- [X] 피그마&컴포넌트 구조도 작성 - 커뮤니티, 영화 상세 정보, 프로필
>
>[연지]
>- [X] 회원가입 백앤드
>- [X] ERD 수정

### 1120(수)
>[민주]
>- [X] HomeView 마무리
>- [X] Navbar - 프론트, 백엔드
>
>[연지]
>- [X] LoginView - 로그인 구현
>- [X] Navbar - 메인화면에 로그인된거 띄우기

### 1121(목)
>[민주]
>- [X] MovieDetail - 영화 정보, 예고편 프론트
>- [X] MovieDetail - 영화 정보, 예고편 백엔드
>- [X] DB - fixtures 데이터 수정
>      
>[연지]
>- [X] UpdateView - 회원정보 수정
>- [X] ProfileVIew - 프로필 프론트,백앤드

### 1122(금)
>[민주]
>- [X] MovieDetail - 찜하기, 시청 상태 프론트
>- [X] MovieDetail - 찜하기, 시청 상태 백엔드
>      
>[연지]
>- [X] 음성 API 끌고 오기, 연결
>- [X] UpdateView - 프로필 사진 수정

### 1123(토)
>[민주]
>- [X] SearchView - URL 쿼리 처리
>      
>[연지]
>- [X] 음성인식 실시간으로 작성, 스크롤

### 1124(일)
>[민주]
>- [X] ReviewReadCard - 프론트, 백엔드
>- [X] ReviewCreateCard - 프론트, 백엔드
>      
>[연지]
>- [X] SearchView - 음성인식 오류 해결
>- [X] ProfileView - css 수정

### 1125(월)
>[민주]
>- [X] SearchView - URL 쿼리 처리 재수정
>- [X] ReviewUDCard - 프론트, 백엔드
>
>[연지]
>- [X] HomeView - 검색창 작업
>- [X] HomeView - 검색창 css 작업

### 1126(화)
>[민주]
>- [X] DB - 초기 데이터 작업
>- [X] MovieDetail - 예고편 링크 수정
>- [X] HomeView - MovieCard css 작업 (정렬 수정)
>
>[연지]
>- [X] DB - 초기 데이터 작업
>- [X] ReviewCard - css 작업
>- [X] Navbar - 시계 추가
>- [X] PPT 작업

### 1127(수)
> 최종 발표

---

## 생성형 AI를 활용한 TIL
### 1123(토)
>[민주]
> #### router를 사용하면서 URL에 query를 표시하지 않는 방법
> HomeView.vue에서 SearchView.vue로 데이터를 전달할 때 2가지 방법이 존재
> 1. router의 params를 사용 <br>
> >1-1. 먼저 라우터 설정을 수정합니다:
> >```
> > {
> >  path: '/search/:searchData?',  // optional parameter
> >  name: 'Search',
> >  component: SearchView
> > }
> > ```
> >
> > 1-2. HomeView.vue를 수정합니다:
> > ```
> > router.push({
> >     name: 'Search',
> >     params: {
> >       searchData: btoa(JSON.stringify(searchData)) // base64로 인코딩
>>     },
> >     replace: true // URL 히스토리를 남기지 않음
>>   });
>> ```
>>
> > 1-3. SearchView.vue에서 params를 받아서 처리합니다:
> >```
> > onMounted(() => {
> >   if (route.params.searchData) {
> >     const searchData = JSON.parse(atob(route.params.searchData)); // base64 디코딩
> >     transcript.value = searchData.transcript;
> >     sentiment.value = searchData.sentiment;
> >     movies.value = searchData.movies;
> >   }
> > });
> > ```
>
> 2. router.push 시에 replace: true와 함께 query를 사용한 후, 즉시 query를 제거 <br>
> > 2-1. router 설정에 props: true 추가
> > ```
> > router.push({
> >    name: 'Search',
> >    query: {
> >      transcript: data.transcript,
> >      sentiment: data.sentiment_score,
> >      movies: JSON.stringify(data.movies)
> >    },
> >    replace: true
> >  }).then(() => {
> >     // query 제거
> >     router.replace({ name: 'Search' });
> >   });
> > ```
>
> 위의 방법을 사용하였던 데이터가 완전히 로드되기 전에 query가 제거되어 데이터가 사라지는 문제가 있었음.
> > 1. HomeView.vue는 기존 그대로 유지
> > 2. SearchView.vue에서 데이터를 로드한 후 URL을 정리합니다:
> > ```
> > onMounted(() => {
> >   // URL의 query params에서 데이터 가져오기
> >   const queryTranscript = route.query.transcript;
> >   const querySentiment = route.query.sentiment;
> >   const queryMovies = route.query.movies;
> >
> >   if (queryTranscript && querySentiment && queryMovies) {
> >     // 데이터 설정
> >     transcript.value = queryTranscript;
> >     sentiment.value = Number(querySentiment);
> >     movies.value = JSON.parse(queryMovies);
> >
> >     // 데이터 설정 후 URL 정리
> >     router.replace({ path: '/search' });
> >   }
> > });
> > ```
> >이렇게 하면:
> > - SearchView가 마운트될 때 먼저 query 파라미터에서 데이터를 가져옵니다
> > - 데이터를 컴포넌트의 상태로 설정합니다
> > - 그 후에 URL을 깔끔하게 정리합니다
> > - 이후 새로운 검색도 정상적으로 동작합니다
>
> 위의 방법대로 했는데 JSON 파싱 에러가 발생하여 claude-3.5-sonnet 모델을 활용한 cursor가 알려준 코드로 수정 <br>
> **쿼리 파라미터 처리 후 깨끗한 URL로 변경 (SearchView.vue onMounted 참고)**

---

## 시간 남으면 추가 할 거

- [ ] LoginView -회원가입 안 된 계정 에러 처리
- [ ] SignupView - ID 중복 처리 (이미 가입된 계정 구분)
- [ ] 사용자 ID랑 Email 필드 서로 바꾸기
- [ ] 소셜 로그인

---

## 소감

 **김민주** <br>
 새로운 언어와 프레임워크를 사용하여 프로젝트를 제작하다보니 생각보다 어려웠던 부분도 많고 뜻대로 작동하지 않아 막막했던 순간도 많았지만, 좋은 팀원과 AI 툴(Special thanks to Cursor...) 덕분에 프로젝트를 끝까지 완성할 수 있었습니다. 이번 프로젝트가 앞으로 있을 협업과 개발자로서의 커리어에 초석을 다지는 계기가 된 것 같아 뿌듯하고 의미 있는 시간이었습니다. <br> 
 **최연지** <br>
 API를 활용한 데이터 처리 과정에서 어려움이 있었지만 문제 해결을 통해 많은 지식을 습득할 수 있었습니다. 팀원과의 원활한 협업을 통해 프로젝트를 성공적으로 완수하는 큰 성취감을 느낄 수 있었습니다. 이번 프로젝트를 통해 이전보다 더 깊이 있는 경험을 쌓을 수 있었고, 실무 역량과 협업 능력을 한층 강화할 수 있었습니다. 
