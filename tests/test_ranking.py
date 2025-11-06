from typing import List, Tuple
import polars as pl
import pytest
from tgalpha.ranking import aggregate_per_symbol


def test_aggregate_basic() -> None:
    """Test basic aggregation of returns."""
    rows: List[Tuple[str, int, float]] = [
        ("AAPL", 2023, 0.05),
        ("AAPL", 2024, 0.10),
        ("MSFT", 2023, 0.03),
        ("MSFT", 2024, 0.07),
    ]
    
    result = aggregate_per_symbol(rows, min_trades=2)
    
    assert len(result) == 2
    assert "AAPL" in result["symbol"].to_list()
    assert "MSFT" in result["symbol"].to_list()


def test_aggregate_median_calculation() -> None:
    """Test that median is calculated correctly."""
    rows: List[Tuple[str, int, float]] = [
        ("AAPL", 2020, 0.01),
        ("AAPL", 2021, 0.05),
        ("AAPL", 2022, 0.09),
    ]
    
    result = aggregate_per_symbol(rows, min_trades=1)
    
    aapl_row = result.filter(pl.col("symbol") == "AAPL")
    median = aapl_row["median_return"].item()
    
    # Median of [0.01, 0.05, 0.09] is 0.05
    assert abs(median - 0.05) < 0.0001


def test_aggregate_win_rate() -> None:
    """Test that win rate is calculated correctly."""
    rows: List[Tuple[str, int, float]] = [
        ("AAPL", 2020, 0.05),
        ("AAPL", 2021, -0.02),
        ("AAPL", 2022, 0.03),
        ("AAPL", 2023, 0.01),
    ]
    
    result = aggregate_per_symbol(rows, min_trades=1)
    
    aapl_row = result.filter(pl.col("symbol") == "AAPL")
    win_rate = aapl_row["win_rate"].item()
    
    # 3 out of 4 are positive = 0.75
    assert abs(win_rate - 0.75) < 0.0001


def test_aggregate_min_trades_filter() -> None:
    """Test that symbols with fewer than min_trades are filtered out."""
    rows: List[Tuple[str, int, float]] = [
        ("AAPL", 2020, 0.05),
        ("AAPL", 2021, 0.10),
        ("AAPL", 2022, 0.03),
        ("MSFT", 2020, 0.02),  # Only 1 observation
    ]
    
    result = aggregate_per_symbol(rows, min_trades=2)
    
    # Only AAPL should remain (has 3 observations >= 2)
    assert len(result) == 1
    assert result["symbol"].item() == "AAPL"


def test_aggregate_sorting() -> None:
    """Test that results are sorted correctly."""
    rows: List[Tuple[str, int, float]] = [
        # AAPL: median=0.05, avg=0.05, win_rate=1.0
        ("AAPL", 2020, 0.05),
        ("AAPL", 2021, 0.05),
        # MSFT: median=0.03, avg=0.03, win_rate=1.0
        ("MSFT", 2020, 0.03),
        ("MSFT", 2021, 0.03),
    ]
    
    result = aggregate_per_symbol(rows, min_trades=2)
    
    # AAPL should be first (higher median)
    assert result["symbol"].to_list()[0] == "AAPL"
    assert result["symbol"].to_list()[1] == "MSFT"


def test_aggregate_empty_input() -> None:
    """Test that empty input returns empty DataFrame."""
    rows: List[Tuple[str, int, float]] = []
    
    result = aggregate_per_symbol(rows, min_trades=1)
    
    assert len(result) == 0
