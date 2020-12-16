"""Module with unit tests for order_book_proj"""
from random import randint, choice
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


def test_create_two_books() -> NoReturn:
    """
    Create two different order book at once
    """
    book1 = OrderBook(10)
    book2 = OrderBook(15)

    assert book1.depth == 10
    assert book2.depth == 15

    assert book1.offer_id == 0
    assert book2.offer_id == 0

    assert not book1.asks
    assert not book1.bids

    assert not book2.asks
    assert not book2.bids


def test_add_offer_ask_trade_type(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer into asks
    """
    book = new_order_book

    trade_type = 'asks'
    price = 1
    quantity = 1

    item_id = book.add_offer(trade_type, price, quantity)

    assert book.offer_id == 1
    assert book.offer_id == item_id

    assert book.asks[book.offer_id]['price'] == price
    assert book.asks[book.offer_id]['quantity'] == quantity

    assert not book.bids


def test_add_offer_bid_trade_type(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer into bids
    """
    book = new_order_book

    trade_type = 'bids'
    price = 1
    quantity = 1

    item_id = book.add_offer(trade_type, price, quantity)

    assert book.offer_id == 1
    assert book.offer_id == item_id

    assert book.bids[book.offer_id]['price'] == price
    assert book.bids[book.offer_id]['quantity'] == quantity

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
    Add new offer without trade type
    """
    book = new_order_book

    price = 1
    quantity = 1

    with pytest.raises(ParamValueException):
        book.add_offer(price=price, quantity=quantity)


def test_add_offer_float_price(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer with price float-type
    """
    book = new_order_book

    trade_type = 'asks'
    price = 1.25
    quantity = 1

    item_id = book.add_offer(trade_type, price, quantity)

    assert book.offer_id == 1
    assert book.offer_id == item_id

    assert book.asks[book.offer_id]['price'] == price
    assert book.asks[book.offer_id]['quantity'] == quantity

    assert not book.bids


def test_add_offer_negative_price(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer with negative price
    """
    book = new_order_book

    trade_type = choice(['asks', 'bids'])
    price = -1
    quantity = 1

    with pytest.raises(ParamValueException):
        book.add_offer(trade_type, price, quantity)


def test_add_offer_zero_price(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer with zero price
    """
    book = new_order_book

    trade_type = choice(['asks', 'bids'])
    price = 0
    quantity = 1

    with pytest.raises(ParamValueException):
        book.add_offer(trade_type, price, quantity)


def test_add_offer_missing_price(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer without price
    """
    book = new_order_book

    trade_type = choice(['asks', 'bids'])
    quantity = 1

    with pytest.raises(ParamTypeException):
        book.add_offer(trade_type=trade_type, quantity=quantity)


def test_add_offer_invalid_price(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer with invalid price (not int or float type)
    """
    book = new_order_book

    trade_type = choice(['asks', 'bids'])
    price = '1'
    quantity = 1

    with pytest.raises(ParamTypeException):
        book.add_offer(trade_type, price, quantity)


def test_add_offer_float_quantity(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer with float quantity
    """
    book = new_order_book

    trade_type = choice(['asks', 'bids'])
    price = 1
    quantity = 1.5

    with pytest.raises(ParamTypeException):
        book.add_offer(trade_type, price, quantity)


def test_add_offer_negative_quantity(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer with negative quantity
    """
    book = new_order_book

    trade_type = choice(['asks', 'bids'])
    price = 1
    quantity = -1

    with pytest.raises(ParamValueException):
        book.add_offer(trade_type, price, quantity)


def test_add_offer_zero_quantity(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer with zero quantity
    """
    book = new_order_book

    trade_type = choice(['asks', 'bids'])
    price = 1
    quantity = 0

    with pytest.raises(ParamValueException):
        book.add_offer(trade_type, price, quantity)


def test_add_offer_missing_quantity(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer without quantity
    """
    book = new_order_book

    trade_type = choice(['asks', 'bids'])
    price = 1

    with pytest.raises(ParamTypeException):
        book.add_offer(trade_type=trade_type, price=price)


def test_add_offer_invalid_quantity(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add new offer with invalid quantity (not int type)
    """
    book = new_order_book

    trade_type = choice(['asks', 'bids'])
    price = 1
    quantity = 'kek'

    with pytest.raises(ParamTypeException):
        book.add_offer(trade_type, price, quantity)


def test_purge_ask_offer(order_book_with_ask_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Purge offer from asks
    """
    book = order_book_with_ask_offer

    deleted_item = book.purge_offer(book.offer_id - 1)

    assert isinstance(deleted_item, dict)

    assert not book.asks
    assert not book.bids

    assert book.offer_id == 1


def test_purge_bid_offer(order_book_with_bid_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Purge offer from bids
    """
    book = order_book_with_bid_offer

    deleted_item = book.purge_offer(book.offer_id - 1)

    assert isinstance(deleted_item, dict)

    assert not book.bids
    assert not book.asks

    assert book.offer_id == 1


def test_purge_offer_invalid_item_id(order_book_with_ask_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Purge offer with invalid id
    """
    book = order_book_with_ask_offer

    with pytest.raises(ParamTypeException):
        deleted_item = book.purge_offer('1')


def test_purge_offer_wrong_item_id(order_book_with_bid_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Purge offer with wrong id param
    """
    book = order_book_with_bid_offer

    with pytest.raises(NoElementException):
        deleted_item = book.purge_offer(100500)


def test_purge_offer_without_item_id(order_book_with_ask_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Purge offer with no id param
    """
    book = order_book_with_ask_offer

    with pytest.raises(ParamTypeException):
        deleted_item = book.purge_offer()


def test_get_offers_data_ask(order_book_with_ask_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Get ask offer from order book
    """
    book = order_book_with_ask_offer

    received_item = book.get_offers_data(book.offer_id -1)

    assert isinstance(received_item, dict)
    assert received_item['price'] == 1
    assert received_item['quantity'] == 1

    assert book.asks
    assert not book.bids
    assert book.offer_id == 1


def test_get_offers_data_bid(order_book_with_bid_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Get bid offer from order book
    """
    book = order_book_with_bid_offer

    received_item = book.get_offers_data(book.offer_id -1)

    assert isinstance(received_item, dict)
    assert received_item['price'] == 1
    assert received_item['quantity'] == 1

    assert book.bids
    assert not book.asks
    assert book.offer_id == 1


def test_get_offers_data_invalid_item_id(order_book_with_bid_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Get offer via invalid id
    """
    book = order_book_with_bid_offer

    with pytest.raises(ParamTypeException):
        received_item = book.get_offers_data('0')


def test_get_offers_data_missing_item(order_book_with_ask_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Get missing offer
    """
    book = order_book_with_ask_offer

    with pytest.raises(NoElementException):
        received_item = book.get_offers_data(100500)


def test_get_offers_data_no_item_id(order_book_with_ask_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Get offer with no id
    """
    book = order_book_with_ask_offer

    with pytest.raises(ParamTypeException):
        received_item = book.get_offers_data()


def test_get_market_snapshot_both_trade_types(order_book_with_both_offers: Callable[[], OrderBook]) -> NoReturn:
    """
    Get snapshot with asks and bids data
    """
    book = order_book_with_both_offers

    market_snapshot = book.get_market_snapshot()

    assert isinstance(market_snapshot['asks'], list)
    assert isinstance(market_snapshot['asks'][0], dict)
    assert market_snapshot['asks'][0]['price'] == 1
    assert market_snapshot['asks'][0]['quantity'] == 1

    assert isinstance(market_snapshot['bids'], list)
    assert isinstance(market_snapshot['bids'][0], dict)
    assert market_snapshot['bids'][0]['price'] == 2
    assert market_snapshot['bids'][0]['quantity'] == 2

    assert book.asks
    assert book.bids
    assert book.offer_id == 2


def test_get_market_snapshot_asks_only(order_book_with_ask_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Get snapshot with only asks data
    """
    book = order_book_with_ask_offer

    market_snapshot = book.get_market_snapshot()
    assert isinstance(market_snapshot, dict)

    assert isinstance(market_snapshot['asks'], list)
    assert isinstance(market_snapshot['asks'][0], dict)
    assert market_snapshot['asks'][0]['price'] == 1
    assert market_snapshot['asks'][0]['quantity'] == 1

    assert not market_snapshot['bids']
    assert isinstance(market_snapshot['bids'], list)

    assert book.asks
    assert not book.bids
    assert book.offer_id == 1


def test_get_market_snapshot_bids_only(order_book_with_bid_offer: Callable[[], OrderBook]) -> NoReturn:
    """
    Get snapshot with only bids data
    """
    book = order_book_with_bid_offer

    market_snapshot = book.get_market_snapshot()
    assert isinstance(market_snapshot, dict)

    assert isinstance(market_snapshot['bids'], list)
    assert isinstance(market_snapshot['bids'][0], dict)
    assert market_snapshot['bids'][0]['price'] == 1
    assert market_snapshot['bids'][0]['quantity'] == 1

    assert not market_snapshot['asks']
    assert isinstance(market_snapshot['asks'], list)

    assert book.bids
    assert not book.asks
    assert book.offer_id == 1


def test_get_market_snapshot_empty(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Get empty snapshot
    """
    book = new_order_book

    market_snapshot = book.get_market_snapshot()
    assert isinstance(market_snapshot, dict)

    assert not market_snapshot['asks']
    assert isinstance(market_snapshot['asks'], list)

    assert not market_snapshot['bids']
    assert isinstance(market_snapshot['bids'], list)

    assert not book.bids
    assert not book.asks
    assert book.offer_id == 0
