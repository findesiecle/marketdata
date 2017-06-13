from typing import List

from sortedcontainers import SortedListWithKey

from .basic_types import Market, Trade


class History:
    """A record of all trades (executed offers) in a given market.
    
    Attrs:
        market: The market to which all recorded trades pertain.
        trades: A sorted list of all trades in the market.
    """
    
    def __init__(self, market: Market) -> None:
        """Creates an empty history of trades.
        
        Args:
            market: The market to which all recorded trades pertain.
        """
        self.market = market

        self.trades = SortedListWithKey(Trade.sort_by_time)

    @property
    def last(self) -> Trade:
        """Fetches the last executed trade."""
        return self.trades[-1]

    def clear(self) -> None:
        """Removes all trades from this history."""
        self.trades.clear()

    def add(self, trade: Trade) -> None:
        """Adds a trade to the history.
        
        The trade does not have to be the lastest record. (It is e.g.
        common to fetch the history in episodes back in time.)
        
        Args:
            trade: A newly registered trade.
        """
        self.trades.add(trade)

    def add_many(self, trades: List[Trade]) -> None:
        """Registers multiple trades to the history.
        
        Args:
            trades: A list of trades.
        """
        self.trades.update(trades)

    def remove(self, trade: Trade) -> None:
        """Removes a specific trade from the history.
        
        Args:
            trade: A previously registered trade.
        
        Raises:
            ValueError if the trade was not registered to this history.
        """
        self.trades.remove(trade)
