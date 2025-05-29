from dataclasses import dataclass
from typing import Optional

@dataclass
class Stock:
    """
    Represents a stock holding in a portfolio.

    Attributes:
        symbol: The ticker symbol of the stock (e.g., 'AAPL').
        shares: The number of shares currently held.
        last_price: The most recent price per share.
    """
    symbol: str
    shares: float
    last_price: float = 0.0

    def update_price(self, price: float) -> None:
        """
        Update the last known price of the stock.

        Args:
            price: The latest market price per share.
        """
        self.last_price = price

    def market_value(self) -> float:
        """
        Calculate the current market value of the holding.

        Returns:
            Current market value (shares * last_price).
        """
        return self.shares * self.last_price 

class StockBuilder:
    """
    Builder pattern implementation for creating Stock instances.
    Allows for future extensibility and validation rules.
    """
    def __init__(self):
        self._symbol: Optional[str] = None
        self._shares: Optional[float] = None
        self._last_price: float = 0.0

    def with_symbol(self, symbol: str) -> 'StockBuilder':
        """Set the stock symbol."""
        self._symbol = symbol.upper()
        return self

    def with_shares(self, shares: float) -> 'StockBuilder':
        """Set the number of shares."""
        if shares < 0:
            raise ValueError("Number of shares cannot be negative")
        self._shares = shares
        return self

    def with_price(self, price: float) -> 'StockBuilder':
        """Set the last known price."""
        if price < 0:
            raise ValueError("Price cannot be negative")
        self._last_price = price
        return self

    def build(self) -> Stock:
        """
        Build and return a Stock instance.
        
        Raises:
            ValueError: If required fields are missing.
        """
        if not self._symbol:
            raise ValueError("Stock symbol is required")
        if self._shares is None:
            raise ValueError("Number of shares is required")

        return Stock(
            symbol=self._symbol,
            shares=self._shares,
            last_price=self._last_price
        ) 