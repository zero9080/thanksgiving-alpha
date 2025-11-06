import polars as pl

def aggregate_per_symbol(rows: list[tuple[str, float]]) -> pl.DataFrame:
    df = pl.DataFrame({"symbol": [r[0] for r in rows], "ret": [r[1] for r in rows]})
    by_sym = df.group_by("symbol").agg([
        pl.len().alias("n"),
        pl.median("ret").alias("median_return"),
        pl.mean("ret").alias("avg_return"),
        (pl.col("ret") > 0).mean().alias("win_rate"),
        pl.std("ret").alias("std"),
    ])
    return by_sym.sort(["median_return", "win_rate", "avg_return"], descending=[True, True, True])
