import os.path
import requests
import urllib3
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

BOOKS_DIR = 'books/'


def download_tululu_book(id):
    url = get_tululu_book_text_url(id)

    author_title = get_author_title_tululu_book(id)

    if author_title:
        author, title = author_title
        filename = f'{id}. {title}.txt'
        download_txt(url, filename)


def get_tululu_book_text_url(id):
    url = 'https://tululu.org/'
    download_path = f'txt.php?id={id}'
    return urllib.parse.urljoin(url, download_path)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_author_title_tululu_book(id):
    url = f'https://tululu.org/b{id}/'

    response = requests.get(url, verify=False)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        print(f'Book page {id} not found')
        return None

    soup = BeautifulSoup(response.text, 'lxml')

    author_title = soup.find('div', id='content').find('h1').text

    title, author = [name.strip() for name in author_title.split('::')]

    return author, title


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(url, verify=False)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        print(f'Book txt for {filename} not found')
        return

    sanitized_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitized_filename)

    with open(filepath, 'w') as file:
        file.write(response.text)

    return filepath


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    Path(BOOKS_DIR).mkdir(parents=True, exist_ok=True)

    for id in range(1, 10 + 1):
        download_tululu_book(id)


if __name__ == '__main__':
    main()
