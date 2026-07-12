"""Process raw OECD CSV responses into standardized interim datasets."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "STRUCTURE_ID",
    "REF_AREA",
    "Reference area",
    "FREQ",
    "TIME_PERIOD",
    "OBS_VALUE",
    "UNIT_MEASURE",
    "Unit of measure",
    "UNIT_MULT",
    "CURRENCY",
    "Currency",
}


def load_raw_data(input_path: Path) -> pd.DataFrame:
    """Load one raw OECD CSV response."""
    if not input_path.exists():
        raise FileNotFoundError(f"Raw OECD file not found: {input_path}")

    dataframe = pd.read_csv(input_path)

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required OECD columns: {missing}")

    if dataframe.empty:
        raise ValueError(f"OECD file contains no observations: {input_path}")

    return dataframe


def standardize_oecd_data(
    dataframe: pd.DataFrame,
    series_name: str,
) -> pd.DataFrame:
    """Convert an OECD response into the common interim structure."""
    standardized = pd.DataFrame(
        {
            "series_name": series_name,
            "provider_series_id": dataframe["STRUCTURE_ID"],
            "provider_entity_id": dataframe["REF_AREA"],
            "country_code": dataframe["REF_AREA"],
            "country_name": dataframe["Reference area"],
            "year": pd.to_numeric(
                dataframe["TIME_PERIOD"],
                errors="raise",
            ).astype("int64"),
            "value": pd.to_numeric(
                dataframe["OBS_VALUE"],
                errors="coerce",
            ),
            "unit_code": dataframe["UNIT_MEASURE"],
            "unit": dataframe["Unit of measure"],
            "unit_multiplier": pd.to_numeric(
                dataframe["UNIT_MULT"],
                errors="coerce",
            ),
            "currency_code": dataframe["CURRENCY"],
            "currency": dataframe["Currency"],
            "frequency": dataframe["FREQ"],
        }
    )

    standardized = standardized.sort_values(["provider_entity_id", "year"]).reset_index(
        drop=True
    )

    return standardized


def save_interim_data(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> Path:
    """Save standardized OECD data as Parquet."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_parquet(output_path, index=False)

    return output_path


def process_series(
    input_path: Path,
    output_path: Path,
    series_name: str,
) -> Path:
    """Process one raw OECD CSV file into interim Parquet."""
    dataframe = load_raw_data(input_path)
    standardized = standardize_oecd_data(dataframe, series_name)
    saved_path = save_interim_data(standardized, output_path)

    print(f"Processed {input_path} to {saved_path}")

    return saved_path
