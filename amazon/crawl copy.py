from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")  # Sandbox 기능 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 안 함
chrome_options.add_argument("--headless")  # Headless 모드 활성화
chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화 (특히 Linux에서 유용)
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

# 웹 드라이버 설정 및 초기화
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Amazon 페이지에 접속
url = "https://www.amazon.com/s?bbn=4&rh=n%3A2578998011%2Cp_n_feature_nine_browse-bin%3A3291437011&dc&qid=1699963461&rnid=3291435011&ref=lp_4_nr_p_n_feature_nine_browse-bin_0"
driver.get(url)

# 페이지의 특정 요소가 로드될 때까지 대기
# 예시: 페이지에 'footer' 섹션이 로드될 때까지 대기
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, 'footer')))

# BeautifulSoup 객체 생성
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 페이지 소스 출력
print(driver.page_source)

# 브라우저 닫기
driver.quit()



# 모든 링크 추출
# all_links = [link['href'] for link in soup.find_all('a', href=True)]

# 첫 10개 링크 출력 (또는 전체 링크 출력)
# print(all_links)
