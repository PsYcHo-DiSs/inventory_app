import os

from flask import Flask
from flasgger import Swagger

from .config import Config
from .extensions import engine
from .models import Base
from .api import orders_bp

def create_app():
    """
    Создает Flask-приложение, подключает БД, Swagger, регистрирует маршруты.
    """

    app = Flask(__name__)
    app.config.from_object(Config)

    # Swagger API
    Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Order API",
            "description": "API для управления заказами и продуктами",
            "version": "1.0"
        },
        "basePath": "/"
    })

    env = os.getenv('FLASK_ENV', 'development')

    # Инициализация базы
    if env == 'development':
        # Локальная разработка - быстрое создание таблиц
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created via SQLAlchemy (dev mode)")
    elif env == 'production':
        # Продакшн (Docker) - миграции уже применены в CMD
        print("✅ Running in production mode (Alembic migrations applied)")

    # Регистрация роутов
    app.register_blueprint(orders_bp)

    return app
