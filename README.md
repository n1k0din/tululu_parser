# Скачивание книг с tululu.org
- `tululu_parse.py` скачивает книги по id c tululu, текст и изображения обложек складывает в books/ и img/, данные о книгах хранит во внутреннем словаре. Пишет логи скачивания в `tululu_parse.log`.

- `parse_tululu_category.py` скачивает [фантастические книги](https://tululu.org/l55/)  по номерам страниц c tululu, текст и изображения обложек складывает в books и img (опционально, можно отключить скачивание) в указанной папке, данные о книгах хранит там же. Пишет логи скачивания в `tululu_category_parse.log`.


## Аргументы
### tululu_parse.py
- `start_id` идентификатор первой книги.
- `stop_id` идентификатор последней книги.

### parse_tululu_category.py
- `--start_page` номер первой страницы.
- `--stop_page` номер последней страницы, по-умолчанию вычисляется последняя существующая.
- `--dest_folder` папка для скачивания, по-умолчанию текущая.
- `--skip_imgs` пропускать скачивание изображений.
- `--skip_txts` пропускать скачивание текста.
- `--json_path` путь к файлу-результату, по-умолчанию `sci_fi_books.json`.

## Пример запуска
- Скачивает книги с идентификатором от 5 до 100 включительно:
  ```bash
  python tululu_parse.py 5 100
  ```

- Скачивает фантастические книги со страницы 5 по страницу 10:
  ```bash
  python parse_tululu_category.py --start_page 5 --stop_page 10
  ```

- Скачивает все фантастические книги, начиная со страницы 690 в папку `download`, пропуская скачивание изображений и текста:
  ```bash
  python parse_tululu_category.py --start_page 690 --skip_txts --dest_folder download
  ```

## Пример результирующего файла
`sci_fi_books.json`
  ```json
  {
    "author": "Мартьянов Андрей",
    "title": "Большая охота",
    "comments": ["Намешал, конечно. И Гизборна сюда приплел и Дункана Маклауда... Но вот же, прилипла, так и не успокоилась пока все книги из этой серии не прочитала. Захватывает. Спасибо.", "Конечно, фантазия у автора очень богатая. И Гизборна сюда приплел и Дункана Маклауда... Но, пока не прочитала все книги из этой серии - не успокоилась. Захватывает."],
    "genres": ["Альтернативная история", "Исторические приключения", "Научная фантастика"],
    "img_path": "download\\img\\59440.jpg"
  }
  {
    "author": "Патрацкая Наталья Владимировна",
    "title": "Деревня Медный ковш",
    "comments": [],
    "genres": ["Научная фантастика", "Прочие приключения", "Современные любовные романы"],
    "img_path": "download\\img\\nopic.gif"
  }
  {
    "author": "Верн Жюль Габриэль",
    "title": "Двадцать тысяч лье под водой",
    "comments": ["ШЕДДЕВР! КТО НЕ ЧИТАЛ - ЧИТАЙТЕ И ДАЙТЕ ПОЧИТАТЬ СВОИМ ДЕТЯМ! ФИЛЬМ-ТУФТА!", "Книга чудесная, фильм слабоват.", "Немного наивная, но добрая и интересная книга. Не могу сказать, что шедевр, но возможно, мы уже просто гонимся за экшном..", "Как бы то не было, но все что было написано мечтами писателя, сейчас все сбылось и человечество до этого упорно и целеустремленно дошло, так что все сбывается...", "Рекомендую любителям фэнтези.", "Я читала эту книгу много раз она мне очень понравилась... Она заинтересовала, заинтриговала меня. Фильм мне не очень понравился. Читайте книги они могут оказаться настолько интересными, что вы не сможете остановится пока не дочитаете. VZ.", "Очень хорошая книга всем рекомендую!!!!!!!!!!!"],
    "genres": ["Морские приключения", "Научная фантастика"],
    "img_path": "download\\img\\59678.jpg"
  }
  ...  
  ```




## Установка

### Подготовка скрипта

1. Скачайте код и перейдите в папку проекта.
    ```bash
    git clone https://github.com/n1k0din/tululu_parser.git
    ```  
    ```bash
    cd tululu_parser
    ```
2. Установите вирт. окружение.
    ```bash
    python -m venv venv
    ```
3. Активируйте.
    ```bash
    venv\Scripts\activate.bat
    ```
    или
    ```bash
    source venv/bin/activate
    ```
4. Установите необходимые пакеты.
    ```bash
    pip install -r requirements.txt
    ```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
