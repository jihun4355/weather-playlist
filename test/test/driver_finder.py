from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import random
from flask import redirect, url_for

app = Flask(__name__)
load_dotenv()
API_KEY = os.getenv("API_KEY")

# OpenWeathermap 에서 찾은 도시 이름과 city_id 를 딕셔너리로 만들기
city_name_to_id = {
    "서울특별시": 1835847, "부산광역시": 1838519, "대구광역시": 1835327, "대전광역시": 1835224,
    "광주광역시": 1841808, "인천광역시": 1843561, "울산광역시": 1833742, "고양시": 1842485,
    "부천시": 1838716, "용인시": 1832427, "수원시": 1835553, "화성시": 1843847,
    "하남시": 1897007, "남양주시": 1897122, "오산시": 1839652, "파주시": 1840898, "군포시" : 1842030,
    "평택시": 1838343, "보령시": 1835447, "부여군": 1838508, "공주시": 1842616,
    "논산시": 1840211, "예산군": 1832771, "천안시": 1845759, "청주시": 1845604,
    "충주시": 1845033, "강릉시": 1843137, "인제군": 1843542, "원주시": 1833105,
    "속초시": 1836553, "화천군": 1844045, "양양군": 1832809, "춘천시": 1845136,
    "목포시": 1841066, "무안군": 1840982, "무주군": 1840942, "화순군": 1843841,
    "신안군": 6395804, "익산시": 1843491, "진안군": 1846114, "임실군": 1843585,
    "완주군": 1833466, "창원시": 1846326, "김해시": 1842943, "남해군": 1840454,
    "밀양시": 1841149, "양산시": 1832828, "창녕군": 6903078, "함양군": 1844533,
    "김천시": 1842944, "상주시": 1837706, "포항시": 1839071, "울진군": 1833105,
    "구미시": 1842225, "제주특별자치도": 1846265
}

# 날씨 → 키워드 ()
def weather_to_keywords(weather):
    mapping = {
        "Clear": "맑음",
        "Clouds": "흐림",
        "Rain": "비",
        "Snow": "눈",
        "Thunderstorm": "천둥번개",
        "Drizzle": "이슬비",
        "Fog": "안개"
    }
    return mapping.get(weather)

# 도시 ID기반 날씨 정보 가져오기
def get_weather_by_city_id(city_id):
    url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()
    if 'weather' not in res or 'main' not in res :
        return "정보 없음", "정보 없음", "알 수 없음"
    weather = res['weather'][0]["main"]
    temp = round(res['main']['temp'],1)
    return weather, temp


# Chrome 드라이버 생성
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(current_dir, 'chromedriver.exe')
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# 멜론 DJ 플레이리스트 크롤링
def crawl_melon_dj(keyword):
    driver = create_driver()
    results = []
    try:
        driver.get(f"https://www.melon.com/dj/djfinder/djfinder_inform.htm?djSearchType=T&djSearchKeyword=%23{keyword}")
        time.sleep(0.2)

        playlist_items = driver.find_elements(By.CSS_SELECTOR, "#djPlylstList > div > ul > li")
        playlist_count = len(playlist_items)
        playlist_random = random.randint(1, playlist_count)
        playlist_selector = f"#djPlylstList > div > ul > li:nth-child({playlist_random}) > div.thumb > a > span" 
        playlist = driver.find_element(By.CSS_SELECTOR, playlist_selector) # 플레이리스트 선택
        playlist.click()
        time.sleep(0.3)

        for i in random.sample(range(1,20),3):
            title_selector = f"#frm > div > table > tbody > tr:nth-child({i}) > td:nth-child(5) > div > div > div.ellipsis.rank01 > span > a"
            artist_selector = f"#frm > div > table > tbody > tr:nth-child({i}) > td:nth-child(5) > div > div > div.ellipsis.rank02 > a"
            album_img_selector = f"#frm > div > table > tbody > tr:nth-child({i}) > td:nth-child(3) > div > a > img"

            title = driver.find_element(By.CSS_SELECTOR, title_selector).text.strip()
            artist = driver.find_element(By.CSS_SELECTOR, artist_selector).text.strip()

            album_img_element = driver.find_element(By.CSS_SELECTOR, album_img_selector)
            album_img_url = album_img_element.get_attribute("src")

            results.append({
                "title": title,
                "artist": artist,
                "album_img": album_img_url
            })

    except Exception as e:
        print("크롤링 오류:", e)
    finally:
        driver.quit()
    return results

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/index")
def index():
    city = request.args.get("city")
    city_id = city_name_to_id.get(city)
    weather, temp = get_weather_by_city_id(city_id)
    keywords = weather_to_keywords(weather)
    songs = crawl_melon_dj(keywords)

    return render_template("index.html",
                           city=city,
                           weather=weather,
                           temp=temp,
                           keywords=keywords,
                           songs=songs)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
