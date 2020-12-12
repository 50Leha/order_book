"""Main class for Order Book project"""

import copy
from typing import Dict, List, Union


class OrderBook:
    """Describes an order book data type"""

    offer_id: int = 0

    asks: dict = {}
    bids: dict = {}

    def __init__(self, depth: int = 20):
        """
        Init a new order book.

        :param depth: size of order book. Default value: 20
        :type: Integer
        """
        self.depth = depth

    def add_offer(self, trade_type: str, price: Union[int, float], quantity: int) -> Union[int, str]:
        """
        Add offer in the order book.

        :param trade_type: a type of trade, where the offer will be placed. Available trade types: ask, bid
        :type: String

        :param price: offer price
        :type: [Integer, Float]

        :param quantity: amount of lots
        :type: Integer

        :return: offer id or None
        :rtype: [Integer, String]
        """
        if type(price) not in {int, float}:
            return 'price must be integer or float'

        elif type(quantity) != int:
            return 'quantity must be integer'

        market_lot = {
            'price': price,
            'quantity': quantity,
        }

        if trade_type == 'ask':

            if len(self.asks) == self.depth:
                return 'asks list is overflowed'

            else:
                self.offer_id += 1
                self.asks[self.offer_id] = market_lot

                return self.offer_id

        elif trade_type == 'bid':

            if len(self.bids) == self.depth:
                return 'bids list is overflowed'

            else:
                self.offer_id += 1
                self.bids[self.offer_id] = market_lot

                return self.offer_id

        else:
            return 'trade_type must be "ask" or "bid"'

    def purge_offer(self, item_id: int) -> Union[None, str]:
        """
        Purge offer from the order book by its id

        :param item_id: offer id
        :type: Integer

        :return: None or error message.
        :rtype: [None, String]
        """
        if type(item_id) != int:
            return f'item_id must be integer'

        if item_id in self.asks.keys():
            self.asks.pop(item_id)

        elif item_id in self.bids.keys():
            self.bids.pop(item_id)

        else:
            return f'There is no offer with id={item_id}'

    def get_offers_data(self, item_id) -> Dict[str, Union[int, float]]:
        """
        Return data of one offer from the order book.

        :param item_id: offer id
        :type: Integer
        """
        if type(item_id) != int:
            return f'item_id must be integer'

        if item_id in self.asks.keys():
            return self.asks.get(item_id)

        elif item_id in self.bids.keys():
            return self.bids.get(item_id)

        else:
            return f'There is no offer with id={item_id}'

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
            'asks': sorted_asks_lots,
            'bids': sorted_bids_lots,
        }

        return market_snapshot
