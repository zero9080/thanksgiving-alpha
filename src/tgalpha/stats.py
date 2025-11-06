from datetime import date
import polars as pl
import pandas as pd
from .holidays import thanksgiving
from .calendar_utils import us_trading_calendar, shift_business_days

def holiday_window_dates(year: int, x_before: int, y_after: int) -> tuple[pd.Timestamp, pd.Timestamp]:
    h = thanksgiving(year)
    cal = us_trading_calendar(date(h.year, 1, 1), date(h.year, 12, 31))
    before = shift_business_days(cal, h, -x_before)
    after = shift_business_days(cal, h, y_after)
    return before, after

def compute_return(df: pl.DataFrame, open_day: pd.Timestamp, close_day: pd.Timestamp) -> float | None:
    try:
        o = df.filter(pl.col("Date") == open_day.to_pydatetime())["Open"].item()
        c = df.filter(pl.col("Date") == close_day.to_pydatetime())["Close"].item()
        return c / o - 1.0
    except Exception:
        return None
