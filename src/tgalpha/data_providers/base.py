from abc import ABC, abstractmethod
import polars as pl
from datetime import date


class PriceProvider(ABC):
    @abstractmethod
    def get_ohlc(self, symbol: str, start: date, end: date) -> pl.DataFrame: ...
