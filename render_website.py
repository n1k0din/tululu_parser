import json
import os
from functools import partial


from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def fix_path_sep_to_posix(books_metadata: list[dict[str, str]]):
    if os.sep == '\\':
        for book in books_metadata:
            book['txt_path'] = book['txt_path'].replace('\\', '/')
            book['img_path'] = book['img_path'].replace('\\', '/')


def build_index(books):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)


def main():
    with open('sci_fi_books.json') as f:
        books_metadata = json.load(f)

    fix_path_sep_to_posix(books_metadata)

    rebuild = partial(build_index, books=books_metadata)

    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')


if __name__ == '__main__':
    main()
