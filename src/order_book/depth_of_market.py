"""Main module for Order Book project"""

from collections import namedtuple
import copy
from typing import Dict, List, Union

from order_book.exceptions import (
    InvalidDepthException, ParamTypeException, ParamValueException, NoElementException, TradeTypeOverflowedException,
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
        ) -> Union[int, str]:
        """
        Add offer in the order book.

        :param trade_type: a type of trade, where the offer will be placed. Available trade types: asks, bids
        :type: String

        :param price: offer price
        :type: [Integer, Float]

        :param quantity: amount of lots
        :type: Integer

        :return: offer id or None
        :rtype: [Integer, String]
        """
        if type(price) not in {int, float}:
            raise ParamTypeException

        elif type(quantity) != int:
            raise ParamTypeException

        if price <= 0:
            raise ParamValueException

        if quantity <= 0:
            raise ParamValueException

        if len(self.asks) == self.depth:
                raise TradeTypeOverflowedException

        if len(self.bids) == self.depth:
                raise TradeTypeOverflowedException

        market_lot = {
            'price': price,
            'quantity': quantity,
        }

        try:
            self.relations[trade_type][self.offer_id] = market_lot
            self.offer_id += 1

            return self.offer_id

        except KeyError:
            raise ParamValueException

    def purge_offer(self, item_id: int = None) -> Union[None, str]:
        """
        Purge offer from the order book by its id

        :param item_id: offer id
        :type: Integer

        :return: None or error message.
        :rtype: [None, String]
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
