from datetime import date
import polars as pl
import pandas as pd
import yfinance as yf

from .base import PriceProvider


class YahooProvider(PriceProvider):
    """Yahoo Finance data provider implementation."""
    
    def get_ohlc(self, symbol: str, start: date, end: date) -> pl.DataFrame:
        """Download OHLC data from Yahoo Finance.
        
        Args:
            symbol: Stock ticker symbol
            start: Start date for data download
            end: End date for data download
            
        Returns:
            Polars DataFrame with columns: Date, Open, Close
        """
        try:
            data = yf.download(
                symbol, start=start, end=end, progress=False, auto_adjust=True
            )
            
            if data.empty:
                return pl.DataFrame(
                    schema={"Date": pl.Datetime, "Open": pl.Float64, "Close": pl.Float64}
                )
            
            # Reset index to make Date a column and select needed columns
            data_reset = data.reset_index()
            
            # Handle potential multi-index columns from yfinance
            if isinstance(data_reset.columns, pd.MultiIndex):
                data_reset.columns = data_reset.columns.get_level_values(0)
            
            # Select only the columns we need
            result_df = data_reset[["Date", "Open", "Close"]]
            
            return pl.from_pandas(result_df)
        except Exception as e:
            # Return empty DataFrame on any error
            return pl.DataFrame(
                schema={"Date": pl.Datetime, "Open": pl.Float64, "Close": pl.Float64}
            )
