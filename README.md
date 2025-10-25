# Deskbook API preparation
![python](https://img.shields.io/static/v1?label=Python&message=3.10&color=<COLOR>)
![FastAPI](https://img.shields.io/static/v1?label=FastAPI&message=0.119.0&color=<COLOR>)
![pydantic](https://img.shields.io/static/v1?label=pydantic&message=2.12.3&color=<COLOR>)
![sqlalchemy](https://img.shields.io/static/v1?label=SQLalchemy&message=2.0.44&color=<COLOR>)
![GeoAlchemy2](https://img.shields.io/static/v1?label=GeoAlchemy2&message=0.18.0&color=<COLOR>)
![alembic](https://img.shields.io/static/v1?label=alembic&message=1.17.0&color=<COLOR>)

Для запуска контейнера базы данных используй
```bash
docker compose up -d dev_db
```

После запуска базы данных необходимо загрузить дамп
```bash
source .env
psql -U $DB_USER -h localhost -p 15432 postgres < app/dumps/init.sql 
(Пароль для БД: "admin")
```

Для запуска контейнера приложения используй
```bash
docker compose up dev_api
```

## Swagger docs
После запуска контейнера апи будет доступно по ссылке:
> http://localhost:8000/docs#/

API-ключ для эндпоинтов
```bash
THIS-FIELD-SHOULD-BE-CHANGED
```