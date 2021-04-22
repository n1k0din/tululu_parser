import os.path
import requests
import urllib3
from pathlib import Path
from urllib.parse import urljoin, unquote, urlsplit

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

BOOKS_DIR = 'books/'
IMAGES_DIR = 'img/'


def get_filename(file_url):
    unquoted_url = unquote(file_url)
    _, _, path, _, _ = urlsplit(unquoted_url)
    _, filename = os.path.split(path)

    return filename


def download_tululu_book(id):

    book = get_tululu_book_info(id)

    if book:
        text_url = get_tululu_book_text_url(id)
        text_filename = f'{id}. {book["title"]}.txt'
        # download_txt(text_url, text_filename)
        # download_img(book['img_url'], get_filename(book['img_url']))
        print(*book['comments'], sep='\n')


def get_tululu_book_text_url(id):
    url = 'https://tululu.org/'
    download_path = f'txt.php?id={id}'
    return urljoin(url, download_path)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_tululu_book_info(id):
    url = f'https://tululu.org/b{id}/'

    response = requests.get(url, verify=False)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return None

    soup = BeautifulSoup(response.text, 'lxml')

    try:
        author_title = soup.find('div', id='content').find('h1').text
    except AttributeError:
        print("Can't find title")
        return None

    img_src = soup.find('div', class_='bookimage').find('img')['src']

    title, author = [name.strip() for name in author_title.split('::')]
    img_url = urljoin(url, img_src)

    comments = soup.find_all('div', class_='texts')

    comments_texts = [comment.find('span').text for comment in comments]

    return {
        'author': author,
        'title': title,
        'img_url': img_url,
        'comments': comments_texts,
    }


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
        return None

    sanitized_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitized_filename)

    with open(filepath, 'w') as file:
        file.write(response.text)

    return filepath


def download_img(url, filename, folder='img/'):
    """Функция для скачивания изображений.
    Args:
        url (str): Cсылка на изображение, которое хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранено изображение.
    """
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
    Path(BOOKS_DIR).mkdir(parents=True, exist_ok=True)
    Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)

    for id in range(1, 10 + 1):
        download_tululu_book(id)


if __name__ == '__main__':
    main()
