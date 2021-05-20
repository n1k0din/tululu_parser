import json
import os
from functools import partial
from math import ceil


from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

PAGES_DIR = 'pages'


def fix_path_sep_to_posix(books_metadata: list[dict[str, str]]):
    if os.sep == '\\':
        for book in books_metadata:
            book['txt_path'] = book['txt_path'].replace('\\', '/')
            book['img_path'] = book['img_path'].replace('\\', '/')


def build_index(books, dir='.', set_size=10, columns_amount=2):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    pages_amount = ceil(len(books) / set_size)
    filename_temlate = 'index{}.html'
    for num, books_set in enumerate(chunked(books, set_size), start=1):

        rendered_page = template.render(
            current_page=num,
            pages_amount=pages_amount,
            books=chunked(books_set, columns_amount),
        )
        filename = filename_temlate.format(num)
        full_path = os.path.join(dir, filename)

        with open(full_path, 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    os.makedirs(PAGES_DIR, exist_ok=True)
    with open('sci_fi_books.json') as f:
        books_metadata = json.load(f)

    fix_path_sep_to_posix(books_metadata)

    rebuild = partial(build_index, books=books_metadata, dir=PAGES_DIR)

    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')


if __name__ == '__main__':
    main()
