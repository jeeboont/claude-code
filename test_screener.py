#!/usr/bin/env python3
"""
Quick test script to verify the screener functionality
"""

import sys
from src.screener import StockScreener


def test_basic_functionality():
    """Test basic screener functionality with a few stocks"""
    print("Testing Stock Screener Functionality\n")
    print("="*60)

    # Test with a small set of stocks
    test_stocks = ['AAPL', 'MSFT']

    print(f"\nTest 1: Fetching data for {test_stocks}")
    print("-"*60)

    screener = StockScreener(period='1mo', interval='1d')

    # Test screening
    try:
        results = screener.screen_multiple_stocks(
            symbols=test_stocks,
            filter_type='bullish',
            verbose=True
        )

        if results:
            print(f"\n✓ Successfully screened {len(results)} stocks")

            df = screener.results_to_dataframe(filtered_only=False)
            print("\nResults preview:")
            print(df.to_string(index=False))

            print("\n✓ All tests passed!")
            return True
        else:
            print("\n✗ Failed to screen stocks")
            return False

    except Exception as e:
        print(f"\n✗ Error during screening: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
