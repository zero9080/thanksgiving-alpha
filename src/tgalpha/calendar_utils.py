from datetime import date
import pandas as pd

def us_trading_calendar(start: date, end: date) -> pd.DatetimeIndex:
    # Minimal placeholder: NYSE business days; replace with proper calendar if needed
    return pd.bdate_range(start=start, end=end, freq="C", weekmask="Mon Tue Wed Thu Fri")

def shift_business_days(cal: pd.DatetimeIndex, anchor: date, offset: int) -> pd.Timestamp:
    idx = cal.get_indexer([pd.Timestamp(anchor)], method="backfill")[0]
    return cal[idx + offset]
