from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

# 웹 드라이버 설정 및 초기화
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Amazon 페이지에 접속
url = "https://www.amazon.com/s?k=child+books&crid=1UIBJIWGRXOMG&sprefix=%2Caps%2C288&ref=nb_sb_ss_recent_1_0_recent"
driver.get(url)

# 페이지가 로드될 때까지 대기
driver.implicitly_wait(10)

# BeautifulSoup 객체 생성
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 's-image' 클래스를 가진 모든 요소 추출
s_image_elements = soup.find_all(class_='s-image')

# 추출된 요소의 정보 출력
for element in s_image_elements:
    print(element, '\n')  # 각 요소의 HTML 내용 출력

# 브라우저 닫기
driver.quit()