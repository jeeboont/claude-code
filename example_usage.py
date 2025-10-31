#!/usr/bin/env python3
"""
Example usage of the Stock Screener library
Demonstrates how to use the screener programmatically
"""

from src.screener import StockScreener


def main():
    print("Stock Screener - Example Usage\n")
    print("="*60)

    # List of stocks to screen
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']

    print(f"\nScreening {len(stocks)} stocks: {', '.join(stocks)}\n")

    # Create screener instance
    screener = StockScreener(period='3mo', interval='1d')

    # Define indicator parameters
    supertrend_params = {
        'period': 10,
        'multiplier': 3.0
    }

    macd_params = {
        'fast': 12,
        'slow': 26,
        'signal': 9
    }

    # Screen for bullish signals
    print("Looking for BULLISH signals (both Supertrend and MACD bullish)...\n")

    results = screener.screen_multiple_stocks(
        symbols=stocks,
        filter_type='bullish',
        supertrend_params=supertrend_params,
        macd_params=macd_params,
        verbose=True
    )

    # Display results
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60 + "\n")

    if results:
        df = screener.results_to_dataframe(filtered_only=False)
        print(df.to_string(index=False))

        # Show only stocks that passed the filter
        filtered = screener.get_filtered_stocks(results)
        print(f"\n\nStocks passing filter: {len(filtered)}/{len(results)}")

        if filtered:
            print("\nBullish stocks:")
            for stock in filtered:
                print(f"  - {stock['symbol']}: ${stock['close']:.2f}")
        else:
            print("\nNo stocks found with bullish signals on both indicators.")
    else:
        print("No data retrieved for the specified stocks.")

    print()


if __name__ == '__main__':
    main()
