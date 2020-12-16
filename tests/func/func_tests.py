"""Module with functional tests for order_book_proj"""
from random import randint, choice
from typing import Callable, NoReturn

import pytest

from order_book.depth_of_market import OrderBook
from order_book.exceptions import (
    InvalidDepthException, ParamTypeException, ParamValueException, NoElementException, TradeTypeOverflowedException,
)


def test_overflow_asks_market(new_order_book: Callable[[], OrderBook]) -> NoReturn:
    """
    """
    book = new_order_book