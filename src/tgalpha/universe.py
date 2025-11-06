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

# S&P 500 constituents (as of November 2025)
# Major US companies across all sectors
SP500_DEFAULT = [
    # Technology (Large Cap)
    "AAPL", "MSFT", "NVDA", "GOOGL", "GOOG", "META", "AVGO", "TSLA", "ORCL", "ADBE",
    "CRM", "CSCO", "ACN", "AMD", "INTC", "IBM", "QCOM", "TXN", "INTU", "NOW",
    "AMAT", "ADI", "MU", "LRCX", "KLAC", "SNPS", "CDNS", "MRVL", "FTNT", "PANW",
    # Communication Services
    "NFLX", "DIS", "CMCSA", "VZ", "T", "TMUS", "CHTR", "EA", "TTWO", "LYV",
    # Consumer Discretionary
    "AMZN", "TSLA", "HD", "MCD", "NKE", "SBUX", "TJX", "BKNG", "LOW", "TGT",
    "ROST", "MAR", "ABNB", "CMG", "ORLY", "YUM", "DHI", "LEN", "POOL", "ULTA",
    # Consumer Staples
    "WMT", "PG", "COST", "KO", "PEP", "PM", "MO", "MDLZ", "CL", "KMB",
    "GIS", "KHC", "TSN", "STZ", "HSY", "KDP", "MNST", "CPB", "CAG", "SJM",
    # Healthcare
    "UNH", "JNJ", "LLY", "ABBV", "MRK", "TMO", "ABT", "DHR", "PFE", "AMGN",
    "CVS", "BMY", "GILD", "CI", "ELV", "VRTX", "REGN", "MCK", "ZTS", "ISRG",
    "HUM", "BIIB", "DXCM", "IDXX", "SYK", "BDX", "EW", "RMD", "ALGN", "ILMN",
    # Financials
    "BRK.B", "JPM", "V", "MA", "BAC", "WFC", "MS", "GS", "SPGI", "BLK",
    "C", "AXP", "SCHW", "CB", "MMC", "PGR", "CME", "ICE", "AON", "TRV",
    "USB", "PNC", "TFC", "COF", "AFL", "MET", "AIG", "PRU", "ALL", "AJG",
    # Industrials
    "CAT", "GE", "BA", "HON", "RTX", "UPS", "DE", "LMT", "UNP", "ETN",
    "ADP", "MMM", "WM", "GD", "ITW", "CSX", "EMR", "NSC", "PCAR", "NOC",
    "CARR", "CTAS", "TT", "PAYX", "ODFL", "VRSK", "CPRT", "FAST", "RSG", "URI",
    # Energy
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "WMB",
    "KMI", "HES", "FANG", "BKR", "HAL", "DVN", "TRGP", "EQT", "CTRA", "MRO",
    # Materials
    "LIN", "APD", "SHW", "ECL", "FCX", "NEM", "CTVA", "DD", "DOW", "NUE",
    "VMC", "MLM", "PPG", "IFF", "ALB", "BALL", "AMCR", "CE", "CF", "MOS",
    # Real Estate
    "AMT", "PLD", "CCI", "EQIX", "PSA", "WELL", "DLR", "O", "SBAC", "SPG",
    "AVB", "EQR", "VTR", "ARE", "INVH", "MAA", "ESS", "UDR", "CPT", "PEAK",
    # Utilities
    "NEE", "SO", "DUK", "D", "AEP", "SRE", "EXC", "XEL", "PCG", "ED",
    "PEG", "WEC", "ES", "AWK", "DTE", "PPL", "FE", "EIX", "ETR", "AEE",
    # Additional Notable Companies
    "UBER", "LYFT", "DASH", "SNOW", "PLTR", "CRWD", "ZS", "DDOG", "NET", "OKTA",
    "TEAM", "WDAY", "VEEV", "ZM", "DOCU", "TWLO", "COIN", "SQ", "PYPL", "SHOP"
]

def load_universe(spec: str) -> List[str]:
    if spec == "djia":
        return DJIA_DEFAULT
    if spec == "nasdaq100":
        return NASDAQ100_DEFAULT
    if spec == "sp500":
        return SP500_DEFAULT
    p = Path(spec)
    if p.suffix.lower() == ".csv" and p.exists():
        df = pl.read_csv(p)
        return df["symbol"].to_list()
    raise ValueError(f"Unsupported universe spec: {spec}")
