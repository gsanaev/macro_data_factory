"""Tests for World Bank interim-data validation."""

from pathlib import Path

import pandas as pd

from macro_data_factory.validation.world_bank import summarize_dataset


def test_summarize_dataset_detects_duplicate_keys(
    tmp_path: Path,
) -> None:
    """Count duplicate provider-entity-year observations."""
    input_path = tmp_path / "indicator.parquet"

    dataframe = pd.DataFrame(
        {
            "indicator_code": ["TEST.CODE", "TEST.CODE"],
            "provider_country_id": ["AF", "AF"],
            "country_code": ["AFG", "AFG"],
            "country_name": ["Afghanistan", "Afghanistan"],
            "year": [2020, 2020],
            "value": [1.0, 2.0],
        }
    )
    dataframe.to_parquet(input_path, index=False)

    summary = summarize_dataset(input_path)

    assert summary["rows"] == 2
    assert summary["countries"] == 1
    assert summary["duplicate_keys"] == 1
