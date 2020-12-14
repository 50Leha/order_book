import pytest

from order_book.depth_of_market import OrderBook


@pytest.fixture
def new_order_book() -> OrderBook:
    """
    Create new order book

    :return: new object of OrderBook
    :rtype: OrderBook
    """
    order_book = OrderBook()

    yield order_book
