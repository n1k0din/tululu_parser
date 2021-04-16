import requests
import urllib3


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    url = "https://tululu.org/txt.php?id=32168"

    response = requests.get(url, verify=False)
    response.raise_for_status()

    filename = 'book.txt'
    with open(filename, 'w') as file:
        file.write(response.text)


if __name__ == '__main__':
    main()
