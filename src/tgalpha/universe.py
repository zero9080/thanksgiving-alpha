from pathlib import Path
from typing import List
import polars as pl

# Current DJIA constituents (as of 2025)
DJIA_DEFAULT = [
    "AAPL", "AMGN", "AMZN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS",
    "DOW", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD",
    "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WMT"
]

def load_universe(spec: str) -> List[str]:
    if spec == "djia":
        return DJIA_DEFAULT
    p = Path(spec)
    if p.suffix.lower() == ".csv" and p.exists():
        df = pl.read_csv(p)
        return df["symbol"].to_list()
    raise ValueError(f"Unsupported universe spec: {spec}")
