import folium
import random
from branca.colormap import linear
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import json
import requests
import io
import os

current_directory = os.getcwd()


import folium
import random
import json
import requests

# 전 세계 국가의 GeoJSON 데이터를 가져오기
geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
geojson_data = requests.get(geojson_url).json()

# 모든 국가에 대해 무작위 데이터 생성
country_data = {country['properties']['name']: random.randint(10, 100) for country in geojson_data['features']}

# 중국과 미국에 더 높은 값을 부여하여 색상 구분이 두드러지게 만듭니다.

# 색상 맵 생성 (낮은 값은 파란색, 높은 값은 빨간색)
colormap = linear.RdYlBu_11.scale(min(country_data.values()), max(country_data.values()))
colormap.caption = 'Book Count'

# 지도 생성 (중앙 위치를 아시아 지역으로 설정)
world_map = folium.Map(location=[34, 100], zoom_start=1)

# Choropleth 레이어 추가
folium.Choropleth(
    geo_data=geojson_data,
    data=country_data,
    columns=['Country', 'Value'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',  # Yellow, Orange, Red 색상 팔레트 사용
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Book Count',
    reset=True
).add_to(world_map)

# 색상 맵을 지도에 추가
colormap.add_to(world_map)

# 지도를 HTML 파일로 저장
world_map.save("world_map.html")


# HTML 파일의 절대 경로 생성
html_file_path = os.path.join(current_directory, "world_map.html")

# Selenium 웹 드라이버 설정
service = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=service, options=chrome_options)

# 저장한 HTML 파일을 열고 지도 렌더링
driver.get(f"file://{html_file_path}")
time.sleep(5)  # 지도가 렌더링되는 시간을 기다립니다.

# 지도의 스크린샷을 PNG 파일로 저장
png = driver.get_screenshot_as_png()
driver.quit()

# PNG 이미지 데이터를 파일로 저장
with open("world_map.png", "wb") as file:
    file.write(png)

