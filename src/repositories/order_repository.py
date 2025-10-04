from sqlalchemy import select
from src.models import Order
from src.repositories.base_repository import BaseRepository

class OrderRepository(BaseRepository[Order]):
    """Репозиторий для заказов."""

    def __init__(self, session):
        super().__init__(Order, session)

    def get_by_client(self, client_id: int):
        stmt = select(Order).where(Order.client_id == client_id)
        return self.session.scalars(stmt).all()