# Thanksgiving-Alpha

> **A reproducible research tool for analyzing stock performance patterns around US Thanksgiving**

Quantitative analysis of DJIA stocks measuring returns from X business days before Thanksgiving to Y business days after. Built with Python, featuring proper NYSE trading calendars, configurable analysis windows, and comprehensive statistical outputs.

**Key Finding:** 25-year analysis (2000-2024) shows 83% of DJIA stocks exhibit positive median returns during the Thanksgiving window, with technology and consumer discretionary sectors significantly outperforming.

## Features

- Analyzes stock performance around Thanksgiving using configurable trading windows
- Calculates returns from X business days before to Y business days after Thanksgiving
- Proper NYSE trading calendar with market holidays and half-day sessions
- Black Friday treated as a trading day (half-day: market closes at 1:00 PM ET)
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

- Black Friday is a half-day trading session (closes at 1:00 PM ET) but counts as a trading day for business day calculations
- NYSE market holidays are properly excluded from business day counts
- Symbols with fewer than `min_trades` observations are filtered out
- Missing data for individual years is handled gracefully
- All returns are simple returns (not log returns)

## Results & Findings

For comprehensive analysis results, see:
- **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Stakeholder-focused overview
- **[ANALYSIS_25YEARS.md](ANALYSIS_25YEARS.md)** - Detailed 25-year findings (2000-2024)

**Top 3 Performers (2000-2024):**
1. Apple (AAPL): +2.00% median return, 72% win rate
2. Amazon (AMZN): +1.69% median return, 68% win rate  
3. Home Depot (HD): +1.26% median return, 76% win rate

## Disclaimer

⚠️ **This tool is for research and educational purposes only.**

- Past performance does not guarantee future results
- Not financial advice or investment recommendations
- Markets evolve; historical patterns may not persist
- Transaction costs and slippage would reduce actual returns
- Survivorship bias present (current DJIA constituents only)
- Always consult qualified financial professionals before making investment decisions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Martin Liebl**  
📧 Email: [lieblm@gmail.com](mailto:lieblm@gmail.com)  
🐙 GitHub: [@lieblm](https://github.com/lieblm)

Questions, feedback, or collaboration inquiries are welcome!

## Support This Project
- ⭐ Star this repository
- 🐛 Report bugs or suggest features via [Issues](https://github.com/lieblm/thanksgiving-alpha/issues)
- 📖 Share your research findings using this tool
- 🔀 Contribute code improvements via Pull Requests
- 🎁 [Sponsor @lieblm on GitHub](https://github.com/sponsors/lieblm)

---

**Built with ❤️ for the quantitative finance community**
