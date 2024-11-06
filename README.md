# Polygon Project

## Описание
Polygon Project - это веб-приложение для создания, управления и визуализации географических полигонов. Приложение позволяет пользователям создавать полигоны как через интерактивную карту, так и путем ручного ввода координат.

## Технологии
- **Backend:**
  - Django 5.1.3
  - Django REST Framework
  - PostGIS/PostgreSQL
  - GeoDjango
- **Frontend:**
  - Leaflet.js (для интерактивных карт)
  - Bootstrap 5.2.3
  - jQuery 3.6.0
- **Инфраструктура:**
  - Docker
  - Docker Compose
  - Nginx
  - Gunicorn

## Особенности
- Интерактивная карта для создания и просмотра полигонов
- Автоматическое определение пересечения антимеридиана
- Нормализация координат полигонов
- REST API для управления полигонами
- Поддержка PostgreSQL с расширением PostGIS
- Контейнеризация с помощью Docker

## Установка и запуск

### Предварительные требования
- Docker
- Docker Compose
- Git

### Установка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/1CyanidE1/polygon_project.git
cd polygon_project
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Настройте переменные окружения в `.env`:
```env
# Django settings
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_ENGINE=django.contrib.gis.db.backends.postgis
DB_NAME=polygon_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432

# pgAdmin settings
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin

# Web settings
WEB_PORT=8000
NGINX_PORT=80

# Static and media files
STATIC_URL=/static/
MEDIA_URL=/media/
```

4. Сборка и запуск контейнеров:
```bash
docker-compose up --build -d
```

5. Создание и применение миграций:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Запуск
После установки приложение будет доступно по адресу:
- Веб-интерфейс: http://localhost
- API: http://localhost/api/
- pgAdmin: http://localhost:5050

## API Endpoints

### Полигоны
- `GET /api/polygons/` - получить список всех полигонов
- `POST /api/polygons/` - создать новый полигон
- `GET /api/polygons/{id}/` - получить полигона по id
- `PUT /api/polygons/{id}/` - обновить полигон
- `DELETE /api/polygons/{id}/` - удалить полигон

### Формат данных

#### Создание полигона (POST /api/polygons/)
```json
{
    "name": "Example Polygon",
    "polygon": {
        "type": "Polygon",
        "coordinates": [
            [
                [longitude1, latitude1],
                [longitude2, latitude2],
                [longitude3, latitude3],
                [longitude1, latitude1]
            ]
        ]
    }
}
```

#### Ответ
```json
{
    "id": 1,
    "name": "Example Polygon",
    "polygon": {
        "type": "Polygon",
        "coordinates": [[...]]
    },
    "crosses_antimeridian": false
}
```

## Структура проекта
```
polygon_project/
├── docker/
│   ├── django/
│   │   └── Dockerfile
│   ├── nginx/
│   │   └── Dockerfile
│   └── pgadmin/
│       └── Dockerfile
├── polygon_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   
├── polygon_project/
│   ├── settings.py
│   └── urls.py
├── templates/
│       └── polygon_app/
│           └── index.html
├── nginx.conf
├── .env.example
├── docker-compose.yml
└── requirements.txt
```

## Обработка антимеридиана
Приложение автоматически определяет и обрабатывает случаи пересечения полигоном антимеридиана. Это происходит в следующих случаях:
1. Когда разница между долготами двух последовательных точек превышает 180 градусов
2. Когда точки находятся по разные стороны от антимеридиана
3. Когда общий диапазон долгот полигона превышает 180 градусов

## Разработка
При разработке рекомендуется использовать:
- Python 3.11 или выше
- Node.js 14 или выше (для frontend разработки)
- PostgreSQL 15 с PostGIS 3.3

## Автор
Слабиков Иван

## Поддержка
Telegram - https://t.me/Sl_ivan

## TODO
- Добавить аутентификацию пользователей
- Реализовать возможность экспорта/импорта полигонов
- Добавить поддержку других форматов геоданных
- Улучшить визуализацию полигонов на карте
- Добавить валидацию геометрии полигонов
