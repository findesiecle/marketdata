import itertools

from decimal import Decimal
from typing import List, NamedTuple

from sortedcontainers import SortedDict

from .basic_types import Market, Offer


_offer_token_id = itertools.count()

class OfferToken(NamedTuple):
    """Token for an offer in the order book.

    The token uniquely represents one offer placed in the order book. As
    such, it is used to query the order book about this offer: e.g. to
    cancel or to find its position.

    The token is also designed to be sortable on price and maintain
    insertion order.

    Note that the imposed sorting order differs between bid and ask
    offers, always placing the "most attractive" offers at the start. 

    Attrs:
        price: Price of the offer. Negative for bid offers, because a
            high price is favourable and should thus be sorted to the
            start.
        time: Sequence number of the time the offer was added to the
            order book.
    """
    price: Decimal
    time: int

    def __new__(cls, offer: Offer) -> 'OfferToken':
        """Creates a token for an offer.

        Args:
            time: A sequence number reflecting insertion order.
            offer: The offer this token will represent.

        Returns:
            A token for the offer.
        """
        price = -offer.price if offer.is_bid else offer.price

        # https://stackoverflow.com/a/3474156
        return cls.__bases__[0].__new__(cls, price, next(_offer_token_id))

    @property
    def is_bid(self) -> bool:
        """Flag for the offer type: True for bids, False for asks."""
        return self.price < 0


class Orderbook:
    """A limit order book with bids and asks for base and counter currency.
    
    Attrs:
        asks: All listed offers to sell base for counter currency,
            sorted by price in descending order. The implementation uses
            a SortedDict that maps from OfferToken to Offer.
        bids: All listed offers to buy base for counter currency, sorted
            by price in ascending order. Like for asks, the
            implementation uses a SortedDict.
        market: Offers listed in an orderbook trade base currency
            against counter currency. This currency pair is the market.
        tick: A generator of monotonically increasing numbers.
    """

    def __init__(self, market: Market) -> None:
        """Creates an empty order book.
        
        Args:
            market: Provides the currency (asset) pair for trade.
        """
        self.market = market

        self.asks = SortedDict()
        self.bids = SortedDict()

    def clear(self) -> None:
        """Removes all offers from the order book."""
        self.asks.clear()
        self.bids.clear()

    def add(self, offer: Offer) -> OfferToken:
        """Adds an offer to the order book.
        
        Depending on the offer, it is added to the asks or bids.
        
        Args:
            offer: Offer to be added.
        
        Returns:
            An offer token to identify the offer uniquely within this
            order book. Make sure to keep hold of this token for things
            like cancelling and updating the order, or to look up its
            position.
        """
        token = OfferToken(offer)

        if offer.is_bid:
            self.bids[token] = offer
        else:
            self.asks[token] = offer

        return token

    def add_many(self, offers: List[Offer]) -> List[OfferToken]:
        """Adds multiple offers to the order book.
        
        Args:
            offers: A list of offers to be placed in the order book.
        
        Returns:
            A list of tokens, one for each offer (in the same order).
        """
        tokens = list()     # List[OfferToken]

        asks = list()       # List[Tuple[OfferToken,Offer]]
        bids = list()

        for offer in offers:
            token = OfferToken(offer)

            tokens.append(token)

            if offer.is_bid:
                bids.append((token, offer))
            else:
                asks.append((token, offer))

        self.asks.update(asks)
        self.bids.update(bids)

        return tokens

    def remove(self, token: OfferToken):
        """Removes an open offer from the order book.
        
        Args:
            token: An offer token.
        
        Raises:
            KeyError if the token/offer is not in the order book.
        """
        if token.is_bid:
            del self.bids[token]
        else:
            del self.asks[token]
