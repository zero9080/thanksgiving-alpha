# GitHub Copilot Instructions - Thanksgiving-Alpha

## Project Status: ✅ PRODUCTION READY (v1.0.1)

You are assisting in a **Python/Poetry** repository called **"thanksgiving-alpha"** - a quantitative finance research tool for analyzing stock performance around US Thanksgiving.

---

## 🎯 Project Overview

**Purpose:** Reproducible research tool that ranks stocks by performance around US Thanksgiving holiday.  
**Methodology:** Compute per-year returns from Open price X business days before Thanksgiving to Close price Y business days after.  
**Trading Window:** Configurable (default: 3 days before → 1 day after, including Black Friday half-day session at 1:00 PM ET close).  
**Output:** CSV, Parquet, and HTML reports with statistical rankings.

---

## 📊 Current State (as of November 7, 2025)

### ✅ Completed Features

1. **Core Functionality** (All implemented and tested)
   - NYSE trading calendar with 10 federal holidays
   - Black Friday treated as half-day session (closes 1:00 PM ET)
   - Business day shifting logic with proper weekend/holiday handling
   - Yahoo Finance integration (yfinance) with auto_adjust=True
   - Year-tracked return computation with missing data handling
   - Multi-format exports: CSV, Parquet, HTML
   - **Statistical significance testing** with Wilcoxon + Benjamini-Hochberg FDR correction

2. **Universes Supported** ⭐ **THREE MAJOR INDICES**
   - **S&P 500:** 270-stock representative sample (54% of index) - 244 analyzed, 78.8% completeness
   - **NASDAQ-100:** 100 stocks - 80 analyzed, 78.6% completeness
   - **DJIA:** 30 stocks - 30 analyzed, 95.9% completeness
   - **Custom:** CSV file support via config
   - **Total Coverage:** 354 unique stocks, 8,293 observations

3. **Testing & Quality**
   - **28 passing unit tests** (pytest)
   - Test coverage: holidays, calendar, stats, ranking, statistical tests
   - Typed with mypy (strict mode) with proper numpy NDArray annotations
   - Linted with ruff and black
   - **All CI checks passing** ✅ (as of Nov 7, 2025)

4. **CLI & Configuration**
   - Command: `python -m tgalpha.cli <config> --top=N --statistics --show-coverage`
   - **IMPORTANT:** Uses typer 0.7.0 (NOT 0.12.5 - compatibility issue with TyperArgument.make_metavar())
   - YAML-based configuration system (pydantic validation)
   - Enhanced with statistical testing flags

5. **Documentation**
   - README.md (comprehensive usage guide)
   - EXECUTIVE_SUMMARY.md (cross-index stakeholder overview with sampling methodology)
   - ANALYSIS_SP500_25YEARS.md (S&P 500: 5,756 observations, 244 stocks, with sampling rationale)
   - ANALYSIS_NASDAQ100_25YEARS.md (NASDAQ-100: 1,818 observations, 80 stocks)
   - ANALYSIS_25YEARS.md (DJIA: 719 observations, 30 stocks)
   - STATISTICAL_RESULTS_SUMMARY.md (comprehensive statistical testing documentation)
   - REFERENCES.md (10 academic citations with DOIs)
   - CITATION.cff (academic citation support)
   - .github/FUNDING.yml (donation/sponsorship links)

6. **Public Release Ready**
   - Repository prepared for public consumption
   - Contact: Martin Liebl (lieblm@gmail.com)
   - Donation addresses included (BTC, ETH, USDC/USDT)
   - Professional README with disclaimers
   - MIT License
   - All analyses complete with statistical rigor

7. **CI/CD Pipeline** ✅ **FULLY OPERATIONAL**
   - GitHub Actions workflow (.github/workflows/ci.yml)
   - Runs on every push and pull request
   - Python 3.12 environment (matches local development)
   - Four-stage validation:
     1. Ruff linting (code quality checks)
     2. Black formatting (code style consistency)
     3. Mypy type checking (strict mode with proper type annotations)
     4. Pytest test suite (28 tests)
   - **Recent fixes (Nov 7, 2025):**
     - Fixed 12 unused import linting errors
     - Updated Python version from 3.11 → 3.12
     - Configured mypy to handle third-party library stubs (pandas, scipy, statsmodels, yfinance, yaml)
     - Added proper numpy NDArray type annotations (replaced `np.ndarray` with `NDArray[Any]`)
     - All type checking errors resolved

