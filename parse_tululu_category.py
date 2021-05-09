import json
import logging
import urllib3
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import tululu_parse


def parse_book_ids_from_category_page(html):
    soup = BeautifulSoup(html, 'lxml')

    book_cards = soup.select('#content .d_book > :nth-child(2) a')

    book_hrefs = (a['href'] for a in book_cards)

    yield from (book_id.strip('/').lstrip('b') for book_id in book_hrefs)


def get_sci_fi_book_ids(page_from=1, page_to=10):
    url_template = 'https://tululu.org/l55/{}'

    for page_num in range(page_from, page_to + 1):
        url = url_template.format(page_num)
        response = requests.get(url, verify=False)
        response.raise_for_status()

        yield from parse_book_ids_from_category_page(response.text)


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    logging.basicConfig(
        filename='tululu_category_parse.log',
        format='%(asctime)s %(message)s',
        encoding='utf-8',
        level=logging.INFO
    )

    Path(tululu_parse.BOOKS_DIR).mkdir(parents=True, exist_ok=True)
    Path(tululu_parse.IMAGES_DIR).mkdir(parents=True, exist_ok=True)

    metadata_filename = "sci_fi_books.json"

    with open(metadata_filename, 'w') as f:
        pass

    books = []
    for book_id in get_sci_fi_book_ids(1, 4):
        try:
            book = tululu_parse.download_tululu_book(book_id)
            books.append(book)
            with open(metadata_filename, "a+") as f:
                json.dump(books, f, ensure_ascii=False)

        except requests.HTTPError:
            logging.warning(f'Book {book_id} not found, skipping...')


if __name__ == '__main__':
    main()
