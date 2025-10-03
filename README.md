# Решение тестового задания

## Предполагаемая структура проекта

```
inventory_app/
├─ src/
│  ├─ api/
│  │  ├─ __init__.py
│  │  └─ orders.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ category.py
│  │  ├─ client.py
│  │  ├─ order.py
│  │  ├─ order_item.py 
│  │  └─ product.py
│  ├─ services/
│  │  ├─ ...
│  │
│  ├─ __init__.py
│  ├─ app.py
│  ├─ config.py
│  └─ extensions.py
├─ .env
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ README.md
```
## Инициация контейнера с базой postgres
```bash
docker run --name postgres-flask_orders -e POSTGRES_PASSWORD=123456 -e POSTGRES_DB=flask_orders -d -p 5440:5432 postgres:latest
```