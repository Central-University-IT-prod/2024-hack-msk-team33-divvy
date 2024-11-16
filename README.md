# Divvy

Divvy — приложение для учета и распределения общих расходов среди друзей, коллег и других групп. Помогает отслеживать расходы, управлять долгами и гарантировать, что каждый участник оплачивает свою долю.

## Структура проекта

Проект состоит из трех основных папок:

- database  
  Содержит схемы и миграции для базы данных.

- web app  
  Веб-приложение для управления группами, расходами и просмотра информации.

- tg bot  
  Telegram-бот для авторизации, отправки уведомлений и взаимодействия с пользователями.

## Использование

1. Авторизуйтесь через Telegram.
2. Создайте группу или присоединитесь к существующей.
3. Добавляйте расходы и следите за балансом долгов.
4. Завершите группу для финальной расплаты и взаимозачета долгов.


## Запуск backend
- Запуск всего проекта в докер-контейнере
- Запускаем всё на 127.0.0.1:8011
1. Билдим контейнер: 
```docker build . -t backend-prod```
2. Запускаем контейнер:
```docker run --env-file .env backend-prod```
- Требуется создать .env:
```
POSTGRES_USER={{sensitive_data}}
POSTGRES_PASSWORD={{sensitive_data}}
POSTGRES_DB={{sensitive_data}}
POSTGRES_HOST={{sensitive_data}}
POSTGRES_PORT={{sensitive_data}}
SECRET_KEY={{sensitive_data}}
ALGORITHM_DECODE=HS256
```

# Запуск всего проекта
## Запуск:
- FrontEnd - localhost:8091
- BackEnd - localhost:8011
- Postgres - :5432
1. Склонить FrontEnd:
 - ```git submodule add https://{{sensitive_data}}/prod-team-33/diwy_frontend frontend```
2. Прописать .env:
```
POSTGRES_USER={{sensitive_data}}
POSTGRES_PASSWORD={{sensitive_data}}
POSTGRES_DB={{sensitive_data}}
POSTGRES_HOST={{sensitive_data}}
POSTGRES_PORT={{sensitive_data}}
SECRET_KEY={{sensitive_data}}
ALGORITHM_DECODE=HS256
BOT_TOKEN={{sensitive_data}}
```
3. Запустить docker-compose:
- ```docker-compose up --build -d``` - в фоне
- ```docker-compose up --build``` - в терминале