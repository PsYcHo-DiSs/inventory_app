from sqlalchemy import select
from src.models import OrderItem
from src.repositories.base_repository import BaseRepository

class OrderItemRepository(BaseRepository[OrderItem]):
    """Репозиторий для позиций заказа."""

    def __init__(self, session):
        super().__init__(OrderItem, session)

    def get_by_order_and_product(self, order_id: int, product_id: int) -> OrderItem | None:
        stmt = (
            select(OrderItem)
            .where(OrderItem.order_id == order_id, OrderItem.product_id == product_id)
            .with_for_update()
        )
        return self.session.execute(stmt).scalar_one_or_none()