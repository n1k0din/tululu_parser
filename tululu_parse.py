import argparse
import logging
import os.path
import urllib3
from pathlib import Path
from urllib.parse import urljoin, unquote, urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

BOOKS_DIR = 'books/'
IMAGES_DIR = 'img/'
TULULU_BASE_URL = 'https://tululu.org/'


def mkdir(*args):
    for dir_name in args:
        Path(dir_name).mkdir(parents=True, exist_ok=True)


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Download books from tululu.org')
    parser.add_argument('start_id', type=int, help='Start book id')
    parser.add_argument('stop_id', type=int, help='Stop book id')

    return parser


def fetch_from_to_parameters():
    arg_parser = create_argument_parser()
    args = arg_parser.parse_args()

    return args.start_id, args.stop_id


def get_filename_from_url(file_url):
    unquoted_url = unquote(file_url)
    _, _, path, _, _ = urlsplit(unquoted_url)
    _, filename = os.path.split(path)

    return filename


def download_tululu_book(book_id):
    book_html = get_tululu_book_html(book_id)

    if book_html:
        book = parse_book_page(book_html)

        text_filename = f'{book_id}. {book["title"]}.txt'

        logging.info(f'Downloading {book_id}: {book["title"]}...')

        book_txt_url, url_params = get_tululu_book_text_url(book_id)

        download_txt(book_txt_url, text_filename, BOOKS_DIR, params=url_params)

        download_img(book['img_url'], get_filename_from_url(book['img_url']), IMAGES_DIR)


def get_tululu_book_text_url(book_id):
    download_path = 'txt.php'
    params = {'id': book_id}
    url = urljoin(TULULU_BASE_URL, download_path)
    return url, params


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_tululu_book_html(id):
    book_page_path = f'b{id}/'
    url = urljoin(TULULU_BASE_URL, book_page_path)

    response = requests.get(url, verify=False)
    response.raise_for_status()

    check_for_redirect(response)

    return response.text


def parse_book_page(html):
    soup = BeautifulSoup(html, 'lxml')

    author_title = soup.find('div', id='content').find('h1').text

    img_src = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(TULULU_BASE_URL, img_src)

    title, author = [name.strip() for name in author_title.split('::')]

    comments_tags = soup.find_all('div', class_='texts')

    comments = [comment.find('span').text for comment in comments_tags]

    genre_tags = soup.find('span', class_='d_book').find_all('a')
    genres = [genre_tag.text for genre_tag in genre_tags]

    return {
        'author': author,
        'title': title,
        'img_url': img_url,
        'comments': comments,
        'genres': genres,
    }


def download_txt(url, filename, folder, params=None):
    '''Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    '''
    response = requests.get(url, params=params, verify=False)
    response.raise_for_status()

    check_for_redirect(response)

    sanitized_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitized_filename)

    with open(filepath, 'w') as file:
        file.write(response.text)

    return filepath


def download_img(url, filename, folder):
    '''Функция для скачивания изображений.
    Args:
        url (str): Cсылка на изображение, которое хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранено изображение.
    '''
    response = requests.get(url, verify=False)
    response.raise_for_status()

    check_for_redirect(response)

    sanitized_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitized_filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logging.basicConfig(
        filename='tululu_parse.log',
        format='%(asctime)s %(message)s',
        encoding='utf-8',
        level=logging.INFO
    )

    mkdir(BOOKS_DIR, IMAGES_DIR)

    start_id, stop_id = fetch_from_to_parameters()

    for book_id in range(start_id, stop_id + 1):
        try:
            download_tululu_book(book_id)
        except requests.HTTPError:
            logging.warning(f'Book {book_id} not found, skipping...')


if __name__ == '__main__':
    main()
