# Portfolio Management System

A simple portfolio management system that allows tracking and rebalancing of stock portfolios based on target allocations. For solution details about the thinking process and solving, please refer to [a relative link](SOLUTION.md)

## Features

- Stock portfolio tracking with real-time prices using Yahoo Finance API
- Portfolio rebalancing based on target allocations
- Clean, modular code structure
- Implementation of design patterns for extensibility and maintainability

## Design Patterns

### Builder Pattern
- Used for creating Stock and Portfolio instances
- Provides fluent interface for object construction
- Enforces validation rules during object creation
- Makes future extensions easier

Example:
```python
stock = (StockBuilder()
    .with_symbol("AAPL")
    .with_shares(100)
    .with_price(150.0)
    .build())

portfolio = (PortfolioBuilder()
    .add_holding(stock)
    .set_target_allocation("AAPL", 0.4)
    .build())
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the example:
```bash
python main.py
```

## Project Structure

- `models/` - Core data models (Stock, Trade, Portfolio)
- `services/` - External services integration (stock price fetching)
- `main.py` - Example usage and main execution
- `requirements.txt` - Project dependencies
- `SOLUTION.md` - Detailed technical solution and design decisions

## Usage Example

```python
from models.portfolio import Portfolio
from models.stock import Stock
from services.price_service import StockPriceService

# Initialize portfolio with holdings and target allocation
holdings = {
    "META": Stock(symbol="META", shares=50),
    "AAPL": Stock(symbol="AAPL", shares=30)
}
target_alloc = {"META": 0.40, "AAPL": 0.60}

# Create portfolio and rebalance
portfolio = Portfolio(holdings=holdings, target_alloc=target_alloc)
trades = portfolio.rebalance()
``` 
