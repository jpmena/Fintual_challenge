# Portfolio Management System

A simple portfolio management system that allows tracking and rebalancing of stock portfolios based on target allocations. For solution details about the thinking process and solving, please refer to [Solution](SOLUTION.md).

## Features

- Stock portfolio tracking with real-time prices using Yahoo Finance API.
- Portfolio rebalancing based on target allocations.
- Clean, modular code structure.
- Implementation of design patterns for extensibility and maintainability.

## Design Patterns

### Builder Pattern
- Used for creating Stock and Portfolio instances.
- Provides fluent interface for object construction.
- Enforces validation rules during object creation.
- Makes future extensions easier.

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
from models import Portfolio, Stock
from models.stock import StockBuilder
from models.portfolio import PortfolioBuilder
from services import StockPriceService

meta_stock = (StockBuilder()
        .with_symbol("META")
        .with_shares(50)
        .build())
    
    aapl_stock = (StockBuilder()
        .with_symbol("AAPL")
        .with_shares(30)
        .build())
    
    googl_stock = (StockBuilder()
        .with_symbol("GOOGL")
        .with_shares(20)
        .build())

    # Create portfolio using builder pattern
    portfolio_builder = PortfolioBuilder()
    
    # Add holdings
    portfolio_builder.add_holding(meta_stock)
    portfolio_builder.add_holding(aapl_stock)
    portfolio_builder.add_holding(googl_stock)
    
    # Set target allocations
    portfolio_builder.set_target_allocation("META", 0.3)   # 30% META
    portfolio_builder.set_target_allocation("AAPL", 0.4)   # 40% AAPL
    portfolio_builder.set_target_allocation("GOOGL", 0.3)  # 30% GOOGL

    # Build portfolio
    portfolio = portfolio_builder.build()
    
    # Fetch and update current market prices
    price_service = StockPriceService()
    prices = price_service.get_current_prices(list(portfolio.holdings.keys()))
    
    # Update stock prices
    for symbol, price in prices.items():
        portfolio.holdings[symbol].update_price(price)
        
    # Calculate rebalancing trades
    trades = portfolio.get_rebalancing_trades()
                
``` 
