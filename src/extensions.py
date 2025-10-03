from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Config
from .models import Base  # импортируем Base с нашими моделями

# движок
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    echo=Config.SQLALCHEMY_ECHO,
    future=True
)

# сессия
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)