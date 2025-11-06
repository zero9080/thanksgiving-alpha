from datetime import date
import polars as pl
import pandas as pd
import yfinance as yf

from .base import PriceProvider

class YahooProvider(PriceProvider):
    def get_ohlc(self, symbol: str, start: date, end: date) -> pl.DataFrame:
        data = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=False)
        if data.empty:
            return pl.DataFrame({"Date": [], "Open": [], "Close": []})
        data = data.reset_index()[["Date", "Open", "Close"]]
        return pl.from_pandas(data)
