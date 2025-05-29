from models import Portfolio, Stock
from models.stock import StockBuilder
from models.portfolio import PortfolioBuilder
from services import StockPriceService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Create stocks using builder pattern
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

    try:
        # Build portfolio
        portfolio = portfolio_builder.build()
        
        # Fetch and update current market prices
        logger.info("Fetching current market prices...")
        price_service = StockPriceService()
        prices = price_service.get_current_prices(list(portfolio.holdings.keys()))
        
        # Update stock prices
        for symbol, price in prices.items():
            portfolio.holdings[symbol].update_price(price)
        
        # Display current portfolio state
        logger.info("\nCurrent Portfolio State:")
        total_value = portfolio.total_value()
        current_alloc = portfolio.current_allocations()
        
        for symbol, stock in portfolio.holdings.items():
            logger.info(f"{symbol}: {stock.shares} shares @ ${stock.last_price:.2f} = ${stock.market_value():.2f} ({current_alloc[symbol]*100:.1f}%)")
        logger.info(f"Total Portfolio Value: ${total_value:.2f}")
        
        # Calculate rebalancing trades
        logger.info("\nRequired Rebalancing Trades:")
        trades = portfolio.get_rebalancing_trades()
        
        if not trades:
            logger.info("No rebalancing needed!")
        else:
            for trade in trades:
                logger.info(str(trade))
                
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 