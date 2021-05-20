import argparse
import json
import logging
import os.path
import urllib3
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import tululu_parse


def fetch_cli_parameters(last_page_num):
    arg_parser = argparse.ArgumentParser(description='Download sci-fi books from tululu.org')
    arg_parser.add_argument('--start_page', type=int, default=1, help='Start page num')
    arg_parser.add_argument('--stop_page', type=int, default=last_page_num, help='Stop page num')
    arg_parser.add_argument('--dest_folder', default='.', help='Download folder')
    arg_parser.add_argument('--skip_imgs', action='store_true', help='Skip cover images download')
    arg_parser.add_argument('--skip_txts', action='store_true', help='Skip book text download')
    arg_parser.add_argument('--json_path', default='sci_fi_books.json', help='Result json path')

    return arg_parser.parse_args()


def parse_book_ids_from_category_page(html):
    soup = BeautifulSoup(html, 'lxml')

    book_cards = soup.select('.d_book > :nth-child(2) a')

    book_hrefs = (a['href'] for a in book_cards)

    yield from (book_id.strip('/').lstrip('b') for book_id in book_hrefs)


def get_last_sci_fi_page_num():
    url = 'https://tululu.org/l55/'

    response = requests.get(url, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    return soup.select('.npage')[-1].text


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

    last_page_num = get_last_sci_fi_page_num()

    args = fetch_cli_parameters(last_page_num)

    download_texts_dir = os.path.join(args.dest_folder, tululu_parse.BOOKS_DIR)
    download_images_dir = os.path.join(args.dest_folder, tululu_parse.IMAGES_DIR)
    Path(download_texts_dir).mkdir(parents=True, exist_ok=True)
    Path(download_images_dir).mkdir(parents=True, exist_ok=True)

    metadata_filename = os.path.join(args.dest_folder, args.json_path)

    books_metadata = []

    for book_id in get_sci_fi_book_ids(args.start_page, args.stop_page + 1):
        try:
            book = tululu_parse.download_tululu_book(
                book_id,
                args.skip_imgs,
                args.skip_txts,
                args.dest_folder,
            )

            books_metadata.append(book)

        except requests.HTTPError:
            logging.warning(f'Book {book_id} not found, skipping...')

    with open(metadata_filename, 'w') as f:
        json.dump(books_metadata, f, ensure_ascii=False)

    logging.info('Done!')


if __name__ == '__main__':
    main()
