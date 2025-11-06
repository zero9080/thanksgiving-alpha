import polars as pl
from typing import List, Tuple


def aggregate_per_symbol(
    rows: List[Tuple[str, int, float]], min_trades: int = 10
) -> pl.DataFrame:
    """Aggregate returns per symbol and rank them.
    
    Args:
        rows: List of (symbol, year, return) tuples
        min_trades: Minimum number of observations required to include a symbol
    
    Returns:
        DataFrame with aggregated statistics, sorted by median_return, win_rate, avg_return
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
    
    # Sort by median_return, win_rate, avg_return (all descending)
    return by_sym.sort(
        ["median_return", "win_rate", "avg_return"], descending=[True, True, True]
    )
