"""
Technical Indicators Module
Implements Supertrend and MACD indicators for stock screening
"""

import pandas as pd
import numpy as np


def calculate_atr(df, period=10):
    """
    Calculate Average True Range (ATR)

    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        period: ATR period (default: 10)

    Returns:
        Series with ATR values
    """
    high = df['high']
    low = df['low']
    close = df['close']

    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()

    return atr


def calculate_supertrend(df, period=10, multiplier=3):
    """
    Calculate Supertrend indicator

    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        period: ATR period (default: 10)
        multiplier: ATR multiplier (default: 3)

    Returns:
        DataFrame with 'supertrend' and 'supertrend_signal' columns
        Signal: 1 for buy (bullish), -1 for sell (bearish)
    """
    df = df.copy()

    # Calculate ATR
    atr = calculate_atr(df, period)

    # Calculate basic upper and lower bands
    hl_avg = (df['high'] + df['low']) / 2
    basic_upper = hl_avg + (multiplier * atr)
    basic_lower = hl_avg - (multiplier * atr)

    # Initialize final bands
    final_upper = basic_upper.copy()
    final_lower = basic_lower.copy()
    supertrend = pd.Series(index=df.index, dtype=float)

    # Calculate final bands and Supertrend
    for i in range(period, len(df)):
        # Final Upper Band
        if pd.notna(basic_upper.iloc[i-1]):
            if basic_upper.iloc[i] < final_upper.iloc[i-1] or df['close'].iloc[i-1] > final_upper.iloc[i-1]:
                final_upper.iloc[i] = basic_upper.iloc[i]
            else:
                final_upper.iloc[i] = final_upper.iloc[i-1]

        # Final Lower Band
        if pd.notna(basic_lower.iloc[i-1]):
            if basic_lower.iloc[i] > final_lower.iloc[i-1] or df['close'].iloc[i-1] < final_lower.iloc[i-1]:
                final_lower.iloc[i] = basic_lower.iloc[i]
            else:
                final_lower.iloc[i] = final_lower.iloc[i-1]

        # Supertrend
        if i == period:
            supertrend.iloc[i] = final_upper.iloc[i] if df['close'].iloc[i] <= final_upper.iloc[i] else final_lower.iloc[i]
        else:
            if supertrend.iloc[i-1] == final_upper.iloc[i-1]:
                supertrend.iloc[i] = final_upper.iloc[i] if df['close'].iloc[i] <= final_upper.iloc[i] else final_lower.iloc[i]
            else:
                supertrend.iloc[i] = final_lower.iloc[i] if df['close'].iloc[i] >= final_lower.iloc[i] else final_upper.iloc[i]

    # Calculate signal
    df['supertrend'] = supertrend
    df['supertrend_signal'] = np.where(df['close'] > supertrend, 1, -1)

    return df[['supertrend', 'supertrend_signal']]


def calculate_macd(df, fast=12, slow=26, signal=9):
    """
    Calculate MACD (Moving Average Convergence Divergence) indicator

    Args:
        df: DataFrame with 'close' column
        fast: Fast EMA period (default: 12)
        slow: Slow EMA period (default: 26)
        signal: Signal line period (default: 9)

    Returns:
        DataFrame with 'macd', 'macd_signal', 'macd_histogram', and 'macd_trend' columns
        macd_trend: 1 for bullish (MACD > Signal), -1 for bearish
    """
    df = df.copy()

    # Calculate EMAs
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()

    # Calculate MACD line
    macd = ema_fast - ema_slow

    # Calculate signal line
    macd_signal = macd.ewm(span=signal, adjust=False).mean()

    # Calculate histogram
    macd_histogram = macd - macd_signal

    # Calculate trend (bullish when MACD > Signal)
    macd_trend = np.where(macd > macd_signal, 1, -1)

    result = pd.DataFrame({
        'macd': macd,
        'macd_signal': macd_signal,
        'macd_histogram': macd_histogram,
        'macd_trend': macd_trend
    })

    return result


def get_current_signals(df):
    """
    Get the current (most recent) signals from a DataFrame with indicators

    Args:
        df: DataFrame with indicator columns

    Returns:
        Dictionary with current indicator values and signals
    """
    if df.empty:
        return None

    latest = df.iloc[-1]

    signals = {
        'close': latest.get('close', None),
        'supertrend': latest.get('supertrend', None),
        'supertrend_signal': latest.get('supertrend_signal', None),
        'macd': latest.get('macd', None),
        'macd_signal': latest.get('macd_signal', None),
        'macd_histogram': latest.get('macd_histogram', None),
        'macd_trend': latest.get('macd_trend', None),
    }

    return signals
