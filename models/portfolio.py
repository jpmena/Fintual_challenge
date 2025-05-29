from typing import Dict, List, Optional
from .stock import Stock
from .trade import Trade

class Portfolio:
    """
    A simple portfolio of stock holdings with target allocation and rebalancing.

    Attributes:
        holdings: A mapping of ticker to Stock instances representing current holdings.
        target_alloc: A mapping of ticker to target weight (fractional, must sum to 1.0).
    """

    def __init__(self, holdings: Dict[str, Stock], target_alloc: Dict[str, float]):
        if not abs(sum(target_alloc.values()) - 1.0) < 1e-6:
            raise ValueError("Target allocations must sum to 1.0")
        if set(holdings) != set(target_alloc):
            raise ValueError("Holdings symbols and target allocation symbols must match")

        self.holdings = holdings
        self.target_alloc = target_alloc

    def total_value(self) -> float:
        """
        Compute the total market value of the portfolio.

        Returns:
            Sum of market values for all holdings.
        """
        return sum(stock.market_value() for stock in self.holdings.values())

    def current_allocations(self) -> Dict[str, float]:
        """
        Compute the current allocation weights for each holding.

        Returns:
            A mapping of ticker to current weight (fraction of total value).
        """
        total = self.total_value()
        if total == 0:
            return {symbol: 0 for symbol in self.holdings}

        return {
            symbol: stock.market_value() / total
            for symbol, stock in self.holdings.items()
        }

    def get_rebalancing_trades(self) -> List[Trade]:
        """Calculate trades needed to rebalance to target allocation."""
        total = self.total_value()
        trades = []
        
        for symbol, target_weight in self.target_alloc.items():
            current_value = self.holdings[symbol].market_value()
            target_value = total * target_weight
            price = self.holdings[symbol].last_price
            
            if price == 0:
                continue
                
            shares_diff = (target_value - current_value) / price
            # Round to nearest integer and only create trade if at least 1 share difference
            shares_diff_int = round(shares_diff)
            if abs(shares_diff_int) >= 1:
                trades.append(Trade(symbol=symbol, shares=shares_diff_int))
                
        return trades

class PortfolioBuilder:
    """
    Builder pattern implementation for creating Portfolio instances.
    Allows for future extensibility and validation rules.
    """
    def __init__(self):
        self._holdings: Dict[str, Stock] = {}
        self._target_alloc: Dict[str, float] = {}

    def add_holding(self, stock: Stock) -> 'PortfolioBuilder':
        """Add a stock holding to the portfolio."""
        self._holdings[stock.symbol] = stock
        return self

    def set_target_allocation(self, symbol: str, weight: float) -> 'PortfolioBuilder':
        """Set target allocation for a symbol."""
        if weight < 0 or weight > 1:
            raise ValueError("Allocation weight must be between 0 and 1")
        self._target_alloc[symbol] = weight
        return self

    def build(self) -> Portfolio:
        """
        Build and return a Portfolio instance.
        
        Raises:
            ValueError: If validations fail.
        """
        if not self._holdings:
            raise ValueError("Portfolio must have at least one holding")
        if not self._target_alloc:
            raise ValueError("Portfolio must have target allocations")
        
        # Ensure all holdings have corresponding allocations and vice versa
        if set(self._holdings) != set(self._target_alloc):
            raise ValueError("Holdings and target allocations must match")
            
        # Validate allocation sum
        total_allocation = sum(self._target_alloc.values())
        if not abs(total_allocation - 1.0) < 1e-6:
            raise ValueError(f"Target allocations must sum to 1.0 (current sum: {total_allocation})")

        return Portfolio(
            holdings=self._holdings.copy(),
            target_alloc=self._target_alloc.copy()
        ) 