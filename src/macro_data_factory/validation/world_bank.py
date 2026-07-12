"""Validate interim World Bank datasets."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def summarize_dataset(input_path: Path) -> dict[str, int | str]:
    """Return basic structural and coverage statistics."""
    if not input_path.exists():
        raise FileNotFoundError(f"Interim World Bank file not found: {input_path}")

    dataframe = pd.read_parquet(input_path)

    required_columns = {
        "indicator_code",
        "country_code",
        "country_name",
        "year",
        "value",
    }

    missing_columns = required_columns.difference(dataframe.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    duplicate_keys = int(
        dataframe.duplicated(
            subset=["indicator_code", "provider_country_id", "country_code", "year"]
        ).sum()
    )

    return {
        "indicator": str(dataframe["indicator_code"].dropna().iloc[0]),
        "rows": len(dataframe),
        "countries": dataframe["country_code"].nunique(dropna=True),
        "minimum_year": int(dataframe["year"].min()),
        "maximum_year": int(dataframe["year"].max()),
        "missing_values": int(dataframe["value"].isna().sum()),
        "duplicate_keys": duplicate_keys,
    }


def print_summary(summary: dict[str, int | str]) -> None:
    """Print a readable World Bank dataset summary."""
    print("World Bank Dataset Summary")
    print("--------------------------")
    print(f"Indicator:       {summary['indicator']}")
    print(f"Rows:            {summary['rows']}")
    print(f"Countries:       {summary['countries']}")
    print(f"Years:           {summary['minimum_year']}–{summary['maximum_year']}")
    print(f"Missing values:  {summary['missing_values']}")
    print(f"Duplicate keys:  {summary['duplicate_keys']}")
