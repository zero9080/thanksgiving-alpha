import typer
from pathlib import Path
from typing import List, Tuple
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
def main(
    config: str,
    top: int = 20,
) -> None:
    """Run the Thanksgiving seasonality analysis.
    
    Args:
        config: Path to YAML configuration file
        top: Number of top-ranked symbols to display
    """
    # Load configuration
    cfg = Config(**yaml.safe_load(Path(config).read_text()))
    
    # Load universe of symbols
    symbols = load_universe(cfg.universe)
    
    # Initialize data provider
    prov = YahooProvider()
    
    # Collect returns for each symbol and year
    rows: List[Tuple[str, int, float]] = []
    
    print(f"Analyzing {len(symbols)} symbols from {cfg.start_year} to {cfg.end_year}...")
    
    for year in range(cfg.start_year, cfg.end_year + 1):
        try:
            # Calculate window dates for this year
            open_day, close_day = holiday_window_dates(
                year, cfg.window.days_before, cfg.window.days_after
            )
            
            # Add buffer for data download (±7 calendar days)
            start = (open_day - pd.Timedelta(days=7)).date()
            end = (close_day + pd.Timedelta(days=7)).date()
            
            for s in symbols:
                try:
                    # Download OHLC data
                    df = prov.get_ohlc(s, start, end)
                    
                    # Compute return for this window
                    r = compute_return(df, open_day, close_day)
                    
                    if r is not None:
                        rows.append((s, year, r))
                except Exception as e:
                    # Skip individual symbol errors but continue processing
                    pass  # Silently skip to reduce noise
                    
        except Exception as e:
            print(f"Warning: Failed to process year {year}: {e}")
            continue
    
    if not rows:
        print("Error: No data collected. Please check your configuration and data availability.")
        raise typer.Exit(code=1)
    
    print(f"Collected {len(rows)} return observations across {len(set(r[0] for r in rows))} symbols")
    
    # Aggregate and rank
    ranking = aggregate_per_symbol(rows, min_trades=cfg.ranking.min_trades)
    
    # Export results
    out_dir = Path(cfg.output.dir)
    export_tables(ranking, out_dir, cfg.output.formats)
    
    # Display top N
    print(f"\nTop {top} symbols by median return:")
    print(ranking.head(top).to_pandas().to_string(index=False))
    print(f"\nFull results saved to {out_dir}/")


if __name__ == "__main__":
    app()
