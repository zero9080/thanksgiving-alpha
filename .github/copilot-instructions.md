# GitHub Copilot Instructions - Thanksgiving-Alpha

## Project Status: ✅ PRODUCTION READY (v1.0.0)

You are assisting in a **Python/Poetry** repository called **"thanksgiving-alpha"** - a quantitative finance research tool for analyzing stock performance around US Thanksgiving.

---

## 🎯 Project Overview

**Purpose:** Reproducible research tool that ranks stocks by performance around US Thanksgiving holiday.  
**Methodology:** Compute per-year returns from Open price X business days before Thanksgiving to Close price Y business days after.  
**Trading Window:** Configurable (default: 3 days before → 1 day after, including Black Friday half-day session at 1:00 PM ET close).  
**Output:** CSV, Parquet, and HTML reports with statistical rankings.

---

## 📊 Current State (as of November 6, 2025)

### ✅ Completed Features

1. **Core Functionality** (All implemented and tested)
   - NYSE trading calendar with 10 federal holidays
   - Black Friday treated as half-day session (closes 1:00 PM ET)
   - Business day shifting logic with proper weekend/holiday handling
   - Yahoo Finance integration (yfinance) with auto_adjust=True
   - Year-tracked return computation with missing data handling
   - Multi-format exports: CSV, Parquet, HTML

2. **Universes Supported** ⭐ **THREE MAJOR INDICES**
   - **S&P 500:** 300 stocks across all sectors (SP500_DEFAULT in universe.py) - **NEW**
   - **NASDAQ-100:** 100 stocks (NASDAQ100_DEFAULT in universe.py)
   - **DJIA:** 30 stocks (DJIA_DEFAULT in universe.py)
   - **Custom:** CSV file support via config
   - **Total Coverage:** 390 unique stocks analyzed

3. **Testing & Quality**
   - **28 passing unit tests** (pytest)
   - Test coverage: holidays, calendar, stats, ranking
   - Typed with mypy (strict mode)
   - Linted with ruff and black
   - All CI checks passing

4. **CLI & Configuration**
   - Command: `python -m tgalpha.cli <config> --top=N`
   - **IMPORTANT:** Uses typer 0.7.0 (NOT 0.12.5 - compatibility issue with TyperArgument.make_metavar())
   - YAML-based configuration system (pydantic validation)

5. **Documentation**
   - README.md (comprehensive usage guide)
   - EXECUTIVE_SUMMARY.md (cross-index stakeholder overview with 8,501 observations) - **UPDATED**
   - ANALYSIS_SP500_25YEARS.md (S&P 500 25-year analysis: 5,879 observations) - **NEW**
   - ANALYSIS_NASDAQ100_25YEARS.md (NASDAQ-100 25-year analysis: 1,904 observations)
   - ANALYSIS_25YEARS.md (DJIA 25-year analysis: 718 observations)
   - CITATION.cff (academic citation support)
   - .github/FUNDING.yml (donation/sponsorship links)

6. **Public Release Ready**
   - Repository prepared for public consumption
   - Contact: Martin Liebl (lieblm@gmail.com)
   - Donation addresses included (BTC, ETH, USDC/USDT)
   - Professional README with disclaimers
   - MIT License

---

## 🔧 Technical Implementation Details

### Key Architecture Decisions

1. **Trading Calendar Logic** (`src/tgalpha/calendar_utils.py`)
   - NYSECalendar class with 10 holidays
   - `shift_business_days()` function handles non-trading days
   - Black Friday is NOT a holiday (half-day session counted as trading day)

2. **Data Provider** (`src/tgalpha/data_providers/yahoo.py`)
   - **Critical:** Use `auto_adjust=True` to avoid MultiIndex column issues
   - Handles missing data gracefully (returns empty DataFrame)
   - 7-day buffer around target window for data fetching

