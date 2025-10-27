#!/usr/bin/env python3
"""
Demo script with mock data to show how the screener output looks
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create mock stock data
def create_mock_data(symbol, trend='bullish'):
    """Create mock OHLCV data for demonstration"""
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')

    # Create price data based on trend
    if trend == 'bullish':
        close_prices = np.linspace(100, 150, 90) + np.random.randn(90) * 2
    else:
        close_prices = np.linspace(150, 100, 90) + np.random.randn(90) * 2

    df = pd.DataFrame({
        'date': dates,
        'open': close_prices + np.random.randn(90),
        'high': close_prices + abs(np.random.randn(90)) + 1,
        'low': close_prices - abs(np.random.randn(90)) - 1,
        'close': close_prices,
        'volume': np.random.randint(1000000, 10000000, 90)
    })

    return df

# Import our screener
from src.screener import StockScreener
from src.indicators import calculate_supertrend, calculate_macd, get_current_signals

print("="*80)
print("STOCK SCREENER DEMO - With Mock Data")
print("="*80)
print("\nThis demonstrates how the screener works with sample data")
print("(In production, it fetches real data from Yahoo Finance)\n")

# Create mock data for demonstration
stocks_data = {
    'AAPL': create_mock_data('AAPL', 'bullish'),
    'MSFT': create_mock_data('MSFT', 'bullish'),
    'GOOGL': create_mock_data('GOOGL', 'bearish'),
    'TSLA': create_mock_data('TSLA', 'bearish'),
    'NVDA': create_mock_data('NVDA', 'bullish'),
}

results = []

print("Screening 5 stocks with Supertrend and MACD indicators...\n")

for symbol, df in stocks_data.items():
    print(f"Processing {symbol}...")

    # Apply indicators
    st_df = calculate_supertrend(df, period=10, multiplier=3.0)
    macd_df = calculate_macd(df, fast=12, slow=26, signal=9)

    # Combine data
    df_combined = pd.concat([df, st_df, macd_df], axis=1)

    # Get current signals
    signals = get_current_signals(df_combined)

    # Check if bullish
    is_bullish = (signals['supertrend_signal'] == 1 and signals['macd_trend'] == 1)

    result = {
        'symbol': symbol,
        'passes_filter': is_bullish,
        'close': signals['close'],
        'supertrend_signal': 'BULLISH' if signals['supertrend_signal'] == 1 else 'BEARISH',
        'macd_trend': 'BULLISH' if signals['macd_trend'] == 1 else 'BEARISH',
        'supertrend': signals['supertrend'],
        'macd': signals['macd'],
        'macd_signal': signals['macd_signal'],
        'macd_histogram': signals['macd_histogram'],
    }

    results.append(result)

# Display all results
print("\n" + "="*80)
print("ALL STOCKS SCREENED")
print("="*80 + "\n")

df_all = pd.DataFrame(results)
print(df_all.to_string(index=False))

# Display only bullish stocks
print("\n" + "="*80)
print("BULLISH SIGNALS (Both Supertrend and MACD Bullish)")
print("="*80 + "\n")

df_bullish = df_all[df_all['passes_filter'] == True]
if not df_bullish.empty:
    print(df_bullish.to_string(index=False))
    print(f"\n\nTotal bullish stocks: {len(df_bullish)}/{len(results)}")
else:
    print("No stocks found with bullish signals on both indicators.")

print("\n" + "="*80)
print("\nNOTE: This demo uses mock data. When running on your local machine")
print("with internet access, the screener will fetch real stock data from")
print("Yahoo Finance and provide actual market signals.")
print("="*80 + "\n")
