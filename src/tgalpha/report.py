from pathlib import Path
import polars as pl

def export_tables(df: pl.DataFrame, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    df.write_csv(out_dir / "ranking.csv")
    df.write_parquet(out_dir / "ranking.parquet")
