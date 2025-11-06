from pathlib import Path
from typing import List
import polars as pl

DJIA_DEFAULT = [
    "AAPL","MSFT","UNH","GS","BA"
]

def load_universe(spec: str) -> List[str]:
    if spec == "djia":
        return DJIA_DEFAULT
    p = Path(spec)
    if p.suffix.lower() == ".csv" and p.exists():
        df = pl.read_csv(p)
        return df["symbol"].to_list()
    raise ValueError(f"Unsupported universe spec: {spec}")
