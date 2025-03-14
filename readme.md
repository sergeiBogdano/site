Django Diving Club Project

Этот проект — сайт для дайв-клуба, разработанный на Django.

Установка и настройка

1. Клонирование репозитория

git clone <URL_РЕПОЗИТОРИЯ>
cd <НАЗВАНИЕ_ПРОЕКТА>

2. Создание и активация виртуального окружения

python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate  # Для Windows

3. Установка зависимостей

pip install -r requirements.txt

4. Применение миграций базы данных

python manage.py migrate

5. Создание суперпользователя

python manage.py createsuperuser

Следуйте инструкциям в терминале для ввода логина, email и пароля.

6. Запуск локального сервера

python manage.py runserver

После этого сайт будет доступен по адресу: http://127.0.0.1:8000/

7. Доступ в админ-панель

Перейдите по адресу http://127.0.0.1:8000/admin/ и войдите с данными суперпользователя.
