"""
Data coverage analysis utilities.

Provides functions to compute and display data completeness by year.
"""

import polars as pl
from typing import List, Tuple


def compute_coverage_by_year(
    rows: List[Tuple[str, int, float]], start_year: int, end_year: int
) -> pl.DataFrame:
    """
    Compute number of valid tickers per year.

    Args:
        rows: List of (symbol, year, return) tuples
        start_year: Start of analysis period
        end_year: End of analysis period

    Returns:
        DataFrame with columns: year, n_stocks, pct_complete
        where n_stocks is count of symbols with valid data that year
    """
    if not rows:
        return pl.DataFrame({"year": [], "n_stocks": [], "pct_complete": []})

    # Create DataFrame
    df = pl.DataFrame(
        {
            "symbol": [r[0] for r in rows],
            "year": [r[1] for r in rows],
            "ret": [r[2] for r in rows],
        }
    )

    # Count unique symbols per year
    coverage = df.group_by("year").agg([pl.n_unique("symbol").alias("n_stocks")]).sort("year")

    # Get total unique symbols in dataset
    total_symbols = df["symbol"].n_unique()

    # Add percentage completeness
    coverage = coverage.with_columns(
        [(pl.col("n_stocks") / total_symbols * 100).alias("pct_complete")]
    )

    # Fill in missing years with zero counts
    all_years = list(range(start_year, end_year + 1))
    year_df = pl.DataFrame({"year": all_years})

    coverage = year_df.join(coverage, on="year", how="left")
    coverage = coverage.with_columns(
        [pl.col("n_stocks").fill_null(0), pl.col("pct_complete").fill_null(0.0)]
    )

    return coverage.sort("year")


def format_coverage_table(coverage: pl.DataFrame) -> str:
    """
    Format coverage DataFrame as markdown table.

    Args:
        coverage: DataFrame from compute_coverage_by_year()

    Returns:
        Markdown formatted table string
    """
    if len(coverage) == 0:
        return "No coverage data available.\n"

    lines = []
    lines.append("| Year | Stocks | Completeness |")
    lines.append("|------|--------|--------------|")

    for row in coverage.iter_rows(named=True):
        year = int(row["year"])
        n_stocks = int(row["n_stocks"])
        pct = float(row["pct_complete"])
        lines.append(f"| {year} | {n_stocks} | {pct:.1f}% |")

    # Add summary statistics
    lines.append("")
    lines.append(f"**Average coverage:** {float(coverage['pct_complete'].mean()):.1f}%  ")  # type: ignore[arg-type]
    lines.append(f"**Median coverage:** {float(coverage['pct_complete'].median()):.1f}%  ")  # type: ignore[arg-type]

    min_year = int(
        coverage.filter(pl.col("pct_complete") == pl.col("pct_complete").min())["year"][0]
    )
    max_year = int(
        coverage.filter(pl.col("pct_complete") == pl.col("pct_complete").max())["year"][0]
    )

    lines.append(
        f"**Min coverage:** {float(coverage['pct_complete'].min()):.1f}% (year {min_year})  "  # type: ignore[arg-type]
    )
    lines.append(
        f"**Max coverage:** {float(coverage['pct_complete'].max()):.1f}% (year {max_year})  "  # type: ignore[arg-type]
    )

    return "\n".join(lines)
