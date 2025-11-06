from pathlib import Path
from typing import List
import polars as pl

# Current DJIA constituents (as of 2025)
DJIA_DEFAULT = [
    "AAPL", "AMGN", "AMZN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS",
    "DOW", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD",
    "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WMT"
]

# NASDAQ-100 constituents (as of November 2025)
# Top 100 non-financial companies listed on NASDAQ
NASDAQ100_DEFAULT = [
    # Mega-cap Technology
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "COST",
    # Large-cap Technology & Communications
    "NFLX", "ADBE", "CRM", "CSCO", "INTC", "AMD", "QCOM", "TXN", "INTU", "AMAT",
    "ADI", "MU", "LRCX", "KLAC", "SNPS", "CDNS", "MRVL", "FTNT", "PANW", "CRWD",
    # Semiconductor & Hardware
    "ASML", "MCHP", "NXPI", "ON", "MPWR", "ENPH", "SMCI", "ARM",
    # Software & Cloud
    "NOW", "TEAM", "WDAY", "DDOG", "ZS", "SNOW", "PLTR", "MNDY", "DXCM", "TTD",
    # E-commerce & Retail
    "BKNG", "EBAY", "JD", "PDD", "MELI", "DASH", "ABNB",
    # Biotech & Healthcare
    "AMGN", "GILD", "VRTX", "REGN", "BIIB", "MRNA", "ILMN", "ALNY", "SGEN", "TECH",
    # Consumer & Industrial
    "TSCO", "ROST", "ODFL", "PCAR", "CPRT", "FAST", "PAYX", "CTAS", "VRSK", "ADP",
    # Food & Beverage
    "PEP", "MDLZ", "KDP", "MNST",
    # Other Major Companies
    "ISRG", "ADSK", "NTES", "LULU", "MELI", "ORLY", "MAR", "AZN", "CHTR", "CMCSA",
    "EA", "XEL", "IDXX", "ANSS", "CSGP", "GEHC", "FANG", "CCEP", "ZM", "LCID"
]

def load_universe(spec: str) -> List[str]:
    if spec == "djia":
        return DJIA_DEFAULT
    if spec == "nasdaq100":
        return NASDAQ100_DEFAULT
    p = Path(spec)
    if p.suffix.lower() == ".csv" and p.exists():
        df = pl.read_csv(p)
        return df["symbol"].to_list()
    raise ValueError(f"Unsupported universe spec: {spec}")
