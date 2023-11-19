import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor

base_url = "https://www.yes24.com/24/Category/Display/001001005004"

def get_book_info(goods_no):
    url = f"http://www.yes24.com/Product/Goods/{goods_no}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    description_section = soup.find('textarea', class_='txtContentText')
    description = description_section.get_text(strip=True) if description_section else "No description found"
    return description

def get_page_data(page_number):
    url = f'{base_url}?PageNumber={page_number}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    page_data = []
    for book_section in soup.find_all('li', {'data-goods-no': True}):
        title_element = book_section.find('img', alt=True)
        price_section = book_section.find('div', class_='goods_price')
        if title_element and price_section:
            title = title_element.get('alt')
            price = price_section.get_text(strip=True).split('원')[0]
            goods_no = book_section.get('data-goods-no')
            page_data.append((title, price, goods_no))

    return page_data

def save_to_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

all_books_data = []

for page_number in range(1, 434):
    page_books = get_page_data(page_number)
    all_books_data.extend(page_books)
    print(f"Page {page_number} done")

# 병렬로 책 설명을 요청하여 시간 단축
with ThreadPoolExecutor() as executor:
    goods_nos = [book[2] for book in all_books_data]
    book_descriptions = list(executor.map(get_book_info, goods_nos))

# 모든 정보를 하나의 리스트에 결합
books_data = [{"title": book[0], "price": book[1], "description": desc} for book, desc in zip(all_books_data, book_descriptions)]

# 최종 결과를 JSON 파일로 저장
save_to_json('books_data_complete.json', books_data)
print("All data processed and saved")
