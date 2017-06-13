from abc import ABCMeta, abstractmethod
from typing import Dict, List

from .basic_types import Balance, Currency, Market, Trade
from .orderbook import Orderbook


class ExchangeInterface(metaclass=ABCMeta):
    name: str

    @abstractmethod
    def markets(self) -> List[Market]:
        raise NotImplementedError()

    @abstractmethod
    def trades(self, market: Market) -> List[Trade]:
        raise NotImplementedError()

    @abstractmethod
    def orderbook(self, market: Market) -> Orderbook:
        raise NotImplementedError()

    @abstractmethod
    def balances(self) -> Dict[Currency, Balance]:
        raise NotImplementedError()
