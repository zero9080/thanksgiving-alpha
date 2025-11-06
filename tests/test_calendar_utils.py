from datetime import date
from tgalpha.calendar_utils import us_trading_calendar

def test_calendar_has_business_days():
    cal = us_trading_calendar(date(2025,1,1), date(2025,1,10))
    assert len(cal) >= 6