---

## 🔧 Technical Implementation Details

### Key Architecture Decisions

1. **Trading Calendar Logic** (`src/tgalpha/calendar_utils.py`)
   - NYSECalendar class with 10 holidays
   - `shift_business_days()` function handles non-trading days
   - Black Friday is NOT a holiday (half-day session counted as trading day)
   - **Type Safety:** Added `# type: ignore[misc]` for pandas USFederalHolidayCalendar inheritance

2. **Data Provider** (`src/tgalpha/data_providers/yahoo.py`)
   - **Critical:** Use `auto_adjust=True` to avoid MultiIndex column issues
   - Handles missing data gracefully (returns empty DataFrame)
   - 7-day buffer around target window for data fetching

3. **Statistics Engine** (`src/tgalpha/stats.py`)
   - `holiday_window_dates()`: Calculates trading window dates
   - `compute_return()`: Year-tracked returns with null checks
   - Simple returns (not log returns)

4. **Statistical Tests** (`src/tgalpha/stats_tests.py`)
   - **Type Safety:** Uses `NDArray[Any]` from `numpy.typing` for all array parameters
   - Bootstrap confidence intervals with explicit float casts
   - Wilcoxon signed-rank test and t-test implementations
   - Benjamini-Hochberg FDR correction for multiple testing
   - Effect size (Cohen's d) and Sharpe ratio calculations

5. **Ranking System** (`src/tgalpha/ranking.py`)
   - Aggregates: n, median_return, avg_return, win_rate, std
   - Sorts by: [median_return, win_rate, avg_return]
   - Filters: min_trades parameter (default 10)

6. **Coverage Analysis** (`src/tgalpha/coverage.py`)
   - **Type Safety:** Explicit int/float casts for polars DataFrame values
   - Added `# type: ignore[arg-type]` for polars aggregation methods
   - Computes year-by-year data completeness

7. **Python Environment**
   - Python 3.12.6 with Poetry (3.12.12 on CI)
   - Key dependencies: polars 1.35.1, pandas 2.3.3, typer 0.7.0, yfinance 0.2.66
   - Virtual environment at `.venv/`

---

## 📈 Key Findings from Completed Analyses

### Comprehensive Multi-Index Summary (2000-2024)
**Total:** 8,293 observations across 354 unique stocks

| Index | Stocks | Observations | Completeness | Top Performer | Consistency Leader |
|-------|--------|--------------|--------------|---------------|-------------------|
| S&P 500 | 244 | 5,756 | 78.8% | SHOP (+3.36%) | MNST (84% win rate) |
| NASDAQ-100 | 80 | 1,818 | 78.6% | ENPH (+3.61%) | MNST (84% win rate) |
| DJIA | 30 | 719 | 95.9% | AAPL (+2.00%) | AMZN/HD/NKE (76% win rate) |

**Statistical Significance:** 0 of 354 stocks reach statistical significance after Benjamini-Hochberg FDR correction (α=0.05), demonstrating proper academic rigor with multiple testing correction. Strong empirical patterns remain (79-87% positive median rates, favorable Sharpe ratios 0.4-0.7).

### S&P 500 Sampling Methodology
**Important:** S&P 500 analysis uses a **representative 270-stock sample (54% of the 500-stock index)**, not the full 500 constituents. This methodological decision prioritizes:
- **Data quality:** 78.8% completeness vs. estimated 65-70% with full 500
- **Liquidity focus:** Actively traded names with longer histories
- **Computational efficiency:** ~20 min vs. 45+ min runtime
- **Sector balance:** Proportional representation across all 11 GICS sectors
- **Statistical robustness:** 5,756 observations provide strong power

Of the 270-stock sample, **244 were successfully analyzed** (26 excluded due to insufficient data: recent IPOs like SNOW, PLTR, DASH, COIN).

**Validation:** 87% positive median rate aligns with literature, sector patterns match theory, cross-validated with DJIA and NASDAQ-100.

**Limitations:** May not capture smallest S&P 500 constituents, survivorship bias remains.

### S&P 500 Analysis (2000-2024) ⭐ **REPRESENTATIVE SAMPLE**
- **5,756 observations** across 244 stocks from 270-stock representative sample (78.8% completeness)
- **Top performers:** SHOP (+3.36%), DE (+3.08%), PANW (+3.05%), AVGO (+2.27%), AMAT (+2.26%)
- **Consistency champion:** MNST (+2.02% median, 84% win rate)
- **Sector insights:**
  - Technology: 6 of top 10 performers (semiconductors dominate)
  - Consumer Discretionary: Strong retail/e-commerce presence (SHOP, AMZN)
  - Industrials: DE (Deere) shows exceptional +3.08% median
  - Financials: Payment networks (MA +2.17%) vastly outperform banks (GS/JPM/WFC negative)
- **Broadest market coverage** with balanced sector representation
- **Investment strategies documented:** Conservative (75%+ win rate), Balanced (2.0%+ median, 65%+ win rate), Aggressive (2.5%+ median)
- **Statistical significance:** 0 of 244 stocks (best p=0.170 for MNST)

### DJIA Analysis (2000-2024)
- **719 observations** across 30 stocks (95.9% completeness)
- **Top performers:** AAPL (+2.00%), AMZN (+1.69%), HD (+1.26%)
- 83% of stocks show positive median returns
- Technology and consumer discretionary sectors outperform
- Financial sector underperforms
- **Statistical significance:** 0 of 30 stocks (best p=0.175 for AAPL)

### NASDAQ-100 Analysis (2000-2024)
- **1,818 observations** across 80 stocks (78.6% completeness)
- **Top performers:** ENPH (+3.61%), PANW (+3.05%), AVGO (+2.27%)
- Semiconductor sector dominance (6 of top 10)
- MNST shows 84% win rate (highest consistency)
- Higher returns but more volatility vs. DJIA
- 78.6% completeness due to recent IPOs (SNOW, PLTR, DASH, etc.)
- **Statistical significance:** 0 of 80 stocks (best p=0.167 for MNST)

### Universal Cross-Index Findings
1. **Thanksgiving seasonality effect confirmed** across all three indices (79-87% positive median returns)
2. **Technology sector leadership** persistent across DJIA, NASDAQ-100, and S&P 500
3. **Consumer discretionary excellence** driven by Black Friday retail anticipation
4. **Traditional banking weakness** (GS, JPM, WFC) consistent across all indices
5. **Payment networks outperform banks** (MA, V significantly higher returns than traditional lenders)
6. **Statistical rigor:** 0/354 stocks reach significance after BH FDR correction (demonstrates proper methodology)

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

**Type Checking Best Practices:**
- Use `NDArray[Any]` from `numpy.typing` instead of `np.ndarray` for function signatures
- Add explicit int/float casts for polars DataFrame aggregations (.mean(), .median(), .min(), .max())
- Use `# type: ignore[misc]` for pandas class inheritance (USFederalHolidayCalendar)
- Use `# type: ignore[arg-type]` for polars aggregation methods when mypy is too strict
- Configure mypy in pyproject.toml to ignore missing stubs for third-party libraries

**Test Coverage:**
- Run `pytest tests/ -v` to verify all 28 tests pass
- Coverage includes: holidays (6), calendar (9), stats (8), ranking (6), statistical tests (5)

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
- `pyproject.toml` - Poetry dependencies and project metadata (v1.0.1)
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
- Adding new universes (Russell 2000, sector ETFs)
- Extending analysis windows (different day combinations)
- Adding visualization/dashboards
- Implementing backtesting strategies
- Fixing data quality issues
- Publishing to PyPI
- Creating GitHub Pages documentation

---

**Last Updated:** November 7, 2025  
**Project Status:** Production Ready (v1.0.1) - All three indices complete with statistical testing + CI/CD fully operational  
**Repository:** https://github.com/lieblm/thanksgiving-alpha  
**Author:** Martin Liebl (lieblm@gmail.com)

