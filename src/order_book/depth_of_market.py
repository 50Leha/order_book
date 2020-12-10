"""Main class for Order Book project"""


from typing import Dict, Union


class OrderBook:
    """Describes an order book data type"""

    self.offer_id = 0

    self.asks = {}
    self.bids = {}

    def __init__(self, depth: int = 20):
        """
        Init a new order book.

        :param depth: size of order book. Default value: 20
        :type: Integer
        """
        self.depth = depth

    def add_offer(self, trade_type: str, price: int, quantity: int) -> Union[int, None]:
        """
        Add offer in the order book.

        :param trade_type: a type of trade, where the offer will be placed. Available trade types: ask, bid
        :type: String

        :param price: offer price
        :type: Integer

        :param quantity: amount of lots
        :type: Integer

        :return: offer id or None
        :rtype: [Integer, None]
        """
        temp_val = {
            'price': price,
            'quantity': quantity,
        }

        if trade_type == 'ask':

            if len(asks) == self.depth:
                return None

            else:
                self.offer_id += 1
                self.asks[self.offer_id] = temp_val

                return self.offer_id

        elif trade_type == 'bid':

            if len(bids) == self.depth:
                return None

            else:
                self.offer_id += 1
                self.bids[self.offer_id] = temp_val

                return self.offer_id

        else:
            return None

    def purge_offer(self, item_id: int) -> Union[None, str]:
        """
        Purge offer from the order book by its id

        :param item_id: offer id
        :type: Integer

        :return: None or error message.
        :rtype: [None, String]
        """
        try:
            asks.pop(item_id)

        except KeyError:
            bids.pop(item_id)

        except KeyError:
            return f'There is no offer with id={item_id}'

    def get_offers_data(seld, item_id) -> Dict[str, int]:
        """
        Return data of one offer from the order book.

        :param item_id: offer id
        :type: Integer
        """
        pass

    def get_markets_spanshot(self):
        """Returns snapshot of market at the current time"""
        pass


    '''
    {
        "asks": [
            {
                "price": <value>,
                "quantity": <value>
            },
        ],
        "bids": [...]
    }