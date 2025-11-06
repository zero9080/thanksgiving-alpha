# Thanksgiving-Alpha

Seasonality research around US Thanksgiving for DJIA constituents and indices.
Parameterizable window: X business days **before** Thanksgiving (use Open) to Y business days **after** (use Close; Black Friday half-day honored).

## Features

- Analyzes stock performance around Thanksgiving using configurable trading windows
- Calculates returns from X business days before to Y business days after Thanksgiving
- Proper NYSE trading calendar with market holidays
- Aggregates statistics per symbol: median return, average return, win rate, standard deviation
- Exports results to CSV, Parquet, and HTML formats
- Comprehensive test suite with 28+ unit tests

## Quickstart

```bash
# Using poetry (recommended)
pipx install poetry
poetry install
poetry run python -m tgalpha.cli configs/example_djia.yaml --top=20

# Or using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
python -m tgalpha.cli configs/example_djia.yaml --top=20
```

## Usage

### Basic Command

```bash
python -m tgalpha.cli <config_file> [--top=N]
```

**Arguments:**
- `config_file`: Path to YAML configuration file (required)
- `--top`: Number of top-ranked symbols to display in console output (default: 20)

### Configuration File

Create a YAML configuration file (see `configs/example_djia.yaml`):

```yaml
universe: djia                # Use built-in DJIA list or path to CSV file
start_year: 1990              # First year to analyze
end_year: 2025                # Last year to analyze (inclusive)
window:
  days_before: 3              # Business days before Thanksgiving
  days_after: 1               # Business days after Thanksgiving
ranking:
  min_trades: 10              # Minimum observations required per symbol
output:
  dir: "data/outputs"         # Output directory
  formats: ["parquet", "csv", "html"]  # Export formats
```

### Example Output

```
Analyzing 30 symbols from 2020 to 2024...
Collected 150 return observations across 30 symbols

Top 5 symbols by median return:
symbol  n  median_return  avg_return  win_rate      std
    BA  5       0.033791    0.019930       0.8 0.053876
   CVX  5       0.022089    0.017793       0.8 0.018389
    VZ  5       0.018682    0.018656       1.0 0.008942
   MMM  5       0.018013    0.011875       0.8 0.020157
   IBM  5       0.017507    0.019707       0.8 0.023459

Full results saved to data/outputs/
```

### Output Files

Results are saved to the configured output directory:
- `ranking.csv` - Full ranking table in CSV format
- `ranking.parquet` - Full ranking table in Parquet format  
- `ranking.html` - HTML table for easy viewing

### Output Columns

- `symbol`: Stock ticker
- `n`: Number of observations (years with data)
- `median_return`: Median return across all years
- `avg_return`: Average (mean) return
- `win_rate`: Proportion of positive returns
- `std`: Standard deviation of returns

## Development

### Running Tests

```bash
poetry run pytest -v
```

### Linting and Formatting

```bash
# Check code quality
poetry run ruff check .
poetry run black --check .
poetry run mypy src

# Auto-fix issues
poetry run ruff check . --fix
poetry run black .
```

### Project Structure

```
thanksgiving-alpha/
├── configs/               # Configuration files
│   └── example_djia.yaml  # Example DJIA configuration
├── src/tgalpha/          # Main package
│   ├── calendar_utils.py  # NYSE trading calendar
│   ├── cli.py            # Command-line interface
│   ├── config.py         # Configuration models
│   ├── holidays.py       # Thanksgiving date calculation
│   ├── ranking.py        # Aggregation and ranking
│   ├── report.py         # Export functionality
│   ├── stats.py          # Return calculation
│   ├── universe.py       # Symbol universe loading
│   └── data_providers/   # Data source implementations
│       ├── base.py       # Abstract provider interface
│       └── yahoo.py      # Yahoo Finance implementation
├── tests/                # Unit tests
└── data/outputs/         # Generated results (gitignored)
```

## How It Works

1. **Date Calculation**: For each year, calculates Thanksgiving (4th Thursday of November)
2. **Trading Window**: Determines X business days before and Y business days after using NYSE calendar
3. **Data Download**: Fetches OHLC data from Yahoo Finance with a buffer around the window
4. **Return Calculation**: Computes `(Close_after / Open_before) - 1.0` for each year
5. **Aggregation**: Groups by symbol and calculates median, mean, win rate, and standard deviation
6. **Ranking**: Sorts by median return (primary), win rate (secondary), average return (tertiary)
7. **Export**: Saves results in multiple formats for further analysis

## Notes

- Black Friday is treated as a full trading day (standard since 1993)
- NYSE market holidays are properly excluded from business day counts
- Symbols with fewer than `min_trades` observations are filtered out
- Missing data for individual years is handled gracefully
- All returns are simple returns (not log returns)
