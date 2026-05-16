# Pirate Restaurant Django DRF

Цей проєкт — Django сайт з REST API для піратського ресторану.

## Запуск у Docker

1. Зібрати й запустити контейнери:

```bash
docker-compose up --build -d
```

2. Перевірити, що контейнери запущені:

```bash
docker-compose ps
```

3. Перейти у браузері:

- http://localhost:8000/ — головна сторінка
- http://localhost:8000/api/menu/ — REST API для `MenuItem`

## Міграції

Docker Compose уже виконує міграції при старті сервісу `web`.
Якщо треба зробити це вручну:

```bash
docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate
```

## Налаштування бази даних

База даних PostgreSQL налаштована через змінні оточення у `docker-compose.yml`:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DATABASE_URL`

Django читає `DATABASE_URL` і використовує значення цих змінних для підключення.

## Перевірка збереження даних після перезапуску

1. Створити тестовий об'єкт або запис у базі:

```bash
docker-compose exec web python manage.py shell -c "from main.models import MenuItem; MenuItem.objects.create(name='restart-test', description='check', price='10.00'); print(MenuItem.objects.filter(name='restart-test').count())"
```

2. Перезапустити контейнери:

```bash
docker-compose restart db web
```

3. Перевірити, що запис зберігся:

```bash
docker-compose exec web python manage.py shell -c "from main.models import MenuItem; print(MenuItem.objects.filter(name='restart-test').exists())"
```

Якщо повертається `True`, дані зберігаються у `postgres_data` і не зникають після перезапуску.

## REST API та Swagger

Після запуску сервісу `web` доступні REST API та Swagger UI:

- Swagger UI: http://localhost:8000/swagger/
- OpenAPI (JSON): http://localhost:8000/swagger.json
- Redoc: http://localhost:8000/redoc/

Приклади endpoint-ів:

- GET /api/menu/ — список пунктів меню (200)
- GET /api/menu/{id}/ — деталі пункту меню (200 / 404)
- GET /api/specials/ — список спеціальних страв (200)
- GET /api/categories/ — список категорій (200)
- POST /api/reservations/ — створити бронювання (201 / 400 / 401)
- POST /api/reservations/{id}/confirm/ — підтвердити бронювання (200 / 401 / 404)

Авторизація

API використовує JWT через `djangorestframework-simplejwt`.

Отримати токен:

```bash
# Отримати access/refresh
curl -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"admin","password":"pirate123"}'
```

Приклад створення бронювання (використовуючи отриманий `access` токен):

```bash
curl -X POST http://localhost:8000/api/reservations/ \
	-H "Authorization: Bearer <ACCESS_TOKEN>" \
	-H "Content-Type: application/json" \
	-d '{"name":"Ivan","email":"ivan@example.com","phone":"+380501112233","guests_count":4,"reservation_date":"2026-06-01T19:00:00Z","special_requests":"Window seat"}'
```

Приклад отримання спеціальних страв:

```bash
curl http://localhost:8000/api/specials/
```

Якщо потрібно встановити пакети локально (не через Docker):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
