"""
Stock Data Fetcher Module
Handles fetching historical stock data using yfinance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


class StockDataFetcher:
    """Fetches stock data from Yahoo Finance"""

    def __init__(self, period='3mo', interval='1d'):
        """
        Initialize the data fetcher

        Args:
            period: Time period to fetch (e.g., '1mo', '3mo', '6mo', '1y')
            interval: Data interval (e.g., '1d', '1h', '5m')
        """
        self.period = period
        self.interval = interval

    def fetch_stock_data(self, symbol):
        """
        Fetch historical data for a single stock

        Args:
            symbol: Stock ticker symbol

        Returns:
            DataFrame with OHLCV data, or None if fetch fails
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=self.period, interval=self.interval)

            if df.empty:
                return None

            # Standardize column names to lowercase
            df.columns = df.columns.str.lower()

            # Reset index to make Date a column
            df = df.reset_index()

            # Ensure we have the required columns
            required_cols = ['close', 'high', 'low', 'open', 'volume']
            if not all(col in df.columns for col in required_cols):
                return None

            return df

        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None

    def fetch_multiple_stocks(self, symbols, verbose=False):
        """
        Fetch historical data for multiple stocks

        Args:
            symbols: List of stock ticker symbols
            verbose: Print progress messages

        Returns:
            Dictionary with symbol as key and DataFrame as value
        """
        stock_data = {}

        for symbol in symbols:
            if verbose:
                print(f"Fetching data for {symbol}...")

            df = self.fetch_stock_data(symbol)

            if df is not None:
                stock_data[symbol] = df
            else:
                if verbose:
                    print(f"Failed to fetch data for {symbol}")

        return stock_data

    def get_latest_price(self, symbol):
        """
        Get the latest price for a stock

        Args:
            symbol: Stock ticker symbol

        Returns:
            Latest close price or None
        """
        df = self.fetch_stock_data(symbol)

        if df is not None and not df.empty:
            return df['close'].iloc[-1]

        return None


def validate_symbol(symbol):
    """
    Validate if a stock symbol exists and has data

    Args:
        symbol: Stock ticker symbol

    Returns:
        Boolean indicating if symbol is valid
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # Check if we got valid data
        if 'symbol' in info or 'shortName' in info:
            return True

        return False

    except:
        return False
