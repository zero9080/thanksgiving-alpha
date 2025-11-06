from datetime import date
import pytest
from tgalpha.holidays import thanksgiving


def test_thanksgiving_2025() -> None:
    assert str(thanksgiving(2025)) == "2025-11-27"


def test_thanksgiving_2024() -> None:
    """Test that Thanksgiving 2024 is correctly calculated."""
    assert str(thanksgiving(2024)) == "2024-11-28"


def test_thanksgiving_2023() -> None:
    """Test that Thanksgiving 2023 is correctly calculated."""
    assert str(thanksgiving(2023)) == "2023-11-23"


def test_thanksgiving_1990() -> None:
    """Test that Thanksgiving 1990 is correctly calculated."""
    assert str(thanksgiving(1990)) == "1990-11-22"


def test_thanksgiving_is_thursday() -> None:
    """Test that Thanksgiving is always a Thursday."""
    for year in range(1990, 2026):
        tg = thanksgiving(year)
        # Thursday is weekday 3 in Python's date.weekday()
        assert tg.weekday() == 3, f"Thanksgiving {year} ({tg}) is not a Thursday"


def test_thanksgiving_is_fourth_thursday() -> None:
    """Test that Thanksgiving is the 4th Thursday of November."""
    for year in range(1990, 2026):
        tg = thanksgiving(year)
        # Count Thursdays before this date in November
        thursdays_before = 0
        for day in range(1, tg.day):
            if date(year, 11, day).weekday() == 3:
                thursdays_before += 1
        # This should be the 4th Thursday (0-indexed: 3)
        assert thursdays_before == 3, f"Thanksgiving {year} is not the 4th Thursday"
