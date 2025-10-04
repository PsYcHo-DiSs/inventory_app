from contextlib import AbstractContextManager
from src.extensions import SessionLocal
from src.repositories import OrderRepository, OrderItemRepository, ProductRepository


class SqlAlchemyUnitOfWork(AbstractContextManager):
    """Unit of Work — управляет транзакцией и хранит репозитории."""

    def __init__(self):
        self.session = SessionLocal()
        self.order_repo = OrderRepository(self.session)
        self.product_repo = ProductRepository(self.session)
        self.item_repo = OrderItemRepository(self.session)

    def __enter__(self):
        self.tx = self.session.begin()
        self.tx.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
