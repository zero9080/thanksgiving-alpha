import typer
from pathlib import Path
import yaml
import pandas as pd
from datetime import date
import polars as pl

from .config import Config
from .universe import load_universe
from .data_providers.yahoo import YahooProvider
from .stats import holiday_window_dates, compute_return
from .ranking import aggregate_per_symbol
from .report import export_tables

app = typer.Typer()

@app.command()
def run(config: str, top: int = 20) -> None:
    cfg = Config(**yaml.safe_load(Path(config).read_text()))
    symbols = load_universe(cfg.universe)
    prov = YahooProvider()

    rows: list[tuple[str, float]] = []
    for year in range(cfg.start_year, cfg.end_year + 1):
        open_day, close_day = holiday_window_dates(year, cfg.window.days_before, cfg.window.days_after)
        start = (open_day - pd.Timedelta(days=7)).date()
        end = (close_day + pd.Timedelta(days=7)).date()
        for s in symbols:
            df = prov.get_ohlc(s, start, end)
            r = compute_return(df, open_day, close_day)
            if r is not None:
                rows.append((s, r))

    ranking = aggregate_per_symbol(rows)
    export_tables(ranking, Path(cfg.output.dir))
    print(ranking.head(top).to_pandas().to_string(index=False))

if __name__ == "__main__":
    app()
