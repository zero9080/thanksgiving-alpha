# Thanksgiving-Alpha

Seasonality research around US Thanksgiving for DJIA constituents and indices.
Parameterizable window: X business days **before** Thanksgiving (use Open) to Y business days **after** (use Close; Black Friday half-day honored).

## Quickstart
```bash
pipx install poetry
poetry install
poetry run tgalpha run --config configs/example_djia.yaml --top 20
```
