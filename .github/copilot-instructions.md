# GitHub Copilot task brief

You are assisting in a Python/Poetry repository called “thanksgiving-alpha”.

## Goal
- Implement a reproducible research tool that ranks DJIA stocks by performance around US Thanksgiving.
- Compute per-year returns from the Open price X business days before Thanksgiving to the Close price Y business days after (Black Friday half-day respected).
- Output CSV and Parquet tables, plus an option to render a simple HTML report later.

## Scope for this iteration
1) Complete minimal functionality using the existing skeleton:
   - Fill any “placeholder” sections if needed.
   - Use Yahoo Finance (yfinance) as the default price provider.
   - Implement window date calculation using business-day logic.
   - For each year in [start_year, end_year] and each symbol in universe:
     open_before = Open(date_shift(thanksgiving(year), -X))
     close_after = Close(date_shift(thanksgiving(year), +Y))
     return = close_after / open_before - 1.0
   - Aggregate per symbol: n, median_return, avg_return, win_rate, std; sort by [median_return, win_rate, avg_return].

2) Configuration
   - Load YAML config at runtime (see configs/example_djia.yaml).
   - Support fields: universe, start_year, end_year, window.{days_before, days_after}, session.*, filters.*, ranking.*, output.*.

3) Data and caching
   - Keep a small buffer when downloading OHLC (±7 calendar days around the target window).
   - No API keys required. Do not commit data files. Respect .gitignore.

4) CLI
   - Command: `tgalpha run --config configs/example_djia.yaml --top 20`
   - Print top-N to stdout as a readable table.
   - Write full ranking to `data/outputs/` as CSV and Parquet.

5) Quality bar
   - Keep code typed (mypy strict) and linted (ruff, black).
   - Add/keep unit tests for: thanksgiving date, business-day shifting, simple return calc.
   - Green CI on GitHub Actions.

## Out of scope for now
- Historical constituent snapshots, advanced calendars, alternative data providers, and HTML report rendering.

## Deliverables
- Working CLI with the above behavior.
- Passing unit tests and CI.
- Short update to README with usage example.
