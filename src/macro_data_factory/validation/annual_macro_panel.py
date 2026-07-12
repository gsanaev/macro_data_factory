"""Validate the annual macroeconomic panel."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


KEY_COLUMNS = ["provider_country_id", "year"]


def summarize_annual_macro_panel(input_path: Path) -> dict[str, object]:
    """Return structural and coverage statistics for the annual panel."""
    if not input_path.exists():
        raise FileNotFoundError(f"Annual macro panel not found: {input_path}")

    dataframe = pd.read_parquet(input_path)

    required_columns = {
        "provider_country_id",
        "country_code",
        "country_name",
        "year",
    }

    missing_columns = required_columns.difference(dataframe.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    indicator_columns = [
        column for column in dataframe.columns if column not in required_columns
    ]

    duplicate_keys = int(dataframe.duplicated(KEY_COLUMNS).sum())

    missingness = {
        column: int(dataframe[column].isna().sum()) for column in indicator_columns
    }

    aggregate_examples = (
        dataframe.loc[
            dataframe["country_code"].isin(
                ["ARB", "AFE", "AFW", "ECS", "LCN", "NAC", "SAS", "WLD"]
            ),
            "country_name",
        ]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return {
        "rows": len(dataframe),
        "entities": dataframe["provider_country_id"].nunique(dropna=True),
        "minimum_year": int(dataframe["year"].min()),
        "maximum_year": int(dataframe["year"].max()),
        "indicator_count": len(indicator_columns),
        "duplicate_keys": duplicate_keys,
        "missingness": missingness,
        "aggregate_examples": aggregate_examples,
    }


def print_annual_macro_panel_summary(summary: dict[str, object]) -> None:
    """Print a readable annual-panel validation summary."""
    print("Annual Macro Panel Summary")
    print("--------------------------")
    print(f"Rows:             {summary['rows']}")
    print(f"Entities:         {summary['entities']}")
    print(f"Years:            {summary['minimum_year']}–{summary['maximum_year']}")
    print(f"Indicators:       {summary['indicator_count']}")
    print(f"Duplicate keys:   {summary['duplicate_keys']}")

    print("\nMissing values by indicator:")
    missingness = summary["missingness"]

    if isinstance(missingness, dict):
        for variable, missing_count in missingness.items():
            print(f"  {variable}: {missing_count}")

    print("\nAggregate examples:")
    aggregate_examples = summary["aggregate_examples"]

    if isinstance(aggregate_examples, list):
        for aggregate in aggregate_examples:
            print(f"  {aggregate}")
