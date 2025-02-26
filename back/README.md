# CineCode-PJT


1. 가상 환경 생성
```
python -m venv venv
```

2. 가상 환경 활성화
```
source venv/Scripts/activate
```

3. 패키지 설치
```
pip install -r requirements.txt
```

4. 실행
```
python manage.py makemigrations
```

```
python manage.py migrate
```

```
python manage.py loaddata genre_data.json genre_secure_movie_data.json category_data.json category_tag_data.json
```

```
python manage.py runserver
```

### `pip install -r requirements.txt` django 설치 오류 시 pip 버전 업데이트
```
python -m pip install --upgrade pip setuptools wheel
```

### `pip install -r requirements.txt` matplotlib 설치 오류 시 pip 버전 업데이트
✅ Visual Studio Build Tools 설치 (Windows)
matplotlib은 일부 환경에서 C++ 컴파일러가 필요합니다. 이를 해결하려면:

[Visual Studio Build Tools 다운로드](https://visualstudio.microsoft.com/ko/visual-cpp-build-tools/)
설치할 때 "C++ Build Tools" 체크
추가 컴포넌트에서 "Windows 10 SDK", "C++ CMake Tools for Windows" 체크
설치 완료 후, PC 재부팅
