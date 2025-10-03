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

    # Инициализация базы (при старте dev, если нужно)
    Base.metadata.create_all(bind=engine)  # для prod используем Alembic!

    # Регистрация роутов
    # from .api import register_routes
    app.register_blueprint(orders_bp)

    return app
