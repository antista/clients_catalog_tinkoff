# task-5

## Описание
Каталог клиентов с аутентификацией, в виде таблицы с возможностью добавления клиента через форму с полями:
* ФИО
* Номер телефона
* Email адрес

### Запуск сервера
* `set FLASK_APP=server.wsgi`
* `flask run`

### Запуск тестов
* `python -m pytest`

### Запуск линтера
* `flake8 server/`