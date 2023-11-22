import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor

# 서브 카테고리 링크 추출

main_url = "https://www.yes24.com/24/Category/Display/001001016001"
file_name = "어린이문학"

def get_subcategory_links(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    subcategory_links = []

    cateSubListWrap = soup.find('div', id='cateSubListWrap')
    if cateSubListWrap:
        for link in cateSubListWrap.find_all('a', href=True):
            full_link = f"http://www.yes24.com{link['href']}"
            subcategory_links.append(full_link)
    
    return subcategory_links

def crawl_category(category_url):
    all_books_data = []
    page_number = 1

    while True:
        page_books = get_page_data(page_number, category_url)
        if page_books is None:
            break

        all_books_data.extend(page_books)
        print(f"Page {page_number} in {category_url} done")
        page_number += 1
    with ThreadPoolExecutor() as executor:
        goods_nos = [book[2] for book in all_books_data]
        book_descriptions = list(executor.map(get_book_info, goods_nos))

    return [{"title": book[0], "price": book[1], "description": desc} for book, desc in zip(all_books_data, book_descriptions)]

def get_book_info(goods_no):
    url = f"http://www.yes24.com/Product/Goods/{goods_no}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 책 설명 추출
    description_section = soup.find('textarea', class_='txtContentText')
    description = description_section.get_text(strip=True) if description_section else "No description found"

    # 품목정보 추출
    infoset_specific = soup.find('div', id='infoset_specific')
    item_info = {}
    if infoset_specific:
        for tr in infoset_specific.find_all('tr'):
            th = tr.find('th').get_text(strip=True)
            td = tr.find('td').get_text(strip=True)
            item_info[th] = td

    return {
        'description': description,
        'item_info': item_info
    }

def get_page_data(page_number, category_url):
    url = f'{category_url}?PageNumber={page_number}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 페이지에 책 목록이 존재하는지 확인
    book_list = soup.find_all('li', {'data-goods-no': True})
    if not book_list:
        return None  # 책 목록이 없으면 None 반환

    page_data = []
    for book_section in book_list:
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

subcategory_urls = get_subcategory_links(main_url)
all_data = []
for sub_url in subcategory_urls:
    category_data = crawl_category(sub_url)
    all_data.extend(category_data)

# 최종 결과를 JSON 파일로 저장
print('Saving data to json file...')
save_to_json(file_name, all_data)
print("All data processed and saved")