3. **Statistics Engine** (`src/tgalpha/stats.py`)
   - `holiday_window_dates()`: Calculates trading window dates
   - `compute_return()`: Year-tracked returns with null checks
   - Simple returns (not log returns)

4. **Ranking System** (`src/tgalpha/ranking.py`)
   - Aggregates: n, median_return, avg_return, win_rate, std
   - Sorts by: [median_return, win_rate, avg_return]
   - Filters: min_trades parameter (default 10)

5. **Python Environment**
   - Python 3.12.6 with Poetry
   - Key dependencies: polars 1.35.1, pandas 2.3.3, typer 0.7.0, yfinance 0.2.66
   - Virtual environment at `.venv/`

---

## 📈 Key Findings from Completed Analyses

### Comprehensive Multi-Index Summary (2000-2024)
**Total:** 8,501 observations across 390 unique stocks

| Index | Stocks | Observations | Completeness | Top Performer | Consistency Leader |
|-------|--------|--------------|--------------|---------------|-------------------|
| S&P 500 | 264 | 5,879 | 89% | SHOP (+3.36%) | MNST (84% win rate) |
| NASDAQ-100 | 96 | 1,904 | 79% | ENPH (+3.61%) | MNST (84% win rate) |
| DJIA | 30 | 718 | 96% | AAPL (+2.00%) | AMZN/HD/NKE (76% win rate) |

### S&P 500 Analysis (2000-2024) ⭐ **NEWLY COMPLETED**
- **5,879 observations** across 264 stocks (89% completeness)
- **Top performers:** SHOP (+3.36%), DE (+3.08%), PANW (+3.05%), AVGO (+2.27%), AMAT (+2.26%)
- **Consistency champion:** MNST (+2.02% median, 84% win rate)
- **Sector insights:**
  - Technology: 6 of top 10 performers (semiconductors dominate)
  - Consumer Discretionary: Strong retail/e-commerce presence (SHOP, AMZN)
  - Industrials: DE (Deere) shows exceptional +3.08% median
  - Financials: Payment networks (MA +2.17%) vastly outperform banks (GS/JPM/WFC negative)
- **Broadest market coverage** with balanced sector representation
- **Investment strategies documented:** Conservative (75%+ win rate), Balanced (2.0%+ median, 65%+ win rate), Aggressive (2.5%+ median)

### DJIA Analysis (2000-2024)
- **718 observations** across 30 stocks (96% completeness)
- **Top performers:** AAPL (+2.00%), AMZN (+1.69%), HD (+1.26%)
- 83% of stocks show positive median returns
- Technology and consumer discretionary sectors outperform
- Financial sector underperforms

### NASDAQ-100 Analysis (2000-2024)
- **1,904 observations** across 96 stocks (79% completeness)
- **Top performers:** ENPH (+3.61%), PANW (+3.05%), AVGO (+2.27%)
- Semiconductor sector dominance (6 of top 10)
- MNST shows 84% win rate (highest consistency)
- Higher returns but more volatility vs. DJIA
- 79% completeness due to recent IPOs (SNOW, PLTR, DASH, etc.)

### Universal Cross-Index Findings
1. **Thanksgiving seasonality effect confirmed** across all three indices (80-90% positive median returns)
2. **Technology sector leadership** persistent across DJIA, NASDAQ-100, and S&P 500
3. **Consumer discretionary excellence** driven by Black Friday retail anticipation
4. **Traditional banking weakness** (GS, JPM, WFC) consistent across all indices
5. **Payment networks outperform banks** (MA, V significantly higher returns than traditional lenders)

---

## 🔧 Technical Implementation Details

### Step 1: Check Recent History
**ALWAYS start by reviewing git commit history:**
```bash
git log --oneline -20
git log --since="2025-11-01" --pretty=format:"%h - %an, %ar : %s"
```

**Key commits to review:**
- Latest NASDAQ-100 analysis
- Public release preparation
- Black Friday half-day corrections
- 25-year DJIA analysis
- Initial CLI implementation and bug fixes

