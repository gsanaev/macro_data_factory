"""Validate interim OECD datasets."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "series_name",
    "provider_series_id",
    "provider_entity_id",
    "country_code",
    "country_name",
    "year",
    "value",
    "unit_code",
    "unit",
    "unit_multiplier",
    "currency_code",
    "currency",
    "frequency",
}


def summarize_dataset(input_path: Path) -> dict[str, int | str]:
    """Return structural and coverage statistics for one OECD series."""
    if not input_path.exists():
        raise FileNotFoundError(f"Interim OECD file not found: {input_path}")

    dataframe = pd.read_parquet(input_path)

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required OECD columns: {missing}")

    if dataframe.empty:
        raise ValueError(f"OECD interim file contains no observations: {input_path}")

    series_names = dataframe["series_name"].dropna().unique()

    if len(series_names) != 1:
        raise ValueError(
            f"Expected one OECD series in {input_path}, found {len(series_names)}."
        )

    duplicate_keys = int(
        dataframe.duplicated(subset=["series_name", "provider_entity_id", "year"]).sum()
    )

    frequencies = dataframe["frequency"].dropna().unique()

    if len(frequencies) != 1:
        raise ValueError(
            f"Expected one frequency in {input_path}, found {len(frequencies)}."
        )

    return {
        "series_name": str(series_names[0]),
        "rows": len(dataframe),
        "entities": dataframe["provider_entity_id"].nunique(dropna=True),
        "minimum_year": int(dataframe["year"].min()),
        "maximum_year": int(dataframe["year"].max()),
        "missing_values": int(dataframe["value"].isna().sum()),
        "duplicate_keys": duplicate_keys,
        "frequency": str(frequencies[0]),
        "unit": str(dataframe["unit"].dropna().iloc[0]),
        "unit_multiplier": int(dataframe["unit_multiplier"].dropna().iloc[0]),
        "currency": str(dataframe["currency"].dropna().iloc[0]),
    }


def print_summary(summary: dict[str, int | str]) -> None:
    """Print a readable OECD dataset summary."""
    print("OECD Dataset Summary")
    print("--------------------")
    print(f"Series:           {summary['series_name']}")
    print(f"Rows:             {summary['rows']}")
    print(f"Entities:         {summary['entities']}")
    print(f"Years:            {summary['minimum_year']}–{summary['maximum_year']}")
    print(f"Frequency:        {summary['frequency']}")
    print(f"Missing values:   {summary['missing_values']}")
    print(f"Duplicate keys:   {summary['duplicate_keys']}")
    print(f"Unit:             {summary['unit']}")
    print(f"Unit multiplier:  {summary['unit_multiplier']}")
    print(f"Currency:         {summary['currency']}")
