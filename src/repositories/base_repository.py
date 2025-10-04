from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar("T")

class BaseRepository(Generic[T]):
    """Базовый репозиторий с CRUD-операциями."""

    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get(self, id_: int) -> T | None:
        return self.session.get(self.model, id_)

    def get_for_update(self, id_: int) -> T | None:
        stmt = select(self.model).where(self.model.id == id_).with_for_update()
        return self.session.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[T]:
        stmt = select(self.model)
        return self.session.scalars(stmt).all()

    def add(self, obj: T) -> T:
        self.session.add(obj)
        return obj

    def delete(self, obj: T):
        self.session.delete(obj)

    def save(self, obj: T) -> T:
        self.session.add(obj)
        self.session.flush()
        return obj