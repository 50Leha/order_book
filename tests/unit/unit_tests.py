import pytest

from order_book.depth_of_market import OrderBook


def test_add_ask_offers():
    book = OrderBook()
    a = book.add_offer('ask', 34, 45)

    assert isinstance(a, int)
    assert a > 0
    assert a == 1

    b = book.add_offer('bid', 45, 56)

    assert isinstance(b, int)
    assert b > 0
    assert b == 2