### Step 2: Review Current Configuration
Check existing config files:
- `configs/example_djia.yaml` - Original DJIA config
- `configs/djia_25years.yaml` - 25-year DJIA analysis
- `configs/nasdaq100_25years.yaml` - 25-year NASDAQ-100 analysis
- `configs/sp500_25years.yaml` - 25-year S&P 500 analysis - **NEW**
- `configs/test_small.yaml` - 5-year test config

### Step 3: Review Analysis Reports
Read the markdown reports to understand findings:
- `ANALYSIS_SP500_25YEARS.md` - S&P 500 comprehensive results - **NEW**
- `ANALYSIS_NASDAQ100_25YEARS.md` - NASDAQ-100 comprehensive results
- `ANALYSIS_25YEARS.md` - DJIA comprehensive results
- `EXECUTIVE_SUMMARY.md` - Cross-index stakeholder summary - **UPDATED**

### Step 4: Understand Known Issues & Limitations

**Data Issues:**
- Some stocks have limited history (recent IPOs: SNOW, PLTR, DASH, ABNB, ARM, UBER, LYFT, COIN, etc.)
- Some stocks have timezone data errors (BRK.B, HES, MRO, PEAK, SQ, SGEN, ANSS)
- Survivorship bias present (using current constituents only)

**Technical Constraints:**
- Typer 0.7.0 required (NOT 0.12.5) - TyperArgument.make_metavar() compatibility
- Yahoo Finance auto_adjust=True required for proper column handling
- Black Friday is half-day (1:00 PM ET close) but counted as trading day

**Test Coverage:**
- Run `pytest tests/ -v` to verify all 28 tests pass
- Coverage includes: holidays (6), calendar (9), stats (8), ranking (6)

---

## 🎯 Potential Future Enhancements

If the user wants to continue development, consider:

1. **Extended Universe Support** ✅ **S&P 500 COMPLETE**
   - ~~S&P 500 analysis~~ ✅ **DONE: 5,879 observations, 264 stocks**
   - Russell 2000 (small caps)
   - Sector-specific ETFs
   - International indices (FTSE, DAX, Nikkei with different holiday calendars)

2. **Advanced Analytics**
   - Historical constituent snapshots (point-in-time universes)
   - Correlation analysis between stocks
   - Volatility regime dependence (VIX-based segmentation)
   - Market cap stratification
   - Rolling window analysis (3-year, 5-year, 10-year periods)

3. **Enhanced Reporting**
   - Interactive HTML dashboards with Plotly
   - Sector heatmaps
   - Year-over-year performance charts
   - Monte Carlo simulations for strategy testing

4. **Strategy Backtesting**
   - Portfolio construction rules
   - Position sizing algorithms
   - Transaction cost modeling
   - Risk-adjusted metrics (Sharpe, Sortino, Calmar)

5. **Data Quality**
   - Point-in-time constituent data (avoid survivorship bias)
   - Alternative data providers (Alpha Vantage, Polygon.io)
   - Corporate action handling (splits, dividends)
   - Delisting detection and handling

6. **Calendar Enhancements**
   - Half-day session hours in data (not just counting as full day)
   - Pre-market/after-hours data
   - Other holiday effects (Christmas, July 4th, etc.)
   - International holiday calendars

---

## 🛠️ Development Workflow Reminders

### Before Making Changes
1. Review git log and recent commits
2. Read relevant analysis reports
3. Check test coverage: `pytest tests/ -v`
4. Review configuration files for examples

### When Adding Features
1. Update universe.py if adding new stock lists
2. Create config file in `configs/` directory
3. Run analysis and generate report
4. Update README.md if CLI changes
5. Add tests if new logic introduced
6. Update this copilot-instructions.md

### When Debugging
1. Check data/outputs/ for actual results
2. Review error messages from yfinance downloads
3. Verify trading calendar logic for specific dates
4. Test with small config (test_small.yaml) first

