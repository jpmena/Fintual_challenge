from dataclasses import dataclass

@dataclass
class Trade:
    """
    Represents an order to trade shares of a stock.

    Attributes:
        symbol: The ticker symbol of the stock to trade.
        shares: Positive number for buy, negative for sell.
    """
    symbol: str
    shares: float

    def __str__(self) -> str:
        """String representation of the trade."""
        action = "BUY" if self.shares > 0 else "SELL"
        return f"{action} {abs(self.shares):.2f} shares of {self.symbol}" 