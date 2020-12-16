from random import randint

import pytest

from order_book.depth_of_market import OrderBook


@pytest.fixture
def new_order_book() -> OrderBook:
    """
    Common fixture
    Create new order book

    :return: new object of OrderBook
    :rtype: OrderBook
    """
    order_book = OrderBook()

    yield order_book


@pytest.fixture
def order_book_with_ask_offer() -> OrderBook:
    """
    Unit fixture
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
    Unit fixture
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
    Unit fixture
    Create new order book and put into new ask and bid offers
    """
    order_book = OrderBook()

    order_book.asks[0] = {'price': 1, 'quantity': 1}
    order_book.bids[0] = {'price': 2, 'quantity': 2}
    order_book.offer_id = 2

    yield order_book


@pytest.fixture
def filled_order_book(new_order_book) -> OrderBook:
    """
    Functional fixture
    Create new order book and fill it up with new ask and bid offers
    """
    book = new_order_book

    for _ in range(book.depth):
        book.add_offer('asks', randint(10, 50), randint(100, 200))
        book.add_offer('bids', randint(10, 50), randint(100, 200))

    yield book
