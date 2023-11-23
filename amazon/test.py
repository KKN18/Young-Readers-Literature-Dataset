from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json

def extract_info(text):
    # 정규 표현식을 사용하여 필요한 정보 추출
    match = re.search(r":\s*(.+)", text)
    return match.group(1).strip() if match else "Information not found"

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("accept-language=en-US,en")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

base_url = "https://www.amazon.com/s?k=child+books&language=en_US&crid=1UIBJIWGRXOMG&refresh=2&sprefix=%2Caps%2C288&ref=glow_cls"
driver.get(base_url)

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 's-image')))

soup = BeautifulSoup(driver.page_source, 'html.parser')

books_info = []

for page_number in range(1, 8):  # 1부터 7까지 페이지를 순회
    current_url = f"{base_url}&page={page_number}"
    driver.get(current_url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 's-image')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 페이지의 책 정보 수집 로직
    # 각 페이지의 책 정보를 books_info 리스트에 추가
    for img in soup.find_all('img', {'class': 's-image'}):
        parent_a_tag = img.find_parent('a', {'class': 'a-link-normal s-no-outline'})
        if parent_a_tag and 'href' in parent_a_tag.attrs:
            link = "https://www.amazon.com" + parent_a_tag['href']
            title = img['alt'] if 'alt' in img.attrs else 'No Title'
            books_info.append({'title': title, 'link': link})

    print(f"Processed page {page_number}")


books_data = []

for book in books_info:
    print(f"Processing {book['title']} - {book['link']}")
    driver.get(book['link'])
    css_selector = 'ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list'
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    price_element = page_soup.find('span', {'class': 'a-price'})
    if price_element:
        price = price_element.get_text(strip=True)
        # print(f"Price: {price}")

    # 책 소개 추출
    description_element = page_soup.find('div', {'class': 'a-expander-content'})
    if description_element:
        description = description_element.get_text(strip=True)
        # print(f"Description: {description}\n")

    detail_ul = page_soup.find('ul', class_='a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list')
    if detail_ul:
        # 각 'li' 태그 내에서 정보 추출
        for li in detail_ul.find_all('li'):
            text = li.get_text(strip=True)
            if 'pages' in text:
                book_length = text
            if 'Reading age' in text:
                target_age = text
            if 'Dimensions' in text:
                dimension = text

        book_length = extract_info(book_length)
        target_age = extract_info(target_age)
        dimension = extract_info(dimension)
        # 추출된 정보 출력
        # print(f"Book Length: {book_length}")
        # print(f"Target Age: {target_age}")
        # print(f"Dimension: {dimension}\n")
        book_data = {
        "title": book['title'],
        "price": price if price_element else "Price not found",
        "description": description if description_element else "Description not found",
        "book_length": book_length if book_length else "Book length not found",
        "target_age": target_age if target_age else "Target age not found",
        "dimension": dimension if dimension else "Dimension not found"
    }
    books_data.append(book_data)
        
with open('child_books.json', 'w', encoding='utf-8') as f:
    json.dump(books_data, f, ensure_ascii=False, indent=4)

driver.quit()
