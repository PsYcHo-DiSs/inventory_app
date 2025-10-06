import pytest
from src.services import (OrderService,
                          OrderNotFoundError,
                          ProductNotFoundError,
                          OutOfStockError)

from src.models import OrderItem


class FakeProduct:
    def __init__(self, id, name, stock, price):
        self.id = id
        self.name = name
        self.stock = stock
        self.price = price


class FakeOrder:
    def __init__(self, id):
        self.id = id


class FakeOrderItem(OrderItem):
    def __init__(self, order_id, product_id, quantity, unit_price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.id = None


class FakeOrderRepo:
    def __init__(self, orders):
        self.orders = orders

    def get_for_update(self, id):
        return self.orders.get(id)


class FakeProductRepo:
    def __init__(self, products):
        self.products = products

    def get_for_update(self, id):
        return self.products.get(id)

    def save(self, product):
        self.products[product.id] = product


class FakeItemRepo:
    def __init__(self):
        self.items = {}

    def get_by_order_and_product(self, order_id, product_id):
        return self.items.get((order_id, product_id))

    def add(self, item):
        self.items[(item.order_id, item.product_id)] = item

    def save(self, item):
        self.items[(item.order_id, item.product_id)] = item


class FakeUnitOfWork:
    def __init__(self):
        # имитация данных в памяти
        self.orders = {1: FakeOrder(1)}
        self.products = {1: FakeProduct(1, "TV", stock=10, price=1000)}
        self.order_repo = FakeOrderRepo(self.orders)
        self.product_repo = FakeProductRepo(self.products)
        self.item_repo = FakeItemRepo()
        self.committed = False
        self.session = self

    def flush(self):
        pass

    def commit(self):
        self.committed = True


def test_add_new_item_creates_order_item():
    """Если товара нет в заказе — создаётся новая позиция, уменьшается stock"""
    uow = FakeUnitOfWork()
    service = OrderService(uow)

    item = service.add_item(order_id=1, product_id=1, quantity=2)

    assert item.quantity == 2
    assert uow.products[1].stock == 8
    assert (1, 1) in uow.item_repo.items


def test_add_item_increases_existing_quantity():
    """Если товар уже есть — увеличивается количество"""
    uow = FakeUnitOfWork()
    service = OrderService(uow)

    # создаём уже существующий item
    existing_item = FakeOrderItem(1, 1, 2, 1000)
    uow.item_repo.add(existing_item)

    service.add_item(order_id=1, product_id=1, quantity=3)

    assert uow.item_repo.items[(1, 1)].quantity == 5
    assert uow.products[1].stock == 7  # 10 - 3


def test_raises_if_order_not_found():
    """Если заказ не найден -> OrderNotFoundError"""
    uow = FakeUnitOfWork()
    uow.orders = {}  # нет заказов
    service = OrderService(uow)

    with pytest.raises(OrderNotFoundError):
        service.add_item(order_id=99, product_id=1, quantity=1)


def test_raises_if_product_not_found():
    """Если товар не найден -> ProductNotFoundError"""
    uow = FakeUnitOfWork()
    uow.products = {}  # нет товаров
    service = OrderService(uow)

    with pytest.raises(ProductNotFoundError):
        service.add_item(order_id=1, product_id=99, quantity=1)


def test_raises_if_not_enough_stock():
    """Если недостаточно имеющегося количества -> OutOfStockError"""
    uow = FakeUnitOfWork()
    uow.products[1].stock = 1  # мало на складе
    service = OrderService(uow)

    with pytest.raises(OutOfStockError):
        service.add_item(order_id=1, product_id=1, quantity=5)