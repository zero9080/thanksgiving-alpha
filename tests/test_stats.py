from datetime import date, datetime
import polars as pl
import pandas as pd
import pytest
from tgalpha.stats import holiday_window_dates, compute_return


def test_window_types() -> None:
    """Test that window dates are properly ordered."""
    before, after = holiday_window_dates(2025, 3, 1)
    assert before <= after


def test_window_dates_2025() -> None:
    """Test specific window dates for 2025."""
    # Thanksgiving 2025 is Nov 27 (Thursday)
    # 3 days before should be Mon Nov 24
    # 1 day after should be Fri Nov 28 (Black Friday - a trading day)
    before, after = holiday_window_dates(2025, 3, 1)
    assert before.date() == date(2025, 11, 24)
    assert after.date() == date(2025, 11, 28)
    # Verify it's a Friday
    assert after.weekday() == 4  # Friday = 4


def test_compute_return_simple() -> None:
    """Test simple return calculation."""
    df = pl.DataFrame({
        "Date": [datetime(2025, 11, 24), datetime(2025, 11, 28)],
        "Open": [100.0, 105.0],
        "Close": [102.0, 110.0],
    })
    
    open_day = pd.Timestamp("2025-11-24")
    close_day = pd.Timestamp("2025-11-28")
    
    ret = compute_return(df, open_day, close_day)
    assert ret is not None
    # Return should be 110/100 - 1 = 0.10 (10%)
    assert abs(ret - 0.10) < 0.0001


def test_compute_return_loss() -> None:
    """Test return calculation with a loss."""
    df = pl.DataFrame({
        "Date": [datetime(2025, 11, 24), datetime(2025, 11, 28)],
        "Open": [100.0, 95.0],
        "Close": [98.0, 90.0],
    })
    
    open_day = pd.Timestamp("2025-11-24")
    close_day = pd.Timestamp("2025-11-28")
    
    ret = compute_return(df, open_day, close_day)
    assert ret is not None
    # Return should be 90/100 - 1 = -0.10 (-10%)
    assert abs(ret - (-0.10)) < 0.0001


def test_compute_return_missing_open_date() -> None:
    """Test that missing open date returns None."""
    df = pl.DataFrame({
        "Date": [datetime(2025, 11, 28)],
        "Open": [100.0],
        "Close": [110.0],
    })
    
    open_day = pd.Timestamp("2025-11-24")
    close_day = pd.Timestamp("2025-11-28")
    
    ret = compute_return(df, open_day, close_day)
    assert ret is None


def test_compute_return_missing_close_date() -> None:
    """Test that missing close date returns None."""
    df = pl.DataFrame({
        "Date": [datetime(2025, 11, 24)],
        "Open": [100.0],
        "Close": [102.0],
    })
    
    open_day = pd.Timestamp("2025-11-24")
    close_day = pd.Timestamp("2025-11-28")
    
    ret = compute_return(df, open_day, close_day)
    assert ret is None


def test_compute_return_zero_open() -> None:
    """Test that zero or negative open price returns None."""
    df = pl.DataFrame({
        "Date": [datetime(2025, 11, 24), datetime(2025, 11, 28)],
        "Open": [0.0, 100.0],
        "Close": [102.0, 110.0],
    })
    
    open_day = pd.Timestamp("2025-11-24")
    close_day = pd.Timestamp("2025-11-28")
    
    ret = compute_return(df, open_day, close_day)
    assert ret is None
