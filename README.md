# 📅 KakaoTalk Morning Briefing Bot

매일 아침 **별내동 날씨 정보**, **네이버 많이 본 뉴스 TOP 5**, **오늘의 명언**을 수집하여 카카오톡 '나에게 보내기'로 자동 전송해 주는 파이썬 스크립트입니다.

---

## 🚀 주요 기능
* **🌤️ 날씨 브리핑**: Open-Meteo API 기반 기온 정보 및 네이버 날씨 기상특보(폭염/호우) 크롤링
* **🔥 뉴스 브리핑**: 네이버 랭킹 뉴스 크롤링 기반 언론사별 많이 본 뉴스 TOP 5 추출
* **💡 오늘의 명언**: 동기부여 명언 랜덤 발송
* **📲 카카오톡 전송**: 카카오톡 Open API를 활용한 나에게 메시지 전송

---

## 🛠️ 기술 스택
* **Language**: Python 3
* **Libraries**: `requests`, `beautifulsoup4`
* **API**: KakaoTalk Talk Memo API, Open-Meteo API

---

## 📦 실행 방법

### 1. 필수 패키지 설치
```bash
pip install requests beautifulsoup4