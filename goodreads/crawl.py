import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_book_details(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            description_element = soup.find('div', class_='DetailsLayoutRightParagraph')
            if description_element:
                description = description_element.find('span', class_='Formatted').text
                return description
        return None
    except Exception as e:
        print(f"Error fetching details for {link}: {e}")
        return None

def fetch_book_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return [(title_section.get_text(strip=True), site_url + title_section.get('href')) 
                    for title_section in soup.find_all('a', class_='bookTitle')]
        return []
    except Exception as e:
        print(f"Error fetching book links: {e}")
        return []

def fetch_books_from_page(page_num):
    print(f"Fetching books from page {page_num}...")
    url = f"{base_url}?page={page_num}"
    book_links = fetch_book_links(url)
    books_data = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_book_details, link): title for title, link in book_links}
        for future in as_completed(future_to_url):
            title = future_to_url[future]
            description = future.result()
            if description:
                books_data.append({'title': title, 'description': description})
    print(f"Completed fetching books from page {page_num}")
    return books_data

site_url = "https://www.goodreads.com"
base_url = "https://www.goodreads.com/list/show/86.Best_Children_s_Books"

final_books_data = []

with ThreadPoolExecutor(max_workers=5) as page_executor:
    page_futures = {page_executor.submit(fetch_books_from_page, i): i for i in range(1, 52)}
    for future in as_completed(page_futures):
        final_books_data.extend(future.result())
        print(f"Processed page {page_futures[future]}")

# Save to JSON
with open('books_data.json', 'w') as f:
    json.dump(final_books_data, f)
    print("Saved all data to books_data.json")

print("All tasks completed.")
