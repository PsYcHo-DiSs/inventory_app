import os

from dotenv import load_dotenv

load_dotenv()

def str_to_bool(value: str | None) -> bool:
    """
    Конвертирует строку в булево значение.
    Считаются True: 'true', '1', 'yes', 'on' (регистр не важен).
    Иначе False.
    """
    if value is None:
        return False
    return value.lower() in ('true', '1', 'yes', 'on')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = str_to_bool(os.getenv('SQLALCHEMY_ECHO'))
    DEBUG = str_to_bool(os.getenv('FLASK_DEBUG'))
