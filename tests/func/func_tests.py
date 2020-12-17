"""Module with functional tests for OrderBook"""
from random import randint, choice
from typing import Callable, NoReturn

import pytest

from order_book.depth_of_market import OrderBook
from order_book.exceptions import NoElementException, TradeTypeOverflowedException


def test_overflow_asks_market_default_depth(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Try to add one more lot when default asks market is overflowed
    """
    book = new_order_book

    for _ in range(book.depth):
        book.add_offer('asks', 1, 1)

    assert book.depth == len(book.asks)
    assert not book.bids

    # try to put 21th lot into asks
    with pytest.raises(TradeTypeOverflowedException):
        book.add_offer('asks', 1, 1)


def test_overflow_asks_market_custom_depth() -> NoReturn:
    """
    Try to add one more lot when custom asks market is overflowed
    """
    book = OrderBook(10)

    for _ in range(book.depth):
        book.add_offer('asks', 1, 1)

    assert book.depth == len(book.asks)
    assert not book.bids

    # try to put 11th lot into asks
    with pytest.raises(TradeTypeOverflowedException):
        book.add_offer('asks', 1, 1)


def test_overflow_bids_market_default_depth(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Try to add one more lot when bids market is overflowed
    """
    book = new_order_book

    for _ in range(book.depth):
        book.add_offer('bids', 1, 1)

    assert book.depth == len(book.bids)
    assert not book.asks

    # try to put 21th lot into bids
    with pytest.raises(TradeTypeOverflowedException):
        book.add_offer('bids', 1, 1)


def test_overflow_bids_market_custom_depth() -> NoReturn:
    """
    Try to add one more lot when custom bids market is overflowed
    """
    book = OrderBook(10)

    for _ in range(book.depth):
        book.add_offer('bids', 1, 1)

    assert book.depth == len(book.bids)
    assert not book.asks

    # try to put 11th lot into bids
    with pytest.raises(TradeTypeOverflowedException):
        book.add_offer('bids', 1, 1)


def test_purge_offer_ask(filled_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Purge ask offer and check, that it`s gone
    """
    book = filled_order_book

    ask_keys = list(book.asks.keys())
    offer_key = choice(ask_keys)

    purged_order = book.purge_offer(offer_key)

    assert isinstance(purged_order, dict)

    assert len(book.asks) == book.depth - 1
    assert len(book.bids) == book.depth

    try:
        price = purged_order['price']
        quantity = purged_order['quantity']

    except KeyError:
        pytest.fail('While parsing purged_offer KeyError occured')

    assert isinstance(price, int)
    assert price > 0

    assert isinstance(quantity, int)
    assert quantity > 0

    ask_keys = list(book.asks.keys())
    assert offer_key not in ask_keys

    with pytest.raises(NoElementException):
        book.get_offers_data(offer_key)


def test_purge_offer_bid(filled_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Purge bid offer and check, that it`s gone
    """
    book = filled_order_book

    bid_keys = list(book.bids.keys())
    offer_key = choice(bid_keys)

    purged_offer = book.purge_offer(offer_key)

    assert isinstance(purged_offer, dict)

    assert len(book.bids) == book.depth - 1
    assert len(book.asks) == book.depth

    try:
        price = purged_offer['price']
        quantity = purged_offer['quantity']

    except KeyError:
        pytest.fail('While parsing purged_offer KeyError occured')

    assert isinstance(price, int)
    assert price > 0

    assert isinstance(quantity, int)
    assert quantity > 0

    bid_keys = list(book.bids.keys())
    assert offer_key not in bid_keys

    with pytest.raises(NoElementException):
        book.get_offers_data(offer_key)


def test_add_purge_ask_offer(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add ask offer and purge it
    """
    book = new_order_book

    price = randint(10, 100)
    quantity = randint(100, 200)

    offer_id = book.add_offer('asks', price, quantity)

    purged_offer = book.purge_offer(offer_id)

    try:
        offer_price = purged_offer['price']
        offer_quantity = purged_offer['quantity']

    except KeyError:
        pytest.fail('While parsing purged_offer KeyError occured')

    assert offer_price == price
    assert offer_quantity == quantity

    with pytest.raises(NoElementException):
        book.get_offers_data(offer_id)


def test_add_purge_bid_offer(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add bid offer and purge it
    """
    book = new_order_book

    price = randint(10, 100)
    quantity = randint(100, 200)

    offer_id = book.add_offer('bids', price, quantity)

    purged_offer = book.purge_offer(offer_id)

    try:
        offer_price = purged_offer['price']
        offer_quantity = purged_offer['quantity']

    except KeyError:
        pytest.fail('While parsing purged_offer KeyError occured')

    assert offer_price == price
    assert offer_quantity == quantity

    with pytest.raises(NoElementException):
        book.get_offers_data(offer_id)


def test_get_ask_offer_data(filled_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Get ask offer data from filled order book
    """
    book = filled_order_book

    ask_keys = list(book.asks.keys())
    offer_key = choice(ask_keys)

    received_offer = book.get_offers_data(offer_key)

    assert isinstance(received_offer, dict)

    try:
        offer_price = received_offer['price']
        offer_quantity = received_offer['quantity']

    except KeyError:
        pytest.fail('While parsing received_offer KeyError occured')

    assert isinstance(offer_price, int)
    assert isinstance(offer_quantity, int)

    try:
        ask_offer = book.asks[offer_key]

    except KeyError:
        pytest.fail('While parsing book.asks KeyError occured')

    assert ask_offer == received_offer

    with pytest.raises(TradeTypeOverflowedException):
        book.add_offer('asks', 1, 1)


def test_get_bid_offer_data(filled_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Get bid offer data from filled order book
    """
    book = filled_order_book

    bid_keys = list(book.bids.keys())
    offer_key = choice(bid_keys)

    received_offer = book.get_offers_data(offer_key)

    assert isinstance(received_offer, dict)

    try:
        offer_price = received_offer['price']
        offer_quantity = received_offer['quantity']

    except KeyError:
        pytest.fail('While parsing received_offer KeyError occured')

    assert isinstance(offer_price, int)
    assert isinstance(offer_quantity, int)

    try:
        bid_offer = book.bids[offer_key]

    except KeyError:
        pytest.fail('While parsing book.bids KeyError occured')

    assert bid_offer == received_offer

    with pytest.raises(TradeTypeOverflowedException):
        book.add_offer('bids', 1, 1)


def test_add_get_purge_ask_offer(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add ask offer, get and purge it
    """
    book = new_order_book

    price = randint(10, 100)
    quantity = randint(100, 200)

    offer_id = book.add_offer('asks', price, quantity)

    received_offer = book.get_offers_data(offer_id)

    try:
        offer_price = received_offer['price']
        offer_quantity = received_offer['quantity']

    except KeyError:
        pytest.fail('While parsing received_offer KeyError occured')

    assert offer_price == price
    assert offer_quantity == quantity

    assert len(book.asks) == 1
    assert not book.bids

    purged_offer = book.purge_offer(offer_id)

    assert received_offer == purged_offer


def test_add_get_purge_bid_offer(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Add bid offer, get and purge it
    """
    book = new_order_book

    price = randint(10, 100)
    quantity = randint(100, 200)

    offer_id = book.add_offer('bids', price, quantity)

    received_offer = book.get_offers_data(offer_id)

    try:
        offer_price = received_offer['price']
        offer_quantity = received_offer['quantity']

    except KeyError:
        pytest.fail('While parsing received_offer KeyError occured')

    assert offer_price == price
    assert offer_quantity == quantity

    assert len(book.bids) == 1
    assert not book.asks

    purged_offer = book.purge_offer(offer_id)

    assert received_offer == purged_offer


def test_get_market_snapshot(filled_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    Get market snapshot and check, that offers are ordered by price
    """
    book = filled_order_book

    snapshot = book.get_market_snapshot()

    assert len(snapshot['asks']) == book.depth
    assert len(snapshot['bids']) == book.depth

    asks_prices = [ask['price'] for ask in snapshot['asks']]
    sorted_asks_prices = sorted(asks_prices)
    assert asks_prices == sorted_asks_prices

    bids_prices = [bid['price'] for bid in snapshot['bids']]
    sorted_bids_prices = sorted(bids_prices)
    assert bids_prices == sorted_bids_prices
