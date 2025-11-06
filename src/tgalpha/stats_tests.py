"""
Statistical significance tests for holiday window returns.

Provides bootstrap confidence intervals, non-parametric tests,
and multiple testing corrections for robust statistical inference.
"""

from typing import List, Tuple, Optional
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests


def bootstrap_confidence_interval(
    returns: np.ndarray,
    statistic: str = "median",
    n_bootstrap: int = 10000,
    confidence_level: float = 0.95,
    random_seed: Optional[int] = 42
) -> Tuple[float, float, float]:
    """
    Compute bootstrap confidence interval for a statistic.
    
    Args:
        returns: Array of returns
        statistic: "median" or "mean"
        n_bootstrap: Number of bootstrap samples
        confidence_level: Confidence level (default 0.95 for 95% CI)
        random_seed: Random seed for reproducibility
    
    Returns:
        Tuple of (point_estimate, lower_bound, upper_bound)
    """
    if len(returns) == 0:
        return (np.nan, np.nan, np.nan)
    
    rng = np.random.default_rng(random_seed)
    
    # Compute point estimate
    if statistic == "median":
        point_est = np.median(returns)
        stat_func = np.median
    elif statistic == "mean":
        point_est = np.mean(returns)
        stat_func = np.mean
    else:
        raise ValueError(f"Unknown statistic: {statistic}")
    
    # Bootstrap sampling
    bootstrap_stats = np.zeros(n_bootstrap)
    n = len(returns)
    
    for i in range(n_bootstrap):
        sample = rng.choice(returns, size=n, replace=True)
        bootstrap_stats[i] = stat_func(sample)
    
    # Compute confidence interval
    alpha = 1 - confidence_level
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100
    
    lower_bound = np.percentile(bootstrap_stats, lower_percentile)
    upper_bound = np.percentile(bootstrap_stats, upper_percentile)
    
    return (point_est, lower_bound, upper_bound)


def wilcoxon_test(
    returns: np.ndarray,
    alternative: str = "greater"
) -> Tuple[float, float]:
    """
    Wilcoxon signed-rank test for returns vs. zero.
    
    Tests whether median return is significantly different from zero.
    Non-parametric alternative to t-test, robust to outliers.
    
    Args:
        returns: Array of returns
        alternative: "two-sided", "greater" (positive returns), or "less"
    
    Returns:
        Tuple of (statistic, p_value)
    """
    if len(returns) < 10:  # Minimum sample size for reliable test
        return (np.nan, np.nan)
    
    try:
        result = stats.wilcoxon(
            returns,
            alternative=alternative,
            zero_method='wilcox',
            method='auto'
        )
        return (result.statistic, result.pvalue)
    except Exception:
        # Handle cases where all values are zero or other edge cases
        return (np.nan, np.nan)


def t_test(
    returns: np.ndarray,
    alternative: str = "greater"
) -> Tuple[float, float]:
    """
    One-sample t-test for returns vs. zero.
    
    Tests whether mean return is significantly different from zero.
    Assumes approximate normality of return distribution.
    
    Args:
        returns: Array of returns
        alternative: "two-sided", "greater" (positive returns), or "less"
    
    Returns:
        Tuple of (statistic, p_value)
    """
    if len(returns) < 10:
        return (np.nan, np.nan)
    
    result = stats.ttest_1samp(returns, 0.0, alternative=alternative)
    return (result.statistic, result.pvalue)


def benjamini_hochberg_correction(
    p_values: List[float],
    alpha: float = 0.05
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Apply Benjamini-Hochberg FDR correction for multiple testing.
    
    Controls false discovery rate when testing many stocks simultaneously.
    Less conservative than Bonferroni correction.
    
    Args:
        p_values: List of p-values from multiple tests
        alpha: Family-wise error rate (default 0.05)
    
    Returns:
        Tuple of (reject_array, corrected_p_values)
        - reject_array: Boolean array indicating which null hypotheses to reject
        - corrected_p_values: Adjusted p-values
    """
    if len(p_values) == 0:
        return (np.array([]), np.array([]))
    
    # Replace NaN p-values with 1.0 (most conservative)
    p_values_clean = [1.0 if np.isnan(p) else p for p in p_values]
    
    reject, corrected_pvals, _, _ = multipletests(
        p_values_clean,
        alpha=alpha,
        method='fdr_bh'
    )
    
    return (reject, corrected_pvals)


def compute_effect_size(returns: np.ndarray) -> float:
    """
    Compute Cohen's d effect size for returns vs. zero.
    
    Measures magnitude of effect independent of sample size.
    
    Args:
        returns: Array of returns
    
    Returns:
        Cohen's d effect size
        - Small: 0.2
        - Medium: 0.5
        - Large: 0.8+
    """
    if len(returns) == 0:
        return np.nan
    
    mean_return = np.mean(returns)
    std_return = np.std(returns, ddof=1)
    
    if std_return == 0:
        return np.nan
    
    # Cohen's d: (mean - 0) / std
    return mean_return / std_return


def sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.0) -> float:
    """
    Compute annualized Sharpe ratio for strategy.
    
    Measures risk-adjusted return. Assumes ~1 trade per year.
    
    Args:
        returns: Array of returns
        risk_free_rate: Annualized risk-free rate (default 0.0)
    
    Returns:
        Sharpe ratio
    """
    if len(returns) == 0:
        return np.nan
    
    mean_return = np.mean(returns)
    std_return = np.std(returns, ddof=1)
    
    if std_return == 0:
        return np.nan
    
    # For annual strategy: Sharpe = (mean - rf) / std
    return (mean_return - risk_free_rate) / std_return
