import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def fix_path_sep_to_posix(books_metadata: list[dict[str, str]]):
    if os.sep == '\\':
        for book in books_metadata:
            book['txt_path'] = book['txt_path'].replace('\\', '/')
            book['img_path'] = book['img_path'].replace('\\', '/')


def main():
    with open('sci_fi_books.json') as f:
        books_metadata = json.load(f)

    fix_path_sep_to_posix(books_metadata)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        books=books_metadata,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 80), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
