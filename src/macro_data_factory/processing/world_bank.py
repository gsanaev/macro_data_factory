"""Process raw World Bank API responses into tabular datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def load_raw_response(input_path: Path) -> list[dict[str, Any]]:
    """Load observations from a raw World Bank API JSON file."""
    if not input_path.exists():
        raise FileNotFoundError(f"Raw World Bank file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Unexpected World Bank JSON structure: {input_path}")

    observations = payload[1]

    if not isinstance(observations, list):
        raise ValueError(f"World Bank observations must be a list: {input_path}")

    return observations


def observations_to_dataframe(
    observations: list[dict[str, Any]],
) -> pd.DataFrame:
    """Convert World Bank observations into a standardized table."""
    records = []

    for observation in observations:
        indicator = observation.get("indicator") or {}
        country = observation.get("country") or {}

        records.append(
            {
                "indicator_code": indicator.get("id"),
                "indicator_name": indicator.get("value"),
                "country_code": observation.get("countryiso3code"),
                "country_name": country.get("value"),
                "year": observation.get("date"),
                "value": observation.get("value"),
                "unit": observation.get("unit"),
                "observation_status": observation.get("obs_status"),
                "decimal": observation.get("decimal"),
            }
        )

    dataframe = pd.DataFrame.from_records(records)

    if dataframe.empty:
        raise ValueError("World Bank response contains no observations.")

    dataframe["year"] = pd.to_numeric(dataframe["year"], errors="raise").astype("int64")
    dataframe["value"] = pd.to_numeric(dataframe["value"], errors="coerce")

    return dataframe


def save_interim_data(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> Path:
    """Save standardized World Bank data as a Parquet file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_parquet(output_path, index=False)

    return output_path


def process_indicator(
    input_path: Path,
    output_path: Path,
) -> Path:
    """Process one raw World Bank indicator file into Parquet format."""
    observations = load_raw_response(input_path)
    dataframe = observations_to_dataframe(observations)
    saved_path = save_interim_data(dataframe, output_path)

    print(f"Processed {input_path} to {saved_path}")

    return saved_path
