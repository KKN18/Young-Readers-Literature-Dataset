from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.amazon.com/s?crid=1UIBJIWGRXOMG&k=child%20books&ref=glow_cls&refresh=2&sprefix=%2Caps%2C288"
driver.get(url)

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 's-image')))

soup = BeautifulSoup(driver.page_source, 'html.parser')

books_info = []
for img in soup.find_all('img', {'class': 's-image'}):
    parent_a_tag = img.find_parent('a', {'class': 'a-link-normal s-no-outline'})
    if parent_a_tag and 'href' in parent_a_tag.attrs:
        link = "https://www.amazon.com" + parent_a_tag['href']
        title = img['alt'] if 'alt' in img.attrs else 'No Title'
        books_info.append({'title': title, 'link': link})

for book in books_info:
    print(book['title'], book['link'])
    driver.get(book['link'])
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-price')))

    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    price_element = page_soup.find('span', {'class': 'a-price'})
    if price_element:
        price = price_element.get_text(strip=True)
        print(f"Price for '{book['title']}': {price}")

    # 책 소개 추출
    description_element = page_soup.find('div', {'class': 'a-expander-content'})
    if description_element:
        description = description_element.get_text(strip=True)
        print(f"Description for '{book['title']}': {description}\n")

driver.quit()
