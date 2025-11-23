# Library API

## Настройка

### Перейти в папку backend и создать .env файл:

```shell
    cd backend    
    cp .env.example .env
```

Обязательно заполните значения DB_PASSWORD, DB_USER, DB_NAME для подключения к бд. Остальные значения менять или заполнять по желанию

## Запуск

### Перейти в папку .deploy и запустить докер:

```shell
    cd ../.deploy    
    docker compose up -d
```
