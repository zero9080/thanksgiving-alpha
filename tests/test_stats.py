from tgalpha.stats import holiday_window_dates

def test_window_types():
    before, after = holiday_window_dates(2025, 3, 1)
    assert before <= after
