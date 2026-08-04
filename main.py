import requests
from bs4 import BeautifulSoup
import warnings
from datetime import datetime
import random
import json

# 경고 메시지 숨기기
warnings.filterwarnings("ignore")

# 1. 모닝 브리핑 텍스트 생성 함수
def build_briefing_message():
    message_text = ""
    
    # [날짜 정보]
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    now = datetime.now()
    today_str = now.strftime("%Y년 %m월 %d일")
    weekday_str = weekdays[now.weekday()]
    
    message_text += f"📅 [{today_str} ({weekday_str}) 모닝 브리핑]\n\n"
    
    # [날씨 정보]
    try:
        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            "latitude=37.648&longitude=127.118&"
            "current_weather=true&"
            "daily=temperature_2m_max,temperature_2m_min&"
            "timezone=Asia%2FTokyo"
        )
        res = requests.get(weather_url, timeout=5).json()
        current_temp = f"{res['current_weather']['temperature']}°C"
        max_temp = f"{res['daily']['temperature_2m_max'][0]}°C"
        min_temp = f"{res['daily']['temperature_2m_min'][0]}°C"
        
        special_report = ""
        try:
            naver_url = "https://weather.naver.com/today/02390130"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
            n_res = requests.get(naver_url, headers=headers, timeout=3)
            page_text = n_res.text
            
            if "폭염경보" in page_text:
                special_report = "폭염경보 발효 중 🥵"
            elif "폭염주의보" in page_text:
                special_report = "폭염주의보 발효 중 🥵"
            elif "호우경보" in page_text or "호우주의보" in page_text:
                special_report = "호우특보 발효 중 ☔"
            elif float(res['daily']['temperature_2m_max'][0]) >= 33:
                special_report = "폭염 특보 발효 중 🥵"
        except Exception:
            if float(res['daily']['temperature_2m_max'][0]) >= 33:
                special_report = "폭염 주의/경보 발효 중 🥵"

        message_text += "🌤️ [오늘 별내동 날씨]\n"
        # 현재 기온 표시 후 (최저/최고) 줄바꿈 처리
        message_text += f"• 기온 : 현재 {current_temp}\n"
        message_text += f"  (최저 {min_temp} / 최고 {max_temp})\n"
        
        if special_report:
            message_text += f"🚨 기상특보 : {special_report}\n"
            
        if "폭염" in special_report or float(res['daily']['temperature_2m_max'][0]) >= 33:
            message_text += "💡 폭염이 계속되니 수분을 충분히 섭취하시고 야외활동을 자제하세요!\n"
        else:
            message_text += "💡 오늘도 활기차고 즐거운 하루 보내세요! 😊\n"

    except Exception:
        message_text += "🌤️ 날씨 정보를 불러오지 못했습니다.\n"

    # [섹션 간 여백]
    message_text += "\n\n"

    # [뉴스 정보 - 네이버 '많이 본 뉴스' TOP 5]
    try:
        ranking_news_url = "https://news.naver.com/main/ranking/popularDay.naver"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        res = requests.get(ranking_news_url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        
        news_boxes = soup.select(".rankingnews_box")
        
        titles = []
        for box in news_boxes:
            press_name = box.select_one(".rankingnews_name")
            press_str = press_name.text.strip() if press_name else ""
            
            first_news = box.select_one(".rankingnews_list li a")
            if first_news:
                title = first_news.text.strip()
                if title and title not in titles:
                    if len(title) > 25:
                        title = title[:25] + "..."
                    
                    if press_str:
                        titles.append(f"[{press_str}] {title}")
                    else:
                        titles.append(title)
                        
            if len(titles) == 5:
                break
                
        message_text += "🔥 [오늘의 네이버 많이 본 뉴스 TOP 5]\n"
        if titles:
            for idx, title in enumerate(titles, start=1):
                message_text += f"{idx}. {title}\n"
        else:
            message_text += "• 많이 본 뉴스를 가져오지 못했습니다.\n"
        
    except Exception:
        message_text += "📰 뉴스를 불러오지 못했습니다.\n"

    # [섹션 간 여백]
    message_text += "\n\n"

    # [오늘의 명언]
    quotes = [
        "\"시작하는 방법은 말하기를 그만두고 행동하는 것이다.\"\n- 월트 디즈니",
        "\"위대한 일을 하는 유일한 방법은 당신이 하는 일을 사랑하는 것이다.\"\n- 스티브 잡스",
        "\"오늘 할 수 있는 일에 전력을 다하라. 그러면 내일은 한 걸음 더 나아가 있을 것이다.\"\n- 뉴턴",
        "\"행복은 습관이다. 그것을 몸에 익혀라.\"\n- 허버드",
        "\"미래를 예측하는 가장 좋은 방법은 미래를 창조하는 것이다.\"\n- 피터 드러커",
        "\"작은 변화가 일어날 때 진정한 삶을 살게 된다.\"\n- 레오 Тол스토이"
    ]
    message_text += "💡 [오늘의 명언]\n"
    message_text += random.choice(quotes)
    
    return message_text

# 2. 카카오톡 전송 함수
def send_kakao_message(text):
    with open("kakao_code.json", "r") as fp:
        tokens = json.load(fp)
        
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": "Bearer " + tokens["access_token"]
    }
    
    EXACT_URL = "https://m.news.naver.com/rankingList"
    
    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": text,
            "link": {
                "web_url": EXACT_URL,
                "mobile_web_url": EXACT_URL
            }
        })
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.json().get("result_code") == 0:
        print("\n📲 카카오톡으로 모닝 브리핑 전송 성공!")
    else:
        print("\n❌ 카카오톡 전송 실패:", response.json())

# 3. 프로그램 실행
if __name__ == "__main__":
    briefing = build_briefing_message()
    print(briefing)             # 터미널 출력
    send_kakao_message(briefing) # 내 카카오톡 전송