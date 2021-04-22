import argparse
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
    parser.add_argument('start_id', type=int, default=1, help='Start book id')
    parser.add_argument('stop_id', type=int, default=10, help='Stop book id')

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


def download_tululu_book(id):

    book_html = get_tululu_book_html(id)

    if book_html:
        book = parse_book_page(book_html)

        text_filename = f'{id}. {book["title"]}.txt'
        download_txt(get_tululu_book_text_url(id), text_filename)

        download_img(book['img_url'], get_filename_from_url(book['img_url']))


def get_tululu_book_text_url(id):
    download_path = f'txt.php?id={id}'
    return urljoin(TULULU_BASE_URL, download_path)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_tululu_book_html(id):
    book_page_path = f'b{id}'
    url = urljoin(TULULU_BASE_URL, book_page_path)

    response = requests.get(url, verify=False)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return

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


def download_txt(url, filename, folder='books/'):
    '''Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    '''
    response = requests.get(url, verify=False)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return

    sanitized_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitized_filename)

    with open(filepath, 'w') as file:
        file.write(response.text)

    return filepath


def download_img(url, filename, folder='img/'):
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

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        print(f'Img {filename} not found')
        return

    sanitized_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitized_filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    mkdir(BOOKS_DIR, IMAGES_DIR)

    start_id, stop_id = fetch_from_to_parameters()

    for id in range(start_id, stop_id + 1):
        download_tululu_book(id)


if __name__ == '__main__':
    main()