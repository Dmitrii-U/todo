1. клонировать репозиторий
2. создать виртуальное окружение
3. установить зависимости проекта:
   ```bash
   poetry install --no-root
   ```  
4. БД - SQLite3. Создается при применении миграций:
   ```bash
   python manage.py migrate
   ```
5. Запуск сервера разработки:
   ```bash
   manage.py runserver 0.0.0.0:8000
   ```
6. API:
   - создание пользователя
      ```bash
      curl --location 'http://0.0.0.0:8000/api/auth/user/create/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
         "username": <username>,
         "password": <password>,
         "email": <email>
      }'
      ```
      в результате в БД создается пользователь в статусе не верифицирован. Для
верификации
   - создание пользователя
      ```bash
      curl --location 'http://0.0.0.0:8000/api/auth/user/create/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
         "username": <username>,
         "password": <password>,
         "email": <email>
      }'
      ```
