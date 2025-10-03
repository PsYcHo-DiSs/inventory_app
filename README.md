## Предполагаемая структура проекта

inventory_app/
├─ app/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ db.py
│  ├─ models.py
│  ├─ services.py
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ orders.py
│  │  └─ products.py   (optional)
│  └─ cli.py
├─ migrations/   (alembic) -- описано в README
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ README.md
