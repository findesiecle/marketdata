from abc import ABCMeta, abstractmethod
from datetime import datetime
from decimal import Decimal
from decimal import getcontext as decimal_getcontext
from typing import NamedTuple

decimal_getcontext().prec = 8


Amount = Decimal
Price = Decimal


class Currency(NamedTuple):
    """A currency (and issuer)."""
    symbol: str
    issuer: str = ''

    def __str__(self):
        template = '{:s}.{:s}' if self.issuer else '{:s}'
        return template.format(*self)


class Balance(NamedTuple):
    """An amount of funds (available)."""
    total: Amount
    available: Amount


class Market(NamedTuple):
    """A currency (asset) pair for trading."""
    base: Currency
    counter: Currency

    def __str__(self):
        return '{!s:s}/{!s:s}'.format(*self)


class Offer(metaclass=ABCMeta):
    # https://stackoverflow.com/a/31439126

    def __init__(self, base_amount: Amount, counter_amount: Amount):
        self.base_amount = Amount(base_amount)
        self.base_remaining = Amount(base_amount)
        self.counter_amount = Amount(counter_amount)
        self.counter_remaining = Amount(counter_amount)

    @property
    @abstractmethod
    def is_bid(self) -> bool:
        raise NotImplementedError('Offer is an abstract class. '
                                  'Use BuyOffer or SellOffer instead.')

    @property
    def price(self) -> Price:
        return self.counter_amount / self.base_amount

    @property
    def price_remaining(self) -> Price:
        return self.counter_remaining / self.base_remaining

    @property
    def is_partial(self) -> bool:
        return self.base_remaining < self.base_amount

    @classmethod
    def from_price(cls, base_amount: Amount, price: Price):
        counter_amount = base_amount * price
        return cls(base_amount, counter_amount)


class BuyOffer(Offer):
    is_bid = True


class SellOffer(Offer):
    is_bid = False


class Trade(NamedTuple):
    """A Trade is an Offer that has been executed."""
    time: datetime
    offer: Offer

    @property
    def is_bid(self) -> bool:
        """Flag for the offer type: True for bids, False for asks."""
        return self.offer.is_bid


class Ticker(NamedTuple):
    time: datetime
    bid: Price
    ask: Price
    last: Price
    volume: Amount
    volume_traded: Amount
    open: Price
    close: Price
    high: Price
    low: Price
