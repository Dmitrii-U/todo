1. клонировать репозиторий
2. создать виртуальное окружение
3. установить зависимости проекта(описаны в pyproject.toml):
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
6. API регистрации/подтверждения/восстановления пароля:
   - _создание пользователя:_
      ```bash
      curl --location 'http://0.0.0.0:8000/api/auth/user/create/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
         "username": <username>,
         "password": <password>,
         "email": <email>
      }'
      ```
      В результате в БД создается пользователь в статусе не верифицирован. 
На email пользователя(в дев режиме email рассылка выводится в консоль) будет 
отправлено письмо со ссылкой подтверждения регистрации. Для верификации 
пользователя - перейти по ссылке или отправить GET запрос:
   - _верификация пользователя:_
      ```bash
      curl --location 'http://0.0.0.0:8000/api/auth/verify/<verification_code>/'
      ```
   - _восстановление пароля:_
      запросить восстановление пароля для пользователя по username:
      ```bash
      curl --location 'http://0.0.0.0:8000/api/auth/pass-recovery/<username>/'
      ```
      В результате будет сформирован и отправлен на email(в консоль в dev режиме)
 код подтверждения для сброса пароля.
      Для установления нового пароля отправить **PATCH** запрос:
      ```bash
      curl --location --request PATCH 'http://0.0.0.0:8000/api/auth/pass-recovery/<username>/' \
      --header 'Content-Type: application/json' \
      --data '{
         "verification_code": "<verification_code>",
         "password": "<password>"
      }'
      ```
