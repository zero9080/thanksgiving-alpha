from pathlib import Path
from typing import List
import polars as pl


def export_tables(df: pl.DataFrame, out_dir: Path, formats: List[str]) -> None:
    """Export ranking table to multiple formats.
    
    Args:
        df: DataFrame with ranking results
        out_dir: Output directory path
        formats: List of output formats (csv, parquet, html)
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    
    if "csv" in formats:
        df.write_csv(out_dir / "ranking.csv")
    
    if "parquet" in formats:
        df.write_parquet(out_dir / "ranking.parquet")
    
    if "html" in formats:
        # Convert to pandas for better HTML formatting
        html_content = df.to_pandas().to_html(index=False, float_format="%.4f")
        (out_dir / "ranking.html").write_text(html_content)
