import polars as pl
from typing import List, Tuple
from tgalpha.stats_tests import (
    bootstrap_confidence_interval,
    wilcoxon_test,
    benjamini_hochberg_correction,
    t_test,
    compute_effect_size,
    sharpe_ratio,
)


def aggregate_per_symbol(
    rows: List[Tuple[str, int, float]],
    min_trades: int = 10,
    compute_statistics: bool = True,
    confidence_level: float = 0.95,
) -> pl.DataFrame:
    """Aggregate returns per symbol and rank them with statistical tests.

    Args:
        rows: List of (symbol, year, return) tuples
        min_trades: Minimum number of observations required to include a symbol
        compute_statistics: Whether to compute bootstrap CIs and significance tests
        confidence_level: Confidence level for bootstrap intervals (default 0.95)

    Returns:
        DataFrame with aggregated statistics, sorted by median_return, win_rate, avg_return

        Columns include:
        - Basic stats: n, median_return, avg_return, win_rate, std
        - Statistical tests (if compute_statistics=True):
          * median_ci_lower, median_ci_upper: Bootstrap 95% CI for median
          * mean_ci_lower, mean_ci_upper: Bootstrap 95% CI for mean
          * p_value_wilcoxon: Wilcoxon signed-rank test p-value (H0: median = 0)
          * p_value_ttest: t-test p-value (H0: mean = 0)
          * p_value_corrected: Benjamini-Hochberg corrected p-value
          * significant: Boolean indicating statistical significance after correction
          * effect_size: Cohen's d effect size
          * sharpe: Sharpe ratio (annualized, assuming 1 trade/year)
    """
    # Create DataFrame from rows
    df = pl.DataFrame(
        {
            "symbol": [r[0] for r in rows],
            "year": [r[1] for r in rows],
            "ret": [r[2] for r in rows],
        }
    )

    # Aggregate by symbol
    by_sym = df.group_by("symbol").agg(
        [
            pl.len().alias("n"),
            pl.median("ret").alias("median_return"),
            pl.mean("ret").alias("avg_return"),
            (pl.col("ret") > 0).mean().alias("win_rate"),
            pl.std("ret").alias("std"),
        ]
    )

    # Filter by minimum trades
    by_sym = by_sym.filter(pl.col("n") >= min_trades)

    if compute_statistics and len(by_sym) > 0:
        # Compute statistical tests for each symbol
        symbols = by_sym["symbol"].to_list()

        # Initialize arrays for statistical results
        median_ci_lower = []
        median_ci_upper = []
        mean_ci_lower = []
        mean_ci_upper = []
        p_values_wilcoxon = []
        p_values_ttest = []
        effect_sizes = []
        sharpe_ratios = []

        for symbol in symbols:
            # Get returns for this symbol
            symbol_returns = df.filter(pl.col("symbol") == symbol)["ret"].to_numpy()

            # Bootstrap confidence intervals
            _, med_lower, med_upper = bootstrap_confidence_interval(
                symbol_returns, statistic="median", confidence_level=confidence_level
            )
            _, mean_lower, mean_upper = bootstrap_confidence_interval(
                symbol_returns, statistic="mean", confidence_level=confidence_level
            )

            # Hypothesis tests
            _, p_wilcoxon = wilcoxon_test(symbol_returns, alternative="greater")
            _, p_ttest = t_test(symbol_returns, alternative="greater")

            # Effect size and risk-adjusted return
            effect_size = compute_effect_size(symbol_returns)
            sharpe = sharpe_ratio(symbol_returns, risk_free_rate=0.0)

            median_ci_lower.append(med_lower)
            median_ci_upper.append(med_upper)
            mean_ci_lower.append(mean_lower)
            mean_ci_upper.append(mean_upper)
            p_values_wilcoxon.append(p_wilcoxon)
            p_values_ttest.append(p_ttest)
            effect_sizes.append(effect_size)
            sharpe_ratios.append(sharpe)

        # Apply Benjamini-Hochberg correction for multiple testing
        reject_array, corrected_p_values = benjamini_hochberg_correction(
            p_values_wilcoxon, alpha=0.05
        )

        # Add statistical columns
        by_sym = by_sym.with_columns(
            [
                pl.Series("median_ci_lower", median_ci_lower),
                pl.Series("median_ci_upper", median_ci_upper),
                pl.Series("mean_ci_lower", mean_ci_lower),
                pl.Series("mean_ci_upper", mean_ci_upper),
                pl.Series("p_value_wilcoxon", p_values_wilcoxon),
                pl.Series("p_value_ttest", p_values_ttest),
                pl.Series("p_value_corrected", corrected_p_values.tolist()),
                pl.Series("significant", reject_array.tolist()),
                pl.Series("effect_size", effect_sizes),
                pl.Series("sharpe", sharpe_ratios),
            ]
        )

    # Sort by median_return, win_rate, avg_return (all descending)
    return by_sym.sort(["median_return", "win_rate", "avg_return"], descending=[True, True, True])
