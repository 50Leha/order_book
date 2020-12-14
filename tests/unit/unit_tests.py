from random import randint
from typing import Callable, NoReturn

import pytest

from order_book.depth_of_market import OrderBook
from order_book.exceptions import (
    InvalidDepthException, ParamTypeException, ParamValueException, NoElementException, TradeTypeOverflowedException,
)


def test_create_default_book(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Create new order book with default depth param
    """
    book = new_order_book

    assert book.depth == 20
    assert book.offer_id == 0

    assert not book.asks
    assert not book.bids


def test_create_custom_book() -> NoReturn:
    """
    Create new order book with custom depth param
    """
    book_size = randint(1, 10)
    book = OrderBook(book_size)

    assert book.depth == book_size
    assert book.offer_id == 0

    assert not book.asks
    assert not book.bids


def test_create_book_zero_depth() -> NoReturn:
    """
    Create new order book with zero depth
    """
    with pytest.raises(InvalidDepthException):
        book = OrderBook(0)


def test_create_book_negative_depth() -> NoReturn:
    """
    Create new order book with negative depth
    """
    with pytest.raises(InvalidDepthException):
        book = OrderBook(-1)


def test_add_offer_ask_trade_type(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer into asks
    """
    book = new_order_book

    trade_type = 'asks'
    price = 1
    quantity = 1

    book.add_offer(trade_type, price, quantity)

    assert book.offer_id == 1
    assert book.asks[book.offer_id - 1]['price'] == price
    assert book.asks[book.offer_id - 1]['quantity'] == quantity

    assert not book.bids


def test_add_offer_bid_trade_type(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer into bids
    """
    book = new_order_book

    trade_type = 'bids'
    price = 1
    quantity = 1

    book.add_offer(trade_type, price, quantity)

    assert book.offer_id == 1
    assert book.bids[book.offer_id - 1]['price'] == price
    assert book.bids[book.offer_id - 1]['quantity'] == quantity

    assert not book.asks


def test_add_offer_invalid_trade_type(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer into invalid trade type
    """
    book = new_order_book

    trade_type = 'foo'
    price = 1
    quantity = 1

    with pytest.raises(ParamValueException):
        book.add_offer(trade_type, price, quantity)


def test_add_offer_missing_trade_type(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    """
    book = new_order_book

    price = 1
    quantity = 1

    with pytest.raises(ParamValueException):
        book.add_offer(price=price, quantity=quantity)



def test_add_offer_float_price(new_order_book: Callable[[], OrderBook]):
    """
    """


def test_add_offer_negative_price(new_order_book: Callable[[], OrderBook]):
    """
    """


def test_add_offer_zero_price(new_order_book: Callable[[], OrderBook]):
    """
    """


def test_add_offer_missing_price(new_order_book: Callable[[], OrderBook]):
    """
    """


def test_add_offer_invalid_price(new_order_book: Callable[[], OrderBook]):
    """
    """


def test_add_offer_int_quantity(new_order_book: Callable[[], OrderBook]):
    """
    """


def test_add_offer_negative_quantity(new_order_book: Callable[[], OrderBook]):
    """
    """


def test_add_offer_zero_quantity(new_order_book: Callable[[], OrderBook]):
    """
    """


def test_add_offer_missing_quantity(new_order_book: Callable[[], OrderBook]):
    """
    """


def test_add_offer_invalid_quantity(new_order_book: Callable[[], OrderBook]):
    """
    """







def test_purge_offer_positive() -> NoReturn:
    """
    """


def test_purge_offer_invalid_item_id() -> NoReturn:
    """
    """


def test_purge_offer_missing_item() -> NoReturn:
    """
    """


def test_purge_offer_no_item_id() -> NoReturn:
    """
    """














def test_get_offers_data_ask():
    """
    """


def test_get_offers_data_bid():
    """
    """


def test_get_offers_data_invalid_item_id():
    """
    """


def test_get_offers_data_missing_item():
    """
    """


def test_get_offers_data_no_item_id():
    """
    """








def test_get_market_snapshot_both_trade_types():
    """
    """


def test_get_market_snapshot_asks_only():
    """
    """


def test_get_market_snapshot_bids_only():
    """
    """


def test_get_market_snapshot_empty():
    """
    """
