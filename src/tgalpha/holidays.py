from datetime import date
import pandas as pd


def thanksgiving(year: int) -> date:
    """Calculate the date of US Thanksgiving for a given year.
    
    US Thanksgiving is the 4th Thursday of November.
    
    Args:
        year: The year to calculate Thanksgiving for
        
    Returns:
        The date of Thanksgiving
    """
    # Start from November 1st
    d = pd.Timestamp(year=year, month=11, day=1)
    
    # Find all Thursdays in November
    thursdays = [
        d + pd.Timedelta(days=i)
        for i in range(30)
        if (d + pd.Timedelta(days=i)).weekday() == 3  # Thursday = 3
    ]
    
    # Return the 4th Thursday (0-indexed: index 3)
    return thursdays[3].date()
