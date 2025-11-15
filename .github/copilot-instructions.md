# Thanksgiving-Alpha - AI Assistant Instructions

**CRITICAL:** AI assistant's primary reference for session continuity.  
**Audience:** Claude Sonnet 4.5 / GitHub Copilot  
**Purpose:** Prevent repeated mistakes, maintain context, enforce best practices  
**For Humans:** See README.md or EXECUTIVE_SUMMARY.md

---
**Metadata:**
- Version: 2.0
- Last Updated: 2025-11-15
- Production Version: 1.0.1
- Language: Python 3.12
- Package Manager: Poetry
---

## ⚡ [P0] CORE COLLABORATION PRINCIPLES

**TRIGGER:** Every interaction with user  
**VIOLATION CONSEQUENCE:** Loss of trust, broken git history, chaos

### Rule #1: Test-First Workflow
**NEVER COMMIT OR PUSH UNTESTED CODE**

**Process (NO EXCEPTIONS):**
```
1. AI: Make code changes
2. AI: "Run these tests: pytest tests/test_X.py -v"
3. USER: Execute tests → confirm results
4. USER: Reply "OK" or describe problem
5. AI: ONLY after "OK" → git commit && git push
```

**Violations to Prevent:**
- ❌ Commit before user confirms tests pass
- ❌ Skip test execution for "small" changes
- ❌ Assume changes work without explicit confirmation
- ❌ Push code that breaks CI pipeline

**Reason:** Untested code in git history = broken builds = wasted time

---

### Rule #2: Work is Sequential Dialog
**NO PARALLEL WORK - WAIT FOR EACH OTHER**

**Correct Pattern:**
```
AI: Propose change A
USER: Execute A → confirm
AI: Propose change B
USER: Execute B → confirm
```

**Incorrect Pattern:**
```
❌ AI: "Do X. Meanwhile I'll do Y..."
❌ Multiple instructions without waiting
❌ "While you do that, I'll..."
```

**Reason:** Parallel work = lost context, conflicting changes, confusion

---

### Rule #3: Respect Task Order
**MULTIPLE TASKS = ONE AT A TIME, PRESERVE ORDER**

**When user provides numbered list:**
```
User: "1. Change X, 2. Add Y, 3. Test Z"

→ Implement 1 ONLY
→ Wait for confirmation
→ Then implement 2
→ Wait for confirmation
→ Then implement 3
```

**Exception:** If different order is more efficient:
```
→ STOP and ASK: "Would it be better to do 2 before 1 because [reason]?"
→ Wait for user decision
→ Then proceed
```

**Reason:** User's order may have dependencies AI doesn't understand

---

## 🔴 [P0] CRITICAL CONSTRAINTS - NEVER VIOLATE

### Python & Poetry Configuration
**TRIGGER:** Any package installation, version changes, or dependency updates

```yaml
CORRECT:
  python: 3.12.6 (local), 3.12.12 (CI)
  package_manager: Poetry
  virtual_env: .venv/
  dependencies: pyproject.toml (version 1.0.1)
  
CRITICAL_VERSIONS:
  typer: ^0.12.3 (with [all] extras)
  yfinance: auto_adjust=True REQUIRED
  polars: ^1.9.0
  
TYPE_SAFETY:
  numpy_arrays: NDArray[Any] from numpy.typing
  polars_casts: Explicit int()/float() for aggregations
  mypy: Strict mode with third-party library overrides
```

**Why Critical:** Wrong yfinance usage = MultiIndex issues, missing type annotations = CI fails

---

## 📊 Current State (as of November 15, 2025)

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

## 📋 [P1] TECHNICAL REFERENCE

**Query This Section:** When writing code, checking file paths, understanding architecture

