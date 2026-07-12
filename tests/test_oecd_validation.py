"""Tests for OECD validation."""

from pathlib import Path

import pandas as pd

from macro_data_factory.validation.oecd import summarize_dataset


def test_summarize_oecd_dataset(tmp_path: Path) -> None:
    """Summarize one valid OECD interim dataset."""
    input_path = tmp_path / "series.parquet"

    dataframe = pd.DataFrame(
        {
            "series_name": ["test_series", "test_series"],
            "provider_series_id": [
                "OECD.TEST:FLOW(1.0)",
                "OECD.TEST:FLOW(1.0)",
            ],
            "provider_entity_id": ["AUS", "AUS"],
            "country_code": ["AUS", "AUS"],
            "country_name": ["Australia", "Australia"],
            "year": [2021, 2022],
            "value": [100.0, 110.0],
            "unit_code": ["XDC", "XDC"],
            "unit": ["National currency", "National currency"],
            "unit_multiplier": [6, 6],
            "currency_code": ["AUD", "AUD"],
            "currency": ["Australian dollar", "Australian dollar"],
            "frequency": ["A", "A"],
        }
    )

    dataframe.to_parquet(input_path, index=False)

    summary = summarize_dataset(input_path)

    assert summary["series_name"] == "test_series"
    assert summary["rows"] == 2
    assert summary["entities"] == 1
    assert summary["minimum_year"] == 2021
    assert summary["maximum_year"] == 2022
    assert summary["missing_values"] == 0
    assert summary["duplicate_keys"] == 0
    assert summary["frequency"] == "A"
    assert summary["unit_multiplier"] == 6
