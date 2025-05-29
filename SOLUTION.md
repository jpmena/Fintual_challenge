# Portfolio Management System - Technical Solution

## Problem Statement
Create a Portfolio management system that can:
- Track a collection of stocks with their current prices.
- Maintain target allocations for each stock.
- Calculate rebalancing trades to achieve target allocations.

## Architecture and Design Patterns

### 1. Design Patterns Used

#### Builder Pattern
- Implemented for both Stock and Portfolio creation to handle complex object construction.
- Allows for future extensibility of object attributes and validation rules.
- Separates construction from representation.

#### Observer Pattern (Price Updates)
- StockPriceService acts as the subject.
- Stock objects are observers that get updated with new prices.
- Decouples price fetching from stock management.

#### Strategy Pattern (Future Extensibility)
- Portfolio rebalancing algorithm is encapsulated.
- Allows for different rebalancing strategies in the future.

### 2. Code Organization

The solution follows a clean architecture approach with:
- `models/` - Core domain models (Stock, Trade, Portfolio).
- `services/` - External integrations (Yahoo Finance API).
- Clear separation of concerns between data models and business logic.

### 3. Key Features

#### Real-time Price Updates
- Integration with Yahoo Finance API.
- Robust error handling for API failures.
- Asynchronous price updates possible in future iterations.

#### Portfolio Rebalancing
- Calculates optimal trades to achieve target allocation.
- Considers current market prices.
- Minimizes number of trades needed.

### 4. Future Extensibility

The solution is designed to be extended with different new functionalities and data, such as, for example:
- Additional stock data providers.
- Different rebalancing strategies.
- Transaction cost optimization.
- Risk metrics and analysis.
- Historical performance tracking.

### 5. Testing Considerations

While not implemented in the 3-hour timeframe, the code is structured to be testable:
- Models are isolated and stateless where possible.
- External dependencies (Yahoo Finance) are abstracted.
- Clear interfaces between components.

### 6. Production Readiness

The code includes:
- Comprehensive error handling.
- Logging for debugging and monitoring.
- Type hints for better maintainability.
- Documentation and docstrings.

## Development History

### Initial Requirements
- Original task: Construct a simple Portfolio class that has a collection of Stocks. Assume each Stock has a “Current Price” method that receives the last available price. Also, the Portfolio class has a collection of “allocated” Stocks that represents the distribution of the Stocks the Portfolio is aiming (i.e. 40% META, 60% APPL)
Provide a portfolio rebalance method to know which Stocks should be sold and which ones should be bought to have a balanced Portfolio based on the portfolio’s allocation.
Add documentation/comments to understand your thinking process and solution
Important: If you use LLMs that’s ok, but you must share the conversations.
- Time constraint: 3 hours
- Focus on maintainability and professional organization.

### Evolution of Solution

