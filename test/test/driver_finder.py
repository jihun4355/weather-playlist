

from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import random



app = Flask(__name__)
load_dotenv()
API_KEY = os.getenv("API_KEY")







@app.route('/')
def location_notice():
    return render_template('location.html')




# 날씨 코드 → 그룹 분류
def weather_code_to_group(code):
    if 200 <= code < 300:
        return "Thunderstorm"
    elif 300 <= code < 400:
        return "Drizzle"
    elif 500 <= code < 600:
        return "Rain"
    elif 600 <= code < 700:
        return "Snow"
    elif 700 <= code < 800:
        return "Atmosphere"
    elif code == 800:
        return "Clear"
    elif 801 <= code <= 804:
        return "Clouds"
    else:
        return "Unknown"

# 날씨 → 키워드
def weather_to_keywords(weather):
    mapping = {
        "Clear": "#맑음",
        "Clouds": "#흐림",
        "Rain": "#비오는날",
        "Snow": "#눈오는날",
        "Thunderstorm": "#천둥번개",
        "Drizzle": "#이슬비",
        "Atmosphere": "#안개"
    }
    return [mapping.get(weather, "#감성")]

# 위도/경도 기반 날씨 정보 가져오기
def get_weather_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()
    print("=== OpenWeather 응답 ===")
    print(res)
    if 'weather' not in res or 'main' not in res:
        return "정보 없음", "정보 없음"
    weather_code = res['weather'][0]['id']
    weather = weather_code_to_group(weather_code)
    temp = res['main']['temp']
    return weather, temp

# BigDataCloud를 통해 한글 도시명 얻기
def get_korean_city_name(lat, lon):
    url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=ko"
    res = requests.get(url).json()
    print("=== BigDataCloud 응답 ===")
    print(res)
    if "city" in res and res["city"]:
        return res["city"]
    elif "locality" in res and res["locality"]:
        return res["locality"]
    elif "principalSubdivision" in res:
        return res["principalSubdivision"]
    else:
        return "알 수 없음"

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
# def crawl_melon_dj(keyword):
#     driver = create_driver()
#     results = []
#     try:
#         driver.get("https://www.melon.com")
#         time.sleep(2)

#         dj_menu = driver.find_element(By.CSS_SELECTOR, 'div#gnb_menu a[href="/dj/today/djtoday_list.htm"]')
#         dj_menu.click()
#         time.sleep(2)

#         search_input = driver.find_element(By.ID, 'djSearchKeyword')
#         search_input.clear()
#         for ch in keyword:
#             search_input.send_keys(ch)
#             time.sleep(0.1)
#         search_input.send_keys(Keys.RETURN)
#         time.sleep(2)

#         playlist_selector = "#djPlylstList > div > ul > li:nth-child(1) > div.thumb > a > span"
#         playlist = driver.find_element(By.CSS_SELECTOR, playlist_selector)
#         playlist.click()
#         time.sleep(2)

#         for i in range(1, 4):
#             title_selector = f"#frm > div > table > tbody > tr:nth-child({i}) > td:nth-child(5) > div > div > div.ellipsis.rank01 > span > a"
#             artist_selector = f"#frm > div > table > tbody > tr:nth-child({i}) > td:nth-child(5) > div > div > div.ellipsis.rank02 > a"
#             album_img_selector = f"#frm > div > table > tbody > tr:nth-child({i}) > td:nth-child(3) > div > a > img"

#             title = driver.find_element(By.CSS_SELECTOR, title_selector).text.strip()
#             artist = driver.find_element(By.CSS_SELECTOR, artist_selector).text.strip()

#             album_img_element = driver.find_element(By.CSS_SELECTOR, album_img_selector)
#             album_img_url = album_img_element.get_attribute("src")

#             results.append({
#                 "title": title,
#                 "artist": artist,
#                 "album_img": album_img_url
#             })

#     except Exception as e:
#         print("크롤링 오류:", e)
#     finally:
#         driver.quit()

#     return results

def crawl_melon_dj(keyword):
    driver = create_driver()
    results = []
    try:
        driver.get("https://www.melon.com")
        time.sleep(2)

        dj_menu = driver.find_element(By.CSS_SELECTOR, 'div#gnb_menu a[href="/dj/today/djtoday_list.htm"]')
        dj_menu.click()
        time.sleep(2)

        search_input = driver.find_element(By.ID, 'djSearchKeyword')
        search_input.clear()
        for ch in keyword:
            search_input.send_keys(ch)
            time.sleep(0.1)
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)

        playlist_selector = "#djPlylstList > div > ul > li:nth-child(1) > div.thumb > a > span"
        playlist = driver.find_element(By.CSS_SELECTOR, playlist_selector)
        playlist.click()
        time.sleep(2)

        # 최대 10곡까지 가져온 후 랜덤 추천
        for i in range(1, 100):
            try:
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
            except:
                continue

        # 3곡 랜덤 선택
        results = random.sample(results, min(3, len(results)))

    except Exception as e:
        print("크롤링 오류:", e)
    finally:
        driver.quit()

    return results




@app.route("/weather")
def get_location_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    weather, temp = get_weather_by_coords(lat, lon)
    city = get_korean_city_name(lat, lon)
    return jsonify({"city": city, "weather": weather, "temp": temp})

@app.route('/index')
def index():
    city = request.args.get("city")
    weather = request.args.get("weather")
    temp = request.args.get("temp")

    if not all([city, weather, temp]):
        return render_template("index.html", city="로딩 중...", weather="정보 없음", temp="정보 없음", keywords=[], songs=[])

    keywords = weather_to_keywords(weather)
    first_keyword = keywords[0] if keywords else "#감성"
    songs = crawl_melon_dj(first_keyword)

    return render_template("index.html",
                           city=city,
                           weather=weather,
                           temp=temp,
                           keywords=keywords,
                           songs=songs)


if __name__ == "__main__":
    app.run(debug=True)

