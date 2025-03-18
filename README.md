# notes_fastapi

Менеджер заметок

# Структура

```
notes_app/
├── main.py          # Точка входа
├── database.py      # Подключение к БД
├── models.py        # SQLAlchemy-модели
├── schemas.py       # Pydantic-схемы
└── routers/         # Роутеры
    └── notes.py     # Эндпоинты для заметок
```

# Запуск

docker-compose build
docker-compose up
