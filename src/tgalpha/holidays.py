from datetime import date
import pandas as pd

def thanksgiving(year: int) -> date:
    d = pd.Timestamp(year=year, month=11, day=1)
    thursdays = [d + pd.Timedelta(days=i) for i in range(30) if (d + pd.Timedelta(days=i)).weekday() == 3]
    return thursdays[3].date()
