# Flask Игра "Угадай число"

Веб-приложение на Flask, в котором пользователи угадывают случайное число от 1 до 1000. Результаты и имена игроков сохраняются в базе данных PostgreSQL.

## Возможности

- Регистрация и вход по имени пользователя (без пароля)
- Сохранение лучших результатов для каждого игрока
- Ведение истории игр в базе данных
- Простой и понятный интерфейс

## Требования

- Python 3.7+
- PostgreSQL
- pip

## Установка

1. Клонируйте репозиторий или скопируйте файлы проекта.

2. Установите зависимости:
   ```bash
   pip install flask psycopg2
   ```

3. Создайте базу данных PostgreSQL и необходимые таблицы. Пример SQL-скрипта:
   ```sql
   CREATE DATABASE project1_db;
   \c project1_db

   CREATE TABLE players (
       user_id SERIAL PRIMARY KEY,
       username VARCHAR(100) UNIQUE NOT NULL
   );

   CREATE TABLE games (
       game_id SERIAL PRIMARY KEY,
       user_id INTEGER REFERENCES players(user_id),
       number_of_guesses INTEGER NOT NULL,
       secret_number INTEGER NOT NULL
   );
   ```

4. Проверьте настройки подключения к базе данных в файле `my_flask.py`:
   ```python
   conn = psycopg2.connect(
       host='localhost',
       database='project1_db',
       user='postgres',
       password='Qaszplkm1'
   )
   ```

5. Запустите приложение:
   ```bash
   python my_flask.py
   ```

6. Откройте браузер и перейдите по адресу:  
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Структура проекта

- `my_flask.py` — основной файл приложения Flask
- `templates/` — HTML-шаблоны (index.html, game.html)
- `freecode/`, `project 1/` — дополнительные материалы и скрипты

## Использование

1. Введите имя пользователя на главной странице.
2. Угадывайте число от 1 до 1000, вводя свои варианты.
3. После победы результат сохранится в базе, и вы увидите свой лучший результат.

## Примечания

- Пароль и параметры подключения к базе указаны в коде для примера. Для продакшена используйте переменные окружения!
- Для запуска на сервере используйте WSGI-сервер (например, gunicorn). 