1. First code:
   - First code written without LLM:
   ```python
from dataclasses import dataclass
from typing import Dict, List
import math

@dataclass
class Stock:
    """
    Represents a stock holding in a portfolio.

    Attributes:
        symbol: The ticker symbol (e.g., 'AAPL').
        shares: The number of shares currently held.
        last_price: The most recent price per share.
    """
    symbol: str
    shares: float
    last_price: float = 0.0

    def update_price(self, price: float) -> None:
        """
        Update the stock's latest price.

        Args:
            price: Latest market price per share.
        """
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.last_price = price

    def market_value(self) -> float:
        """
        Calculate current market value of this holding.

        Returns:
            shares * last_price
        """
        return self.shares * self.last_price

@dataclass
class Trade:
    """
    Order to adjust position in a stock.

    Attributes:
        symbol: Ticker symbol.
        shares: Positive for buy, negative for sell (integer shares).
    """
    symbol: str
    shares: int

class Portfolio:
    """
    Collection of Stock holdings with target allocations and rebalancing.

    Attributes:
        holdings: Dict of symbol to Stock.
        target_alloc: Dict of symbol to weight (fractions summing to 1.0).
    """
    def __init__(self, holdings: Dict[str, Stock], target_alloc: Dict[str, float]):
        if not math.isclose(sum(target_alloc.values()), 1.0, rel_tol=1e-6):
            raise ValueError("Target allocations must sum to 1.0")
        if set(holdings.keys()) != set(target_alloc.keys()):
            raise ValueError("All holdings must have a matching target allocation")
        self.holdings = holdings
        self.target_alloc = target_alloc

    def total_value(self) -> float:
        """Total market value of the portfolio."""
        return sum(s.market_value() for s in self.holdings.values())

    def current_allocations(self) -> Dict[str, float]:
        """Current weight of each holding."""
        total = self.total_value()
        if total == 0:
            return {sym: 0.0 for sym in self.holdings}
        return {sym: stk.market_value() / total for sym, stk in self.holdings.items()}

    def rebalance(self) -> List[Trade]:
        """
        Compute trades (integer shares) to reach target allocations.

        Returns:
            List of Trade instructions (integer shares to buy/sell).
        """
        total = self.total_value()
        if total == 0:
            raise ValueError("Cannot rebalance an empty portfolio")

        trades: List[Trade] = []
        # Determine share adjustments per holding
        for symbol, target_weight in self.target_alloc.items():
            stock = self.holdings[symbol]
            current_value = stock.market_value()
            target_value = target_weight * total
            value_diff = target_value - current_value

            if stock.last_price <= 0:
                raise ValueError(f"Invalid last price for {symbol}: {stock.last_price}")

            # Determine integer share difference (round to nearest integer)
            raw_shares = value_diff / stock.last_price
            share_diff = int(round(raw_shares))

            # Only record non-zero adjustments
            if share_diff != 0:
                trades.append(Trade(symbol=symbol, shares=share_diff))

        return trades

if __name__ == "__main__":
    holdings = {
        "META": Stock(symbol="META", shares=50),
        "AAPL": Stock(symbol="AAPL", shares=30)
    }
    holdings["META"].update_price(300.00)
    holdings["AAPL"].update_price(150.00)

    target_alloc = {"META": 0.40, "AAPL": 0.60}
    portfolio = Portfolio(holdings, target_alloc)

    trades = portfolio.rebalance()
    for t in trades:
        action = "BUY" if t.shares > 0 else "SELL"
        print(f"{action} {abs(t.shares)} shares of {t.symbol}")

```

2. First Iteration:
   - Question: "How could I improve the initial implementation, involving splitting the code into multiple files, thus improving the structure. Also, which real-time stock price tools are free and easy to use?"
   - Changes Made:
     - Split code into multiple files
     - Added real-time price fetching. In this case, LLM suggested yfinance, which is a library that connects to a Yahoo finance scraper. For this reason, it is important to always use the last version of yfinance, as the old ones tend to get the rate limit error for the scrapers.
     - Improved project structure

3. Second Iteration:
   - Question: "Need to update dependencies, add solution documentation, and implement Builder design patterns"
   - Changes Made:
     - Updated yfinance to latest version
     - Added comprehensive documentation, such as the skeleton for the README and SOLUTION md files. 
     - Implemented Builder pattern for Stock and Portfolio. The idea behind this is to consider that both classes might expand on their functionalities, and applying builder patterns allow to separate how we use the stocks and portfolios objects with how we create them. If in the future we want to add new things such as price history, for example, we would be able to do it without compromising how the objects interact today on the rebalance methods.
     - Added detailed technical documentation

4. Final check:
   - Add manual price input as a complement in case yfinance fails.
   - Tested with different symbols, with yfinance and with manual price input.
   - Tested some border cases such as no price available, target allocation not being 100%, minimum trade size, rounding the number of shares to be an integer, etc.

### Key Decisions

1. Use of Builder Pattern:
   - Chosen for better object construction.
   - Enables future extensibility.
   - Improves code readability.
   - Enforces validation during construction.

2. Project Structure:
   - Modular approach with separate concerns.
   - Clear separation of models and services.
   - Easy to extend and maintain.

3. Documentation:
   - Comprehensive README for quick start.
   - Detailed SOLUTION.md for technical review.
   - Inline documentation and type hints.