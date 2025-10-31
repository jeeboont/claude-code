"""
Stock Screener Module
Filters stocks based on Supertrend and MACD indicators
"""

import pandas as pd
from src.indicators import calculate_supertrend, calculate_macd, get_current_signals
from src.data_fetcher import StockDataFetcher


class StockScreener:
    """
    Screen stocks based on technical indicators
    """

    def __init__(self, period='3mo', interval='1d'):
        """
        Initialize the stock screener

        Args:
            period: Historical data period (default: '3mo')
            interval: Data interval (default: '1d')
        """
        self.data_fetcher = StockDataFetcher(period=period, interval=interval)
        self.results = []

    def apply_indicators(self, df, supertrend_params=None, macd_params=None):
        """
        Apply Supertrend and MACD indicators to a DataFrame

        Args:
            df: Stock data DataFrame
            supertrend_params: Dict with 'period' and 'multiplier' (optional)
            macd_params: Dict with 'fast', 'slow', 'signal' (optional)

        Returns:
            DataFrame with indicators added
        """
        if df is None or df.empty:
            return None

        # Default parameters
        if supertrend_params is None:
            supertrend_params = {'period': 10, 'multiplier': 3}

        if macd_params is None:
            macd_params = {'fast': 12, 'slow': 26, 'signal': 9}

        # Calculate Supertrend
        supertrend_df = calculate_supertrend(
            df,
            period=supertrend_params['period'],
            multiplier=supertrend_params['multiplier']
        )

        # Calculate MACD
        macd_df = calculate_macd(
            df,
            fast=macd_params['fast'],
            slow=macd_params['slow'],
            signal=macd_params['signal']
        )

        # Merge all data
        result_df = df.copy()
        result_df = pd.concat([result_df, supertrend_df, macd_df], axis=1)

        return result_df

    def screen_stock(self, symbol, filter_type='bullish', supertrend_params=None, macd_params=None):
        """
        Screen a single stock

        Args:
            symbol: Stock ticker symbol
            filter_type: 'bullish', 'bearish', or 'both'
            supertrend_params: Supertrend parameters
            macd_params: MACD parameters

        Returns:
            Dictionary with screening results or None
        """
        # Fetch data
        df = self.data_fetcher.fetch_stock_data(symbol)

        if df is None or df.empty:
            return None

        # Apply indicators
        df_with_indicators = self.apply_indicators(df, supertrend_params, macd_params)

        if df_with_indicators is None or df_with_indicators.empty:
            return None

        # Get current signals
        signals = get_current_signals(df_with_indicators)

        if signals is None:
            return None

        # Check if stock passes the filter
        passes_filter = False

        if filter_type == 'bullish':
            # Both Supertrend and MACD should be bullish
            passes_filter = (signals['supertrend_signal'] == 1 and signals['macd_trend'] == 1)

        elif filter_type == 'bearish':
            # Both Supertrend and MACD should be bearish
            passes_filter = (signals['supertrend_signal'] == -1 and signals['macd_trend'] == -1)

        elif filter_type == 'both':
            # Stock passes if either bullish or bearish on both indicators
            bullish = (signals['supertrend_signal'] == 1 and signals['macd_trend'] == 1)
            bearish = (signals['supertrend_signal'] == -1 and signals['macd_trend'] == -1)
            passes_filter = bullish or bearish

        # Prepare result
        result = {
            'symbol': symbol,
            'passes_filter': passes_filter,
            'close': signals['close'],
            'supertrend': signals['supertrend'],
            'supertrend_signal': 'BULLISH' if signals['supertrend_signal'] == 1 else 'BEARISH',
            'macd': signals['macd'],
            'macd_signal': signals['macd_signal'],
            'macd_histogram': signals['macd_histogram'],
            'macd_trend': 'BULLISH' if signals['macd_trend'] == 1 else 'BEARISH',
        }

        return result

    def screen_multiple_stocks(self, symbols, filter_type='bullish', supertrend_params=None, macd_params=None, verbose=False):
        """
        Screen multiple stocks

        Args:
            symbols: List of stock ticker symbols
            filter_type: 'bullish', 'bearish', or 'both'
            supertrend_params: Supertrend parameters
            macd_params: MACD parameters
            verbose: Print progress messages

        Returns:
            List of dictionaries with screening results
        """
        results = []

        for i, symbol in enumerate(symbols, 1):
            if verbose:
                print(f"Screening {symbol} ({i}/{len(symbols)})...")

            result = self.screen_stock(symbol, filter_type, supertrend_params, macd_params)

            if result is not None:
                results.append(result)

        self.results = results
        return results

    def get_filtered_stocks(self, results=None):
        """
        Get only stocks that pass the filter

        Args:
            results: List of screening results (uses self.results if None)

        Returns:
            List of dictionaries for stocks that passed the filter
        """
        if results is None:
            results = self.results

        return [r for r in results if r['passes_filter']]

    def results_to_dataframe(self, results=None, filtered_only=False):
        """
        Convert screening results to a DataFrame

        Args:
            results: List of screening results (uses self.results if None)
            filtered_only: Only include stocks that passed the filter

        Returns:
            DataFrame with screening results
        """
        if results is None:
            results = self.results

        if filtered_only:
            results = self.get_filtered_stocks(results)

        if not results:
            return pd.DataFrame()

        df = pd.DataFrame(results)

        # Reorder columns for better readability
        column_order = [
            'symbol', 'passes_filter', 'close',
            'supertrend_signal', 'macd_trend',
            'supertrend', 'macd', 'macd_signal', 'macd_histogram'
        ]

        # Only include columns that exist
        column_order = [col for col in column_order if col in df.columns]

        return df[column_order]
