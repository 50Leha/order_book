"""Module for Order Book projects exceptions"""


class InvalidDepthException(Exception):
    pass


class ParamTypeException(Exception):
    pass


class ParamValueException(Exception):
    pass


class NoElementException(Exception):
    pass


class TradeTypeOverflowedException(Exception):
    pass
