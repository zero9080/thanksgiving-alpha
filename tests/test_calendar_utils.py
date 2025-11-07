from datetime import date
import pytest
from tgalpha.calendar_utils import us_trading_calendar, shift_business_days


def test_calendar_has_business_days() -> None:
    """Test that calendar returns business days."""
    cal = us_trading_calendar(date(2025, 1, 1), date(2025, 1, 10))
    assert len(cal) >= 6


def test_calendar_excludes_weekends() -> None:
    """Test that weekends are not included in trading calendar."""
    cal = us_trading_calendar(date(2025, 1, 1), date(2025, 1, 31))
    for day in cal:
        # Monday = 0, Sunday = 6
        assert day.weekday() < 5, f"{day} is a weekend day"


def test_calendar_excludes_new_years() -> None:
    """Test that New Year's Day (Jan 1) is excluded when it falls on a weekday."""
    # 2024: Jan 1 is Monday (observed)
    cal = us_trading_calendar(date(2024, 1, 1), date(2024, 1, 2))
    dates = [d.date() for d in cal]
    assert date(2024, 1, 1) not in dates


def test_calendar_excludes_christmas() -> None:
    """Test that Christmas is excluded from trading calendar."""
    # 2024: Dec 25 is Wednesday
    cal = us_trading_calendar(date(2024, 12, 24), date(2024, 12, 26))
    dates = [d.date() for d in cal]
    assert date(2024, 12, 25) not in dates


def test_shift_business_days_forward() -> None:
    """Test shifting forward by business days."""
    cal = us_trading_calendar(date(2025, 1, 1), date(2025, 1, 31))
    # Start from Jan 2, 2025 (Thursday)
    anchor = date(2025, 1, 2)
    result = shift_business_days(cal, anchor, 1)
    # Should be Friday, Jan 3
    assert result.date() == date(2025, 1, 3)


def test_shift_business_days_backward() -> None:
    """Test shifting backward by business days."""
    cal = us_trading_calendar(date(2025, 1, 1), date(2025, 1, 31))
    # Start from Jan 6, 2025 (Monday)
    anchor = date(2025, 1, 6)
    result = shift_business_days(cal, anchor, -1)
    # Should be Friday, Jan 3 (skipping weekend)
    assert result.date() == date(2025, 1, 3)


def test_shift_business_days_across_weekend() -> None:
    """Test that shifting across weekends works correctly."""
    cal = us_trading_calendar(date(2025, 1, 1), date(2025, 1, 31))
    # Friday Jan 3
    anchor = date(2025, 1, 3)
    result = shift_business_days(cal, anchor, 1)
    # Should be Monday Jan 6 (skipping weekend)
    assert result.date() == date(2025, 1, 6)


def test_shift_from_non_trading_day() -> None:
    """Test shifting from a non-trading day (weekend)."""
    cal = us_trading_calendar(date(2025, 1, 1), date(2025, 1, 31))
    # Saturday Jan 4
    anchor = date(2025, 1, 4)
    # offset=1 should give us the first trading day after the weekend (Monday Jan 6)
    result = shift_business_days(cal, anchor, 1)
    assert result.date() == date(2025, 1, 6)


def test_shift_business_days_out_of_range() -> None:
    """Test that shifting out of calendar range raises an error."""
    cal = us_trading_calendar(date(2025, 1, 2), date(2025, 1, 10))
    anchor = date(2025, 1, 2)

    # Shifting too far back should raise ValueError
    with pytest.raises(ValueError):
        shift_business_days(cal, anchor, -10)
