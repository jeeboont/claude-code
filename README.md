# Stock Screener - Supertrend & MACD

A Python-based stock screener that filters US stocks based on **Supertrend** and **MACD** (Moving Average Convergence Divergence) technical indicators.

## Features

- **Technical Indicators**:
  - Supertrend indicator with customizable ATR period and multiplier
  - MACD indicator with configurable fast/slow EMA and signal line periods

- **Flexible Screening**:
  - Filter for bullish, bearish, or both signal types
  - Screen custom lists of stocks or use the provided sample list
  - Adjustable historical data periods and intervals

- **Data Export**:
  - View results in formatted tables
  - Export results to CSV for further analysis

## How It Works

The screener identifies stocks where both indicators agree:

- **Bullish Signal**: Both Supertrend and MACD show bullish trends
  - Supertrend: Price is above the Supertrend line
  - MACD: MACD line is above the signal line

- **Bearish Signal**: Both Supertrend and MACD show bearish trends
  - Supertrend: Price is below the Supertrend line
  - MACD: MACD line is below the signal line

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd claude-code
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Screen for bullish stocks using the default stock list:
```bash
python stock_screener.py
```

### Filter Options

Screen for bearish signals:
```bash
python stock_screener.py --filter bearish
```

Screen for both bullish and bearish signals:
```bash
python stock_screener.py --filter both
```

### Custom Stock Lists

Use a custom stock list file:
```bash
python stock_screener.py --stocks my_stocks.txt
```

Screen specific symbols:
```bash
python stock_screener.py --symbols AAPL MSFT GOOGL TSLA NVDA
```

### Customize Indicator Parameters

Adjust Supertrend parameters:
```bash
python stock_screener.py --st-period 14 --st-multiplier 2.5
```

Adjust MACD parameters:
```bash
python stock_screener.py --macd-fast 10 --macd-slow 20 --macd-signal 7
```

### Historical Data Options

Use different time periods:
```bash
python stock_screener.py --period 6mo  # 6 months of data
python stock_screener.py --period 1y   # 1 year of data
```

Use different intervals:
```bash
python stock_screener.py --interval 1h   # Hourly data
python stock_screener.py --interval 1wk  # Weekly data
```

### Output Options

Show all screened stocks (not just matches):
```bash
python stock_screener.py --show-all
```

Export results to CSV:
```bash
python stock_screener.py --output results.csv
```

Enable verbose output:
```bash
python stock_screener.py --verbose
```

## Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--stocks` | string | stocks.txt | Path to file containing stock symbols |
| `--symbols` | list | - | List of stock symbols (overrides --stocks) |
| `--filter` | choice | bullish | Filter type: bullish, bearish, or both |
| `--period` | string | 3mo | Historical data period (1mo, 3mo, 6mo, 1y, etc.) |
| `--interval` | string | 1d | Data interval (1h, 1d, 1wk, etc.) |
| `--st-period` | int | 10 | Supertrend ATR period |
| `--st-multiplier` | float | 3.0 | Supertrend ATR multiplier |
| `--macd-fast` | int | 12 | MACD fast EMA period |
| `--macd-slow` | int | 26 | MACD slow EMA period |
| `--macd-signal` | int | 9 | MACD signal line period |
| `--output` | string | - | Output CSV file path |
| `--verbose` | flag | False | Print verbose progress messages |
| `--show-all` | flag | False | Show all stocks, not just matches |

## Project Structure

```
claude-code/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── indicators.py        # Supertrend and MACD calculations
│   ├── data_fetcher.py      # Stock data fetching using yfinance
│   └── screener.py          # Stock screening logic
├── stock_screener.py        # Main CLI script
├── stocks.txt               # Sample stock list
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Technical Indicators Explained

### Supertrend

The Supertrend indicator is based on Average True Range (ATR) and helps identify trend direction:
- When price is above Supertrend: **Bullish trend**
- When price is below Supertrend: **Bearish trend**

**Parameters**:
- `period`: ATR calculation period (default: 10)
- `multiplier`: ATR multiplier for bands (default: 3.0)

### MACD (Moving Average Convergence Divergence)

MACD shows the relationship between two moving averages:
- When MACD line is above signal line: **Bullish momentum**
- When MACD line is below signal line: **Bearish momentum**

**Parameters**:
- `fast`: Fast EMA period (default: 12)
- `slow`: Slow EMA period (default: 26)
- `signal`: Signal line EMA period (default: 9)

## Creating Custom Stock Lists

Create a text file with one stock symbol per line:

```
# My custom stock list
AAPL
MSFT
GOOGL
TSLA
```

Lines starting with `#` are treated as comments and ignored.

## Example Output

```
================================================================================
SCREENING RESULTS - BULLISH SIGNALS
================================================================================

symbol  passes_filter    close supertrend_signal macd_trend  supertrend     macd macd_signal macd_histogram
  AAPL           True  $175.43           BULLISH    BULLISH      172.15   2.3456      1.8901         0.4555
  MSFT           True  $378.91           BULLISH    BULLISH      371.22   5.6789      4.2341         1.4448
  NVDA           True  $495.22           BULLISH    BULLISH      485.67   8.9012      7.1234         1.7778


Total stocks matching criteria: 3/50
```

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **yfinance**: Fetching stock data from Yahoo Finance
- **pandas-ta**: Technical analysis indicators (optional, not currently used)
- **requests**: HTTP library for API calls

## Limitations

- Data is fetched from Yahoo Finance (yfinance), which may have rate limits
- Historical data availability varies by stock and exchange
- Real-time data may have a delay
- Screening many stocks can take time due to API rate limits

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is for educational and informational purposes only. It is not financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.
