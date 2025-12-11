## 🔍 Project Overview – Samply (Weather-based Music Recommender)

Samply는 **사용자가 선택한 위치의 실시간 날씨 정보를 기반으로 분위기에 맞는 음악을 자동 추천하는 웹서비스**이다.  
OpenWeather API로 수집한 날씨 + Selenium 기반 멜론(Melon) 크롤링을 결합하여  
날씨 분위기별 음악을 3곡씩 자동 추천해준다.  
(참고: PDF 1~4p)

---

## ☁ 주요 기능 (PDF p.4)

### ✔ 1) 위치 선택 기능  
- 시/도 → 시/군/구 2단계 선택 구조  
- 사용자가 원하는 지역의 날씨 조회 가능

### ✔ 2) 실시간 날씨 정보 제공  
- OpenWeather API 기반  
- 도시 이름 → city_id 매핑  
- weather / temperature 실시간 조회

### ✔ 3) 날씨 기반 음악 추천  
- 날씨 → 키워드 매핑  
  - Clear → “맑은날”  
  - Rain → “비오는날”  
  - Snow → “눈오는날” 등  
- 키워드 기반 Melon DJ 플레이리스트 해시태그 검색  
- Selenium으로 플레이리스트 정보 수집  
- 20곡 중 랜덤 3곡을 추천

### ✔ 4) 추천된 음악 바로 보기  
- 음악 제목 클릭 → 자동으로 유튜브 검색 페이지로 이동  

---

## ⚙ 동작 플로우 (PDF p.5)


---

## 💻 코드 구현 (PDF p.6~17)

### ✔ home.html – 위치 선택
- select 2개(시/도, 시/군/구)
- submit 시 → `/index?city=서울특별시` 형태로 전달

### ✔ app.py 주요 기능
- @app.route("/") → home.html 렌더링  
- @app.route("/index") →  
  - city 파싱  
  - 날씨 조회  
  - 키워드 변환  
  - Melon 크롤링  
  - index.html로 데이터 전달

### ✔ OpenWeather API (PDF p.9~10)
- `&units=metric`으로 섭씨 변환  
- 온도는 round(value, 1)로 소수 1자리 반올림  
- 응답 JSON에서 weather/main 추출

### ✔ Melon DJ 크롤링 (PDF p.13~15)
- Selenium 기반 자동화  
- 해시태그 검색 페이지 접속  
- playlist 요소 목록 수집  
- 랜덤 playlist 선택  
- 그 안에서 1~20번곡 중 랜덤 3곡 추출  
- title / artist / album_img 수집 후 results 배열에 저장

### ✔ index.html 렌더링 (PDF p.17)
- 날씨/온도 출력  
- 날씨 아이콘 출력  
- 추천된 노래 3곡 보여주기  

---

## ⚠ 트러블슈팅 (PDF p.18~20)

### ✔ 문제 1: HTTP 환경에서 위치 정보 차단  
- 외부 기기 접속 시 위치 정보 제공 불가  
➡ 해결: **사용자가 직접 위치 선택하도록 구조 변경**

### ✔ 문제 2: 로딩 지연으로 음악 정보 누락  
- Selenium이 렌더링보다 먼저 크롤링 시도  
➡ 해결: **time.sleep() 지연 추가 → 요소 로딩 안정화**

---

## 🎥 시연 영상 (PDF p.21)
- 카메라로 QR 촬영 → 웹서비스 접속  
- 실시간 날씨 기반 음악 추천 과정 확인 가능

---

## 👥 팀원 역할 (PDF p.22~23)

| 이름 | 역할 |
|------|------|
| 이○준 | Flask 서버 / 데이터 처리 / 발표 |
| 채○석 | HTML UI 개발 / 발표 |
| 노○빈 | 웹 구성 / 크롤링 / PPT |
| 유○훈 | 크롤링 / 데이터 처리 / PPT |

---

## 🎧 팀원 추천곡 (PDF p.23)
- Secret Base  
- Unstoppable  
- Hi Bully  
- 최유리 – 사랑  



## 📄 Samply – 날씨 기반 음악 추천 웹서비스 (PDF Report)

전체 프로젝트 발표 자료는 아래 PDF에서 확인할 수 있습니다.

👉 [📘 **Samply PDF 열기**](./3조(삼플리).pdf)



:contentReference[oaicite:1]{index=1}

---

### 📌 PDF 미리보기 썸네일 (옵션)

[![PDF Preview](./samply_page1.png)](./3조(삼플리).pdf)