### Project Structure
```
/Users/lieblm/Documents/GitHub/thanksgiving-alpha/
├── .github/
│   ├── workflows/ci.yml          # CI/CD pipeline
│   ├── copilot-instructions.md   # THIS FILE
│   └── FUNDING.yml               # Donation links
├── configs/
│   ├── djia_25years.yaml         # DJIA 2000-2024
│   ├── nasdaq100_25years.yaml    # NASDAQ-100 2000-2024
│   ├── sp500_25years.yaml        # S&P 500 2000-2024 (270-stock sample)
│   └── test_small.yaml           # 5-year test config
├── src/tgalpha/
│   ├── cli.py                    # Typer CLI
│   ├── universe.py               # Stock lists (DJIA/NASDAQ/SP500)
│   ├── calendar_utils.py         # NYSE calendar + business day logic
│   ├── holidays.py               # Thanksgiving date calculation
│   ├── stats.py                  # Window dates + return computation
│   ├── stats_tests.py            # Wilcoxon + BH FDR correction
│   ├── ranking.py                # Aggregation + sorting
│   ├── report.py                 # CSV/Parquet/HTML exports
│   ├── coverage.py               # Data completeness analysis
│   └── data_providers/
│       ├── base.py               # Abstract provider interface
│       └── yahoo.py              # Yahoo Finance (auto_adjust=True)
├── tests/
│   ├── test_holidays.py          # 6 tests
│   ├── test_calendar_utils.py    # 9 tests
│   ├── test_stats.py             # 8 tests
│   └── test_ranking.py           # 6 tests
├── pyproject.toml                # Poetry config (v1.0.1)
├── README.md                     # Main documentation
├── EXECUTIVE_SUMMARY.md          # Stakeholder overview
└── LICENSE                       # MIT License
```

### Key Architecture Components

#### Trading Calendar (`calendar_utils.py`)
```python
class NYSECalendar:
    """10 federal holidays, NO Black Friday"""
    
def shift_business_days(date, days, calendar):
    """Handles weekends + holidays + direction"""
    # Black Friday = trading day (half-day session)
```

**Type Safety Note:** Uses `# type: ignore[misc]` for pandas USFederalHolidayCalendar inheritance

#### Data Provider (`yahoo.py`)
```python
def get_ohlc(symbol, start_date, end_date):
    # CRITICAL: auto_adjust=True
    data = yf.download(symbol, start=start, end=end, auto_adjust=True)
    # Avoids MultiIndex columns
    # 7-day buffer around window
```

#### Statistics (`stats.py` + `stats_tests.py`)
```python
# stats.py
def holiday_window_dates(year, days_before, days_after, calendar):
    """Calculates trading window around Thanksgiving"""
    
def compute_return(data, open_date, close_date):
    """Year-tracked returns with null checks"""
    # Simple returns: (close / open - 1) * 100

# stats_tests.py (NDArray[Any] for type safety)
def wilcoxon_test(returns: NDArray[Any]) -> Tuple[float, float]:
    """Wilcoxon signed-rank test"""
    
def benjamini_hochberg_correction(p_values: NDArray[Any], alpha: float):
    """BH FDR correction for multiple testing"""
```

### Known Limitations
```yaml
data_limitations:
  survivorship_bias: Using present-day constituents
  recent_ipos: Insufficient history (SNOW, PLTR, DASH, COIN, ARM)
  yahoo_errors: Some stocks have timezone issues (BRK.B, HES, MRO)
  
sp500_sampling:
  current: 270-stock representative sample (54% of index)
  rationale: Data quality (78.8%) vs full 500 (~65-70%)
  runtime: ~20 min vs 45+ min for full 500
  trade_off: Liquidity focus, may miss smallest constituents
  
statistical:
  sample_size: n=23-25 observations per stock
  significance: 0/354 stocks after BH FDR correction
  interpretation: Proper academic rigor, not absence of effect
```

---

## 🔀 [P2] DECISION TREES

**Query This Section:** When encountering common problems

### When Tests Fail

```
START: pytest shows failures

├─ Type checking errors (mypy)?
│  ├─ numpy.ndarray → Use NDArray[Any] from numpy.typing
│  ├─ polars aggregations → Add explicit int()/float() casts
│  └─ pandas inheritance → Add # type: ignore[misc]

├─ Data quality issues?
│  ├─ Check Yahoo Finance response (empty DataFrame?)
│  ├─ Verify auto_adjust=True in yfinance call
│  └─ Test with test_small.yaml (5-year window)

├─ Calendar logic errors?
│  ├─ Black Friday counted correctly? (half-day = trading day)
│  ├─ Weekend shifts working? (shift_business_days)
│  └─ Holiday detection accurate? (10 federal holidays)

└─ Statistical test issues?
   ├─ Check sample size (n >= 10 for Wilcoxon)
   ├─ Verify return distribution (outliers?)
   └─ BH correction working? (sorted p-values)
```

### When Adding New Universe

```
START: User wants to add Russell 2000, sector ETFs, etc.

├─ Create new list in universe.py
│  ├─ Follow existing pattern (DJIA, NASDAQ100, SP500)
│  ├─ Include stock symbols only
│  └─ Document source and date

├─ Create config file
│  ├─ Copy existing YAML (e.g., djia_25years.yaml)
│  ├─ Update universe name
│  └─ Set appropriate min_trades threshold

├─ Run analysis
│  ├─ Test with small date range first (2020-2024)
│  ├─ Check data completeness
│  └─ Review top 10 performers (sanity check)

└─ Document findings
   ├─ Create ANALYSIS_[UNIVERSE]_[YEARS].md
   └─ Update EXECUTIVE_SUMMARY.md
```

### When to Ask vs Continue

```
ASK USER:
├─ Modifying trading calendar logic
├─ Changing statistical methodology
├─ Adding dependencies (new Python packages)
├─ Altering universe definitions
├─ Unclear requirement or ambiguous request
└─ Multiple valid approaches exist

CONTINUE WITHOUT ASKING:
├─ Obvious syntax error or typo
├─ Following established code pattern
├─ Applying documented best practice
├─ Fixing linting/formatting issues
└─ Git history shows clear precedent
```

---

## 🐛 [P2] TOP 5 COMMON MISTAKES

**Query This Section:** Before implementing similar features

### 1. Wrong Typer Version (OBSOLETE - NOW USING 0.12.3)
**Historical Note:** Version 0.7.0 was previously required due to TyperArgument.make_metavar() compatibility issues. Project now uses typer 0.12.3 with [all] extras as of pyproject.toml update.

---

### 2. Yahoo Finance auto_adjust=False
**Symptom:** MultiIndex columns, KeyError on 'Close' or 'Open'  
**Trigger:** Calling yf.download()

```python
# WRONG
data = yf.download(symbol, start=start, end=end)
# Returns MultiIndex: ('Close', 'AAPL')

# CORRECT
data = yf.download(symbol, start=start, end=end, auto_adjust=True)
# Returns simple columns: 'Close', 'Open'
```

**Prevention:** Grep for `yf.download` before adding new data fetching code

---

### 3. Using np.ndarray Instead of NDArray[Any]
**Symptom:** mypy strict mode errors: "Missing type parameters for generic type"  
**Trigger:** Function signatures with numpy arrays

```python
# WRONG
def wilcoxon_test(returns: np.ndarray) -> dict:
    pass

# CORRECT
from numpy.typing import NDArray
from typing import Any

def wilcoxon_test(returns: NDArray[Any]) -> dict:
    pass
```

**Prevention:** Always import NDArray[Any] from numpy.typing

---

### 4. Not Checking Git History
**Symptom:** Re-implementing existing patterns, breaking working code  
**Trigger:** Before implementing ANY feature

```bash
# Check if feature exists
git log --grep="calendar"
git log --grep="statistical"

# Find similar patterns
git log --all -- src/tgalpha/stats.py

# Understand why it was done
git show <hash>
```

**Rule:** Always search git history before coding

---

### 5. Pushing Untested Code
**Symptom:** CI pipeline fails, broken main branch, wasted time  
**Trigger:** Before git push

```bash
# ALWAYS RUN BEFORE PUSHING:
pytest tests/ -v           # 28 tests must pass
ruff check src/ tests/     # Zero errors
black src/ tests/ --check  # Properly formatted
mypy src/                  # Zero type errors

# THEN AND ONLY THEN:
git push
```

**Rule:** Never push without local validation

---

## 📚 [P2] CODE PATTERNS

**Query This Section:** When implementing similar functionality

### Type Safety Pattern
```python
# Import proper types
from numpy.typing import NDArray
from typing import Any

# Function signatures
def compute_statistic(returns: NDArray[Any]) -> float:
    # Explicit casts for numpy operations
    result = float(np.mean(returns))
    return result

# Polars DataFrame casts
df = pl.DataFrame({"year": [2020, 2021]})
year_value = int(df.filter(pl.col("year") == 2020).select("year").row(0)[0])

# Type ignore comments (when necessary)
class NYSECalendar(USFederalHolidayCalendar):  # type: ignore[misc]
    """Pandas inheritance pattern"""
```

### Testing Pattern
```python
# Test structure
def test_feature_name():
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_value
    assert len(result) > 0
    # Use pytest.approx for floats
    assert result["return"] == pytest.approx(1.5, abs=0.01)
```

### Error Handling Pattern
```python
def fetch_data(symbol: str) -> pl.DataFrame:
    """Fetch data with graceful degradation"""
    try:
        data = yf.download(symbol, ..., auto_adjust=True)
        if data.empty:
            logger.warning(f"No data for {symbol}")
            return pl.DataFrame()
        return convert_to_polars(data)
    except Exception as e:
        logger.error(f"Error fetching {symbol}: {e}")
        return pl.DataFrame()
```

---

## 🎯 [P3] FUTURE ENHANCEMENTS ROADMAP

**Query This Section:** When user asks "what's next" or "what could we add"

### Phase 1: Extended Universes (Priority)
- ✅ **S&P 500** - COMPLETE (5,756 observations, 244 stocks from 270-stock sample)
- ✅ **NASDAQ-100** - COMPLETE (1,818 observations, 80 stocks)
- ✅ **DJIA** - COMPLETE (719 observations, 30 stocks)
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

## 🔍 [P3] QUICK COMMANDS

**Query This Section:** When needing specific commands

### Git Commands
```bash
# Recent changes
git log --oneline -20
git log --since="2025-11-01" --pretty=format:"%h - %an, %ar : %s"

# Search commits
git log --grep="statistical"
git log --all -- src/tgalpha/stats.py

# View specific commit
git show <hash>
git show --stat <hash>

# Compare versions
git diff v1.0.0 v1.0.1
git diff <hash1> <hash2> -- src/tgalpha/

# Investigate
git blame src/tgalpha/calendar_utils.py
```

### Poetry Commands
```bash
# Install dependencies
poetry install

# Add package
poetry add package-name

# Update packages
poetry update

# Show installed packages
poetry show --tree

# Activate virtual environment
poetry shell
```

### Testing & Quality
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_holidays.py -v

# Run with coverage
pytest tests/ --cov=src/tgalpha --cov-report=term-missing

# Linting
ruff check src/ tests/
ruff check . --fix  # Auto-fix

# Formatting
black src/ tests/
black src/ tests/ --check  # Check only

# Type checking
mypy src/
```

### Analysis Commands
```bash
# Run analysis
python -m tgalpha.cli configs/sp500_25years.yaml --top=50

# With statistical tests
python -m tgalpha.cli configs/nasdaq100_25years.yaml --statistics

# With coverage report
python -m tgalpha.cli configs/djia_25years.yaml --show-coverage
```

---

## ✅ [P3] SESSION START CHECKLIST

**Execute at start of EVERY session:**

```yaml
step_1_read_principles:
  action: Read CORE COLLABORATION PRINCIPLES section
  why: Never violate test-first workflow or sequential work rules
  
step_2_check_changes:
  action: git log --oneline -10
  why: Understand what changed since last session
  
step_3_check_status:
  action: Read CURRENT STATE section
  why: Know what's completed vs in progress
  
step_4_user_context:
  if_user_says_continue:
    action: ASK "What should we work on?"
    why: Don't assume what user wants to prioritize
```

**Before making ANY code changes:**

```yaml
step_1_check_history:
  action: git log --grep="feature-name"
  why: Don't re-implement existing patterns
  
step_2_read_file:
  action: Read entire file you'll modify
  why: Understand current implementation
  
step_3_check_tests:
  action: Find related tests in tests/ directory
  why: Know what test coverage exists
  
step_4_ask_if_unclear:
  action: ASK user for clarification
  why: Don't guess or assume
```

**After making changes:**

```yaml
step_1_request_test:
  action: Say "Run tests: pytest tests/test_X.py -v"
  why: Explicit test command for user
  
step_2_wait:
  action: WAIT for user confirmation
  do_not: Continue to next task, commit code, assume success
  
step_3_validate:
  when: User confirms tests pass
  action: Request full validation (ruff, black, mypy)
  
step_4_commit:
  when: All checks pass
  action: git commit with detailed message
  message_must_include: WHY, WHAT, HOW, TESTED confirmation
```

---

## 📍 METADATA FOOTER

```yaml
document:
  version: 2.0
  last_updated: 2025-11-15
  optimized_for: Claude Sonnet 4.5
  structure: Priority-based with decision trees
  
production:
  version: 1.0.1
  status: Production Ready
  repository: https://github.com/lieblm/thanksgiving-alpha
  
package_ecosystem:
  language: Python 3.12.6 (3.12.12 on CI)
  package_manager: Poetry
  virtual_env: .venv/
  key_dependencies: polars, pandas, yfinance, typer@0.12.3
  
ci_cd:
  platform: GitHub Actions
  workflow: .github/workflows/ci.yml
  stages: [ruff, black, mypy, pytest]
  test_count: 28
  status: All passing
  
contact:
  author: Martin Liebl
  email: lieblm@gmail.com
  for_humans: See README.md or EXECUTIVE_SUMMARY.md
```

---

**END OF AI INSTRUCTIONS**

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

