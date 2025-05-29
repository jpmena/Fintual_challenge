import yfinance as yf
from typing import Dict, List
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockPriceService:
    """Service for fetching real-time stock prices using Yahoo Finance API."""
    
    @staticmethod
    def get_current_prices(symbols: List[str]) -> Dict[str, float]:
        """
        Fetch current prices for multiple stock symbols.
        
        Args:
            symbols: List of stock symbols to fetch prices for.
            
        Returns:
            Dictionary mapping symbols to their current prices.
            If a price cannot be fetched, that symbol will be omitted.
        """
        prices = {}
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                current_price = ticker.info.get('regularMarketPrice')
                if current_price:
                    prices[symbol] = float(current_price)
                else:
                    logger.warning(f"Could not get price for {symbol}")
            except Exception as e:
                logger.error(f"Error fetching price for {symbol}: {str(e)}")
                prices[symbol] = input(f"Please manually enter the price for {symbol}: ")
        return prices

    @staticmethod
    def update_portfolio_prices(portfolio) -> None:
        """
        Update all stock prices in a portfolio with current market prices.
        
        Args:
            portfolio: A Portfolio instance to update prices for.
        """
        symbols = list(portfolio.holdings.keys())
        prices = StockPriceService.get_current_prices(symbols)
        
        for symbol, price in prices.items():
            if symbol in portfolio.holdings:
                portfolio.holdings[symbol].update_price(price)
                logger.info(f"Updated {symbol} price to ${price:.2f}") 