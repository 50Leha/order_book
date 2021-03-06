"""
Main module for Order Book project

OrderBook is a simplified order book model. It implements the following methods:

- add_offer - adds a new lot to asks or bids depending on the passed parameters.
Method receives trade type, price and quantity as input.

- purge_offer - removes a lot from the order book.
Receives the id of the lot position, returns the lot object containing
the parameters price, quantity.

- get_offers_data - returns the lot object containing the parameters price, quantity.
Receives the id of the lot position.

- get_market_snapshot - generates a snapshot of asks and bids sorted in ascending order of the lot price.
"""

from collections import namedtuple
import copy
from typing import Dict, List, Union

from order_book.exceptions import (
    InvalidDepthException, ParamTypeException, ParamValueException,
    NoElementException, TradeTypeOverflowedException
)


TradeTypes = namedtuple('TradeType', ['asks', 'bids'])
TradeType = TradeTypes('asks', 'bids')


class OrderBook:
    """Describes an order book data type"""

    def __init__(self, depth: int = 20) -> None:
        """
        Init a new order book.
        If depth is zero or negative - throws InvalidDepthException

        :param depth: size of order book. Default value: 20
        :type: Integer
        """
        if depth <= 0:
            raise InvalidDepthException

        self.depth: int = depth
        self.offer_id : int = 0

        self.asks: dict = {}
        self.bids: dict = {}

        self.relations = {
            TradeType.asks: self.asks,
            TradeType.bids: self.bids
        }

    def add_offer(
        self,
        trade_type: str = None,
        price: Union[int, float] = None,
        quantity: int = None
        ) -> int:
        """
        Add offer in the order book.

        :param trade_type: a type of trade, where the offer will be placed.
        Available trade types: asks, bids
        :type: String

        :param price: offer price
        :type: [Integer, Float]

        :param quantity: amount of lots
        :type: Integer

        :return: offer id
        :rtype: Integer
        """
        if type(price) not in {int, float}:
            raise ParamTypeException

        elif type(quantity) != int:
            raise ParamTypeException

        if price <= 0:
            raise ParamValueException

        if quantity <= 0:
            raise ParamValueException

        try:
            self.relations[trade_type]

        except KeyError:
            raise ParamValueException

        if len(self.relations[trade_type]) == self.depth:
                raise TradeTypeOverflowedException

        market_lot = {
            'price': price,
            'quantity': quantity,
        }

        self.offer_id += 1
        self.relations[trade_type][self.offer_id] = market_lot

        return self.offer_id


    def purge_offer(self, item_id: int = None) -> Dict[str, Union[int, float]]:
        """
        Purge offer from the order book by its id

        :param item_id: offer id
        :type: Integer

        :return: Purged offer
        :rtype: Dictionary
        """
        if type(item_id) != int:
            raise ParamTypeException

        if item_id in self.asks.keys():
            return self.asks.pop(item_id)

        elif item_id in self.bids.keys():
            return self.bids.pop(item_id)

        else:
            raise NoElementException

    def get_offers_data(self, item_id: int = None) -> Dict[str, Union[int, float]]:
        """
        Return data of one offer from the order book.

        :param item_id: offer id
        :type: Integer

        :return: ask or bid offer
        :type: Dictionary
        """
        if type(item_id) != int:
            raise ParamTypeException

        if item_id in self.asks.keys():
            return self.asks.get(item_id)

        elif item_id in self.bids.keys():
            return self.bids.get(item_id)

        else:
            raise NoElementException

    def get_market_snapshot(self) -> Dict[str, List[Dict[str, Union[int, float]]]]:
        """
        Returns snapshot of market at the current time.

        :return: sorted asks and bids lists.
        :rtype: Dictionary
        """
        asks_snapshot = copy.deepcopy(self.asks)
        bids_snapshot = copy.deepcopy(self.bids)

        asks_lots = [lot for lot in asks_snapshot.values()]
        bids_lots = [lot for lot in bids_snapshot.values()]

        sorted_asks_lots = sorted(asks_lots, key=lambda x: x['price'])
        sorted_bids_lots = sorted(bids_lots, key=lambda x: x['price'])

        market_snapshot = {
            TradeType.asks: sorted_asks_lots,
            TradeType.bids: sorted_bids_lots,
        }

        return market_snapshot
