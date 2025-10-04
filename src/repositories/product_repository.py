from sqlalchemy import select
from src.models import Product
from src.repositories.base_repository import BaseRepository

class ProductRepository(BaseRepository[Product]):
    """Репозиторий для работы с товарами."""

    def __init__(self, session):
        super().__init__(Product, session)

    def get_by_name(self, name: str) -> Product | None:
        stmt = select(Product).where(Product.name == name)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_available(self):
        stmt = select(Product).where(Product.stock > 0)
        return self.session.scalars(stmt).all()