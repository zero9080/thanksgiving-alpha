from datetime import date
import pandas as pd
from pandas.tseries.holiday import (
    USFederalHolidayCalendar,
    Holiday,
    nearest_workday,
    GoodFriday,
)


def _third_monday(month: int) -> Holiday:
    """Helper to create third Monday holidays."""
    return Holiday(
        f"ThirdMonday{month}",
        month=month,
        day=15,  # Start from middle of month
        offset=pd.DateOffset(weekday=0),  # Monday
    )


class NYSECalendar(USFederalHolidayCalendar):
    """NYSE trading calendar with market holidays.

    Note: Black Friday (day after Thanksgiving) is a half-day trading session
    (market closes at 1:00 PM ET) but is still counted as a trading day for
    business day calculations. It is NOT a market holiday.
    """

    rules = [
        Holiday("NewYearsDay", month=1, day=1, observance=nearest_workday),
        # MLK Day: 3rd Monday in January
        Holiday("MLKDay", month=1, day=15, offset=pd.DateOffset(weekday=0)),
        # Presidents Day: 3rd Monday in February
        Holiday("PresidentsDay", month=2, day=15, offset=pd.DateOffset(weekday=0)),
        GoodFriday,
        # Memorial Day: Last Monday in May
        Holiday("MemorialDay", month=5, day=25, offset=pd.DateOffset(weekday=0)),
        Holiday("Juneteenth", month=6, day=19, observance=nearest_workday),
        Holiday("IndependenceDay", month=7, day=4, observance=nearest_workday),
        # Labor Day: First Monday in September
        Holiday("LaborDay", month=9, day=1, offset=pd.DateOffset(weekday=0)),
        # Thanksgiving: 4th Thursday in November
        Holiday("Thanksgiving", month=11, day=22, offset=pd.DateOffset(weekday=3)),
        Holiday("Christmas", month=12, day=25, observance=nearest_workday),
    ]


def us_trading_calendar(start: date, end: date) -> pd.DatetimeIndex:
    """Generate NYSE trading days between start and end (inclusive).

    Args:
        start: Start date
        end: End date

    Returns:
        DatetimeIndex of trading days
    """
    nyse_cal = NYSECalendar()
    all_days = pd.bdate_range(start=start, end=end, freq="C")
    holidays = nyse_cal.holidays(start=start, end=end)
    trading_days = all_days.difference(holidays)
    return trading_days


def shift_business_days(cal: pd.DatetimeIndex, anchor: date, offset: int) -> pd.Timestamp:
    """Shift from anchor date by offset business days using the provided calendar.

    This function treats the anchor as the reference point (day 0), regardless of
    whether it's a trading day. Offsets are counted in trading days from the anchor.
    - offset=0: nearest trading day to anchor (or anchor itself if it's a trading day)
    - offset=1: 1st trading day after anchor
    - offset=-1: 1st trading day before anchor

    Args:
        cal: DatetimeIndex of valid trading days
        anchor: Reference date (may or may not be a trading day)
        offset: Number of business days to shift (positive for future, negative for past)

    Returns:
        pd.Timestamp of the target trading day
    """
    anchor_ts = pd.Timestamp(anchor)

    if offset > 0:
        # Counting forward: find trading days after anchor
        # searchsorted with side='right' gives us the first index > anchor
        idx = cal.searchsorted(anchor_ts, side="right")
        if idx >= len(cal):
            raise ValueError(f"No trading days after {anchor}")
        # Now we're at the first trading day after anchor
        # offset=1 means we want this day, offset=2 means next day, etc.
        target_idx = idx + offset - 1
    elif offset < 0:
        # Counting backward: find trading days before anchor
        # searchsorted with side='left' gives us the first index >= anchor
        idx = cal.searchsorted(anchor_ts, side="left")
        # We want to go back from anchor, so start from idx-1
        # offset=-1 means we want the previous trading day
        target_idx = idx + offset
    else:
        # offset=0: return the anchor if it's a trading day, otherwise error
        if anchor_ts in cal:
            return anchor_ts
        else:
            raise ValueError(f"Anchor {anchor} is not a trading day and offset is 0")

    if target_idx < 0 or target_idx >= len(cal):
        raise ValueError(f"Offset {offset} from {anchor} results in date outside calendar range")

    return cal[target_idx]
