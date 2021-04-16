import requests
import urllib3
from pathlib import Path

BOOKS_DIR = 'books/'


def download_tululu_book(id):
    url = 'https://tululu.org/txt.php'
    params = {'id': id}

    print(f'Downloading {id}...')

    response = requests.get(url, params=params, verify=False)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        print(f'Book {id} not found')
        return

    file_path = f'{BOOKS_DIR}id{id}.txt'
    with open(file_path, 'w') as file:
        file.write(response.text)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    Path(BOOKS_DIR).mkdir(parents=True, exist_ok=True)

    for id in range(1, 10 + 1):
        download_tululu_book(id)


if __name__ == '__main__':
    main()
