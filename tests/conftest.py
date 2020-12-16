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


@pytest.fixture
def order_book_with_ask_offer() -> OrderBook:
    """
    Create new order book and fill it up with new ask offer

    :return: new object of OrderBook
    :rtype: OrderBook
    """
    order_book = OrderBook()

    order_book.asks[0] = {'price': 1, 'quantity': 1}
    order_book.offer_id = 1

    yield order_book


@pytest.fixture
def order_book_with_bid_offer() -> OrderBook:
    """
    Create new order book and fill it up with new bid offer

    :return: new object of OrderBook
    :rtype: OrderBook
    """
    order_book = OrderBook()

    order_book.bids[0] = {'price': 1, 'quantity': 1}
    order_book.offer_id = 1

    yield order_book


@pytest.fixture
def order_book_with_both_offers() -> OrderBook:
    """
    Create new order book and fill it up with new ask and bid offers
    """
    order_book = OrderBook()

    order_book.asks[0] = {'price': 1, 'quantity': 1}
    order_book.bids[0] = {'price': 2, 'quantity': 2}
    order_book.offer_id = 2

    yield order_book
