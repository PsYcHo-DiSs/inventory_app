from src.models import OrderItem


class OrderNotFoundError(Exception):
    """Заказ не найден"""
    pass


class ProductNotFoundError(Exception):
    """Товар не найден"""
    pass


class OutOfStockError(Exception):
    """Товара недостаточно на складе"""
    pass


class OrderService:
    """Бизнес-логика заказов (независимая от SQLAlchemy)."""

    def __init__(self, uow):
        self.uow = uow

    def add_item(self, order_id: int, product_id: int, quantity: int) -> OrderItem:
        """
            Добавление товара в заказ.
            Если товар уже есть — увеличиваем количество.
            Если товара нет в наличии — кидаем OutOfStockError.
            Если заказ или товар не найдены — кидаем соответствующие ошибки.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        order = self.uow.order_repo.get_for_update(order_id)
        if not order:
            raise OrderNotFoundError(f"Order {order_id} not found")

        product = self.uow.product_repo.get_for_update(product_id)
        if not product:
            raise ProductNotFoundError(f"Product {product_id} not found")

        if product.stock < quantity:
            raise OutOfStockError(f"Not enough stock for {product.name}")

        item = self.uow.item_repo.get_by_order_and_product(order_id, product_id)
        if item:
            item.quantity += quantity
            self.uow.item_repo.save(item)
        else:
            item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.price,
            )
            self.uow.item_repo.add(item)

        product.stock -= quantity
        self.uow.product_repo.save(product)
        self.uow.session.flush()

        return item
