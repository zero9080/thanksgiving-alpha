## Academic References

### Holiday Effects in Financial Markets

1. **Lakonishok, J., & Smidt, S. (1988)**  
   "Are Seasonal Anomalies Real? A Ninety-Year Perspective"  
   *Review of Financial Studies*, 1(4), 403-425.  
   [DOI: 10.1093/rfs/1.4.403](https://doi.org/10.1093/rfs/1.4.403)  
   - Seminal study documenting calendar anomalies including holiday effects
   - Found significant positive returns around major US holidays
   - 90-year analysis from 1897-1986

2. **Ariel, R. A. (1990)**  
   "High Stock Returns Before Holidays: Existence and Evidence on Possible Causes"  
   *Journal of Finance*, 45(5), 1611-1626.  
   [DOI: 10.1111/j.1540-6261.1990.tb03731.x](https://doi.org/10.1111/j.1540-6261.1990.tb03731.x)  
   - Documents pre-holiday effect across multiple holidays
   - Thanksgiving identified as strong positive effect
   - Discusses possible behavioral explanations

3. **Brockman, P., & Michayluk, D. (1998)**  
   "The Persistent Holiday Effect: Additional Evidence"  
   *Applied Economics Letters*, 5(4), 205-209.  
   [DOI: 10.1080/135048598354813](https://doi.org/10.1080/135048598354813)  
   - Confirms holiday effect persists through 1990s
   - Tests robustness across different time periods
   - Examines whether effect has diminished over time

4. **Cao, M., & Wei, J. (2005)**  
   "Stock Market Returns: A Note on Temperature Anomaly"  
   *Journal of Banking & Finance*, 29(6), 1559-1573.  
   [DOI: 10.1016/j.jbankfin.2004.06.028](https://doi.org/10.1016/j.jbankfin.2004.06.028)  
   - Explores mood and sentiment factors in seasonal patterns
   - Relevant for understanding Thanksgiving optimism effect
   - Connects weather/seasonal patterns to returns

### Statistical Methods for Financial Research

5. **Benjamini, Y., & Hochberg, Y. (1995)**  
   "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing"  
   *Journal of the Royal Statistical Society: Series B*, 57(1), 289-300.  
   [DOI: 10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x)  
   - FDR correction method used in this analysis
   - Less conservative than Bonferroni for financial applications
   - Widely adopted in quantitative finance research

6. **Efron, B., & Tibshirani, R. J. (1994)**  
   *An Introduction to the Bootstrap*  
   Chapman & Hall/CRC Monographs on Statistics & Applied Probability.  
   ISBN: 978-0412042317  
   - Bootstrap confidence intervals methodology
   - Non-parametric inference for financial returns
   - Standard reference for uncertainty quantification

### Market Microstructure and Trading Costs

7. **Hasbrouck, J. (2009)**  
   "Trading Costs and Returns for U.S. Equities: Estimating Effective Costs from Daily Data"  
   *Journal of Finance*, 64(3), 1445-1477.  
   [DOI: 10.1111/j.1540-6261.2009.01469.x](https://doi.org/10.1111/j.1540-6261.2009.01469.x)  
   - Methods for estimating transaction costs from market data
   - Relevant for understanding gross vs. net returns
   - Informs realistic implementation costs

8. **Frazzini, A., Israel, R., & Moskowitz, T. J. (2018)**  
   "Trading Costs"  
   *Financial Analysts Journal*, 74(2), 1-22.  
   [DOI: 10.2469/faj.v74.n2.1](https://doi.org/10.2469/faj.v74.n2.1)  
   - Comprehensive analysis of actual trading costs
   - Distinction between gross and net returns
   - Important for evaluating strategy profitability

### Survivorship Bias

9. **Brown, S. J., Goetzmann, W. N., & Ross, S. A. (1995)**  
   "Survival"  
   *Journal of Finance*, 50(3), 853-873.  
   [DOI: 10.1111/j.1540-6261.1995.tb04039.x](https://doi.org/10.1111/j.1540-6261.1995.tb04039.x)  
   - Quantifies survivorship bias in stock return studies
   - Demonstrates magnitude of bias (typically 0.5-1.5% annually)
   - Methods for correcting bias using historical constituent data

10. **Elton, E. J., Gruber, M. J., & Blake, C. R. (1996)**  
    "Survivorship Bias and Mutual Fund Performance"  
    *Review of Financial Studies*, 9(4), 1097-1120.  
    [DOI: 10.1093/rfs/9.4.1097](https://doi.org/10.1093/rfs/9.4.1097)  
    - Classic reference on survivorship bias
    - Applicable to index constituent analyses
    - Methodology for bias adjustment

---

## Data Sources

**Market Data:**
- Yahoo Finance API via yfinance library (v0.2.50+)
- OHLC prices with automatic adjustment for splits and dividends
- [https://finance.yahoo.com/](https://finance.yahoo.com/)

**Trading Calendar:**
- NYSE official holiday schedule (10 federal holidays)
- pandas_market_calendars for business day calculations
- Federal Reserve holiday calendar cross-reference

**Index Constituents:**
- S&P 500, NASDAQ-100, DJIA as of November 2025
- Sources: S&P Dow Jones Indices, Nasdaq.com, DJIA official website
- Note: Historical changes in constituents not reflected (survivorship bias present)

---

## Citation

If you use this analysis in academic research, please cite:

```bibtex
@software{liebl2025thanksgiving,
  author = {Liebl, Martin},
  title = {Thanksgiving-Alpha: Quantitative Analysis of US Thanksgiving Seasonality},
  year = {2025},
  version = {1.0.0},
  url = {https://github.com/lieblm/thanksgiving-alpha},
  note = {Analysis of 390 stocks across S\&P 500, NASDAQ-100, and DJIA indices (2000-2024)}
}
```

For questions or collaboration inquiries, contact: lieblm@gmail.com
