#!/usr/bin/env python3
"""
Stock Screener - Main Script
Screens US stocks based on Supertrend and MACD indicators
"""

import argparse
import sys
from src.screener import StockScreener


def load_stock_list(file_path):
    """Load stock symbols from a file"""
    try:
        with open(file_path, 'r') as f:
            symbols = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return symbols
    except FileNotFoundError:
        print(f"Error: Stock list file '{file_path}' not found")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Screen US stocks based on Supertrend and MACD indicators',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Screen for bullish stocks from default list
  python stock_screener.py

  # Screen for bearish stocks
  python stock_screener.py --filter bearish

  # Use custom stock list
  python stock_screener.py --stocks my_stocks.txt

  # Screen specific symbols
  python stock_screener.py --symbols AAPL MSFT GOOGL TSLA

  # Customize indicator parameters
  python stock_screener.py --st-period 14 --st-multiplier 2.5 --macd-fast 10

  # Export results to CSV
  python stock_screener.py --output results.csv
        """
    )

    parser.add_argument(
        '--stocks',
        type=str,
        default='stocks.txt',
        help='Path to file containing stock symbols (default: stocks.txt)'
    )

    parser.add_argument(
        '--symbols',
        type=str,
        nargs='+',
        help='List of stock symbols to screen (overrides --stocks)'
    )

    parser.add_argument(
        '--filter',
        type=str,
        choices=['bullish', 'bearish', 'both'],
        default='bullish',
        help='Filter type: bullish, bearish, or both (default: bullish)'
    )

    parser.add_argument(
        '--period',
        type=str,
        default='3mo',
        help='Historical data period (default: 3mo). Examples: 1mo, 6mo, 1y'
    )

    parser.add_argument(
        '--interval',
        type=str,
        default='1d',
        help='Data interval (default: 1d). Examples: 1h, 1d, 1wk'
    )

    # Supertrend parameters
    parser.add_argument(
        '--st-period',
        type=int,
        default=10,
        help='Supertrend ATR period (default: 10)'
    )

    parser.add_argument(
        '--st-multiplier',
        type=float,
        default=3.0,
        help='Supertrend ATR multiplier (default: 3.0)'
    )

    # MACD parameters
    parser.add_argument(
        '--macd-fast',
        type=int,
        default=12,
        help='MACD fast EMA period (default: 12)'
    )

    parser.add_argument(
        '--macd-slow',
        type=int,
        default=26,
        help='MACD slow EMA period (default: 26)'
    )

    parser.add_argument(
        '--macd-signal',
        type=int,
        default=9,
        help='MACD signal line period (default: 9)'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Output CSV file path (optional)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print verbose progress messages'
    )

    parser.add_argument(
        '--show-all',
        action='store_true',
        help='Show all screened stocks, not just those that pass the filter'
    )

    args = parser.parse_args()

    # Load stock symbols
    if args.symbols:
        symbols = args.symbols
        print(f"Screening {len(symbols)} specified symbols...")
    else:
        print(f"Loading stock list from: {args.stocks}")
        symbols = load_stock_list(args.stocks)
        print(f"Loaded {len(symbols)} symbols")

    # Set up indicator parameters
    supertrend_params = {
        'period': args.st_period,
        'multiplier': args.st_multiplier
    }

    macd_params = {
        'fast': args.macd_fast,
        'slow': args.macd_slow,
        'signal': args.macd_signal
    }

    # Create screener
    screener = StockScreener(period=args.period, interval=args.interval)

    print(f"\nScreening parameters:")
    print(f"  Filter: {args.filter}")
    print(f"  Period: {args.period}")
    print(f"  Interval: {args.interval}")
    print(f"  Supertrend: period={args.st_period}, multiplier={args.st_multiplier}")
    print(f"  MACD: fast={args.macd_fast}, slow={args.macd_slow}, signal={args.macd_signal}")
    print(f"\nStarting screening...\n")

    # Screen stocks
    results = screener.screen_multiple_stocks(
        symbols,
        filter_type=args.filter,
        supertrend_params=supertrend_params,
        macd_params=macd_params,
        verbose=args.verbose
    )

    # Convert to DataFrame
    df = screener.results_to_dataframe(filtered_only=not args.show_all)

    if df.empty:
        print("\nNo stocks found matching the criteria.")
        return

    # Display results
    print("\n" + "="*80)
    print(f"SCREENING RESULTS - {args.filter.upper()} SIGNALS")
    print("="*80 + "\n")

    # Format numeric columns
    if 'close' in df.columns:
        df['close'] = df['close'].apply(lambda x: f"${x:.2f}")
    if 'supertrend' in df.columns:
        df['supertrend'] = df['supertrend'].apply(lambda x: f"{x:.2f}")
    if 'macd' in df.columns:
        df['macd'] = df['macd'].apply(lambda x: f"{x:.4f}")
    if 'macd_signal' in df.columns:
        df['macd_signal'] = df['macd_signal'].apply(lambda x: f"{x:.4f}")
    if 'macd_histogram' in df.columns:
        df['macd_histogram'] = df['macd_histogram'].apply(lambda x: f"{x:.4f}")

    print(df.to_string(index=False))
    print(f"\n\nTotal stocks matching criteria: {len(df)}/{len(results)}")

    # Export to CSV if requested
    if args.output:
        # Convert back to numeric for CSV
        df_export = screener.results_to_dataframe(filtered_only=not args.show_all)
        df_export.to_csv(args.output, index=False)
        print(f"Results exported to: {args.output}")

    print()


if __name__ == '__main__':
    main()
