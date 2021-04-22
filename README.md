# Скачивание книг с tululu.org
- `tululu_parse.py` скачивает книги по id c tululu, текст и изображения обложек складывает в txt/ и images/, данные о книгах хранит во внутреннем словаре Пишет логи скачивания в `tululu_parse.log`.


## Аргументы
- `start_id` идентификатор первой книги
- `stop_id` идентификатор последней книги

## Пример запуска
Скачивает книги с идентификатором от 5 до 100 включительно:
  ```bash
  python tululu_parse.py 5 100
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
