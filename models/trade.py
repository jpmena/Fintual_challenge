from dataclasses import dataclass

@dataclass
class Trade:
    """
    Represents an order to trade shares of a stock.

    Attributes:
        symbol: The ticker symbol of the stock to trade.
        shares: Positive integer for buy, negative integer for sell.
    """
    symbol: str
    shares: int

    def __str__(self) -> str:
        """String representation of the trade."""
        action = "BUY" if self.shares > 0 else "SELL"
        return f"{action} {abs(self.shares)} shares of {self.symbol}" 