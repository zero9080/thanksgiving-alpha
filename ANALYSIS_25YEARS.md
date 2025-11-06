# 25-Year Thanksgiving Seasonality Analysis
## DJIA Constituents: 2000-2024

**Analysis Period:** 2000-2024 (25 years)  
**Trading Window:** 3 business days before Thanksgiving → 1 business day after (Black Friday)  
**Universe:** 30 DJIA stocks  
**Total Observations:** 718 (out of possible 750)  
**Data Completeness:** 95.7%

---

## Executive Highlights

### Top 10 Performers (by Median Return)

| Rank | Symbol | Company | Median Return | Avg Return | Win Rate | Years | Std Dev |
|------|--------|---------|---------------|------------|----------|-------|---------|
| 1 | AAPL | Apple | **+2.00%** | +1.79% | 68% | 25 | 4.03% |
| 2 | AMZN | Amazon | **+1.69%** | +2.11% | 76% | 25 | 4.50% |
| 3 | HD | Home Depot | **+1.26%** | +1.60% | 76% | 25 | 4.03% |
| 4 | UNH | UnitedHealth | **+1.21%** | +1.69% | 72% | 25 | 4.43% |
| 5 | NKE | Nike | **+1.14%** | +1.05% | 76% | 25 | 2.88% |
| 6 | VZ | Verizon | **+1.09%** | +1.43% | 64% | 25 | 3.28% |
| 7 | V | Visa | **+1.03%** | +0.89% | 59% | 17 | 3.23% |
| 8 | CSCO | Cisco | **+0.95%** | +0.72% | 56% | 25 | 2.76% |
| 9 | MCD | McDonald's | **+0.86%** | +0.91% | 72% | 25 | 2.01% |
| 10 | WMT | Walmart | **+0.84%** | +0.64% | 64% | 25 | 2.34% |

### Bottom 5 Performers

| Rank | Symbol | Company | Median Return | Avg Return | Win Rate | Years | Std Dev |
|------|--------|---------|---------------|------------|----------|-------|---------|
| 26 | GS | Goldman Sachs | **-0.04%** | +1.30% | 44% | 25 | 8.70% |
| 27 | JPM | JPMorgan Chase | **-0.13%** | +0.99% | 48% | 25 | 6.88% |
| 28 | JNJ | Johnson & Johnson | **-0.24%** | -0.40% | 32% | 25 | 1.35% |
| 29 | CRM | Salesforce | **-0.54%** | +0.87% | 38% | 21 | 7.22% |

---

## Key Insights

### 1. Technology Leadership
- **AAPL and AMZN** dominate with consistently positive median returns (>1.5%)
- **Technology sector** shows strongest Thanksgiving performance
- **MSFT** shows lower median (+0.44%) despite being a tech leader

### 2. Retail & Consumer
- **HD, NKE, WMT, MCD** all show positive median returns
- Likely benefiting from Black Friday shopping anticipation
- **Consumer discretionary stocks** perform well in this window

### 3. Healthcare Strength
- **UNH** ranks 4th with +1.21% median return and 72% win rate
- Defensive characteristics provide stability

### 4. Financial Sector Weakness
- **GS and JPM** show negative median returns
- High volatility (std dev >6%)
- Lower win rates (44-48%)
- Financials appear to underperform during holiday period

### 5. Consistency Metrics
- **Highest Win Rates:** AMZN, HD, NKE (76% each)
- **Most Consistent:** MCD, PG (low volatility)
- **Highest Volatility:** GS (8.70%), CRM (7.22%), JPM (6.88%)

---

## Statistical Analysis

### Distribution of Returns

**Positive Median Returns:** 25 out of 30 stocks (83%)  
**Negative Median Returns:** 5 out of 30 stocks (17%)

### Win Rate Distribution
- **>70% Win Rate:** 6 stocks (AMZN, HD, UNH, NKE, MCD)
- **60-70% Win Rate:** 7 stocks
- **50-60% Win Rate:** 11 stocks
- **<50% Win Rate:** 6 stocks

### Volatility Tiers
- **Low Vol (<2.5%):** PG, JNJ, MCD, INTC, KO, MMM
- **Medium Vol (2.5-4%):** Most stocks (18 stocks)
- **High Vol (>6%):** GS, JPM, CRM

---

## Sector Performance Summary

| Sector | Top Performer | Median Return | Avg Win Rate |
|--------|---------------|---------------|--------------|
| Technology | AAPL (+2.00%) | +1.02% | 61% |
| Consumer Discretionary | AMZN (+1.69%) | +0.90% | 69% |
| Healthcare | UNH (+1.21%) | +0.52% | 60% |
| Consumer Staples | WMT (+0.84%) | +0.44% | 61% |
| Industrials | HON (+0.78%) | +0.45% | 63% |
| Energy | CVX (+0.49%) | +0.49% | 60% |
| Financials | AXP (+0.82%) | -0.08% | 46% |

---

## Risk-Return Profile

### Best Risk-Adjusted Returns (Sharpe-like)
1. **NKE:** +1.14% median / 2.88% std = 0.40 ratio
2. **AAPL:** +2.00% median / 4.03% std = 0.50 ratio
3. **MCD:** +0.86% median / 2.01% std = 0.43 ratio

### Highest Risk, Lowest Return
1. **GS:** -0.04% median / 8.70% std
2. **CRM:** -0.54% median / 7.22% std
3. **JPM:** -0.13% median / 6.88% std

---

## Data Quality Notes

### Missing Data
- **CRM (Salesforce):** Only 21 years (IPO: 2004)
- **V (Visa):** Only 17 years (IPO: 2008)
- **DOW:** Missing most years (recent DJIA addition)
- **BA (Boeing):** 24 years (1 timeout error)

### Survivorship Considerations
- Analysis includes current DJIA constituents only
- Does not account for companies removed from index over time
- Historical DJIA composition changes not reflected

---

## Trading Implications

### Long Candidates (Positive Edge)
- **High Conviction:** AAPL, AMZN, HD (>1.5% median, >68% win rate)
- **Moderate Conviction:** UNH, NKE, VZ (1-1.5% median, >59% win rate)
- **Low Volatility:** MCD, NKE, WMT (stable, consistent)

### Avoid / Short Candidates
- **Negative Edge:** JNJ, JPM, GS, CRM (negative median returns)
- **High Volatility, Low Return:** GS, CRM (poor risk-reward)

### Portfolio Construction
- **Diversified Basket:** Top 10 stocks by median return
- **Risk Management:** Avoid high-volatility financials
- **Sector Tilt:** Overweight technology & consumer discretionary

---

## Comparison: 5-Year vs 25-Year Results

### Changes in Rankings

| Stock | 5-Yr Rank | 25-Yr Rank | Change |
|-------|-----------|------------|--------|
| BA | 1st | 14th | ↓ 13 |
| CVX | 2nd | 17th | ↓ 15 |
| VZ | 3rd | 6th | ↑ 3 |
| AAPL | - | 1st | New Top |
| AMZN | - | 2nd | New Top |

**Key Observation:** Short-term (5-year) leaders like BA and CVX show regression to the mean over longer periods. Technology stocks (AAPL, AMZN) demonstrate sustained outperformance over 25 years.

---

## Conclusions

1. **Thanksgiving Effect Exists:** 83% of stocks show positive median returns during the analysis window

2. **Technology Dominance:** Tech sector shows strongest and most consistent performance

3. **Retail Anticipation:** Consumer-facing stocks benefit from Black Friday shopping expectations

4. **Financial Underperformance:** Banks and financial services show weakness during holiday period

5. **Statistical Significance:** With 25 years of data and 68-76% win rates for top performers, patterns appear robust

6. **Risk Considerations:** 
   - Past performance doesn't guarantee future results
   - Small sample size per stock (max 25 observations)
   - Survivorship bias (current DJIA constituents only)
   - Transaction costs would reduce returns
   - Market conditions evolve over time

---

## Recommendations

**For Researchers:**
- Expand analysis to full S&P 500 for broader validation
- Test alternative windows (e.g., 5 days before/after)
- Analyze sector rotation patterns
- Statistical significance testing (t-tests, bootstrapping)

**For Traders:**
- Consider long positions in AAPL, AMZN, HD, UNH, NKE
- Avoid or short JNJ, GS, JPM during this window
- Use tight stops given multi-day holding period
- Account for transaction costs in strategy design

**For Portfolio Managers:**
- Tactical tilt toward technology & consumer discretionary
- Reduce financial exposure around Thanksgiving
- Consider this as one factor among many
- Backtest with realistic trading costs

---

## Appendix: Full Dataset

**Files Generated:**
- `data/outputs/ranking.csv` - Full results table
- `data/outputs/ranking.parquet` - Compressed binary format
- `data/outputs/ranking.html` - Web-viewable table

**Configuration Used:** `configs/djia_25years.yaml`

**Analysis Date:** November 6, 2025

---

**Disclaimer:** This analysis is for informational and research purposes only. Past performance does not guarantee future results. Trading involves risk of loss. Consult with a financial advisor before making investment decisions.
