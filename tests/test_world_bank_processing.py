"""Tests for processing raw World Bank data."""

import json
from pathlib import Path

import pandas as pd

from macro_data_factory.processing.world_bank import process_indicator


def test_process_indicator(tmp_path: Path) -> None:
    """Convert a small raw World Bank response into Parquet."""
    input_path = tmp_path / "SP.POP.TOTL.json"
    output_path = tmp_path / "SP.POP.TOTL.parquet"

    payload = [
        {"page": 1, "pages": 1, "total": 2},
        [
            {
                "indicator": {
                    "id": "SP.POP.TOTL",
                    "value": "Population, total",
                },
                "country": {
                    "id": "AF",
                    "value": "Afghanistan",
                },
                "countryiso3code": "AFG",
                "date": "2020",
                "value": 38972230,
                "unit": "",
                "obs_status": "",
                "decimal": 0,
            },
            {
                "indicator": {
                    "id": "SP.POP.TOTL",
                    "value": "Population, total",
                },
                "country": {
                    "id": "AF",
                    "value": "Afghanistan",
                },
                "countryiso3code": "AFG",
                "date": "2021",
                "value": 40099462,
                "unit": "",
                "obs_status": "",
                "decimal": 0,
            },
        ],
    ]

    input_path.write_text(json.dumps(payload), encoding="utf-8")

    result_path = process_indicator(input_path, output_path)
    dataframe = pd.read_parquet(result_path)

    assert result_path == output_path
    assert dataframe.shape == (2, 10)
    assert dataframe["provider_country_id"].tolist() == ["AF", "AF"]
    assert dataframe["country_code"].tolist() == ["AFG", "AFG"]
    assert dataframe["year"].tolist() == [2020, 2021]
    assert dataframe["value"].tolist() == [38972230, 40099462]