### Before Committing
1. Run all tests: `pytest tests/ -v`
2. Check linting: `ruff check src/ tests/`
3. Format code: `black src/ tests/`
4. Review git diff carefully
5. Write descriptive commit messages

---

## 📝 Important File Locations

**Source Code:**
- `src/tgalpha/cli.py` - Command-line interface
- `src/tgalpha/universe.py` - Stock universes (DJIA, NASDAQ-100, S&P 500)
- `src/tgalpha/calendar_utils.py` - NYSE calendar and business day logic
- `src/tgalpha/holidays.py` - Thanksgiving date calculation
- `src/tgalpha/stats.py` - Window dates and return computation
- `src/tgalpha/ranking.py` - Aggregation and sorting
- `src/tgalpha/report.py` - Multi-format exports
- `src/tgalpha/data_providers/yahoo.py` - Yahoo Finance integration

**Tests:**
- `tests/test_holidays.py` - 6 tests
- `tests/test_calendar_utils.py` - 9 tests
- `tests/test_stats.py` - 8 tests
- `tests/test_ranking.py` - 6 tests

**Configuration:**
- `pyproject.toml` - Poetry dependencies and project metadata (v1.0.0)
- `.gitignore` - Excludes data/, .venv/, .DS_Store, etc.

**Documentation:**
- `README.md` - Main documentation
- `EXECUTIVE_SUMMARY.md` - Cross-index stakeholder summary
- `ANALYSIS_SP500_25YEARS.md` - S&P 500 25-year findings
- `ANALYSIS_NASDAQ100_25YEARS.md` - NASDAQ-100 25-year findings
- `ANALYSIS_25YEARS.md` - DJIA 25-year findings
- `CITATION.cff` - Academic citation
- `LICENSE` - MIT License

---

## 🔑 Critical Reminders

1. **Black Friday is a half-day session** (closes 1:00 PM ET) - mentioned throughout docs
2. **Typer version must be 0.7.0** - version 0.12.5 causes TyperArgument.make_metavar() error
3. **Yahoo Finance needs auto_adjust=True** - avoids MultiIndex column issues
4. **All 28 tests must pass** before pushing changes
5. **Survivorship bias** - current analyses use present-day constituents only
6. **Contact info** - Martin Liebl (lieblm@gmail.com) in all public-facing docs
7. **Repository is public** - suitable for external consumption

---

## 💡 Quick Commands Reference

```bash
# Run analysis
python -m tgalpha.cli configs/djia_25years.yaml --top=20
python -m tgalpha.cli configs/nasdaq100_25years.yaml --top=50
python -m tgalpha.cli configs/sp500_25years.yaml --top=50

# Run tests
pytest tests/ -v

# Check code quality
ruff check src/ tests/
black src/ tests/ --check
mypy src/

# Format code
black src/ tests/

# Check git history
git log --oneline -20
git log --graph --oneline --all

# Review recent changes
git diff HEAD~5..HEAD
git show <commit-hash>
```

---

## 🎓 Session Context Recovery Protocol

**When starting a new session, ALWAYS:**

1. **Review git log** - Last 20 commits minimum
2. **Read analysis reports** - Understand current findings
3. **Check test status** - Run `pytest tests/ -v`
4. **Review configurations** - See what analyses have been completed
5. **Ask user for context** - What do they want to work on next?

**Common continuation points:**
- Adding new universes (S&P 500, Russell 2000)
- Extending analysis windows (different day combinations)
- Adding visualization/dashboards
- Implementing backtesting strategies
- Fixing data quality issues
- Publishing to PyPI
- Creating GitHub Pages documentation

---

**Last Updated:** November 6, 2025  
**Project Status:** Production Ready (v1.0.0)  
**Repository:** https://github.com/lieblm/thanksgiving-alpha  
**Author:** Martin Liebl (lieblm@gmail.com)

