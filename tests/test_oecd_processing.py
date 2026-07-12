"""Tests for OECD processing."""

from pathlib import Path

import pandas as pd

from macro_data_factory.processing.oecd import process_series


def test_process_series(tmp_path: Path) -> None:
    """Convert a small OECD CSV into standardized Parquet."""
    input_path = tmp_path / "series.csv"
    output_path = tmp_path / "series.parquet"

    dataframe = pd.DataFrame(
        {
            "STRUCTURE_ID": ["OECD.TEST:FLOW(1.0)", "OECD.TEST:FLOW(1.0)"],
            "REF_AREA": ["AUS", "AUS"],
            "Reference area": ["Australia", "Australia"],
            "FREQ": ["A", "A"],
            "TIME_PERIOD": [2021, 2022],
            "OBS_VALUE": [100.0, 110.0],
            "UNIT_MEASURE": ["XDC", "XDC"],
            "Unit of measure": ["National currency", "National currency"],
            "UNIT_MULT": [6, 6],
            "CURRENCY": ["AUD", "AUD"],
            "Currency": ["Australian dollar", "Australian dollar"],
        }
    )

    dataframe.to_csv(input_path, index=False)

    result_path = process_series(
        input_path=input_path,
        output_path=output_path,
        series_name="test_series",
    )

    result = pd.read_parquet(result_path)

    assert result_path == output_path
    assert result.shape == (2, 13)
    assert result["series_name"].tolist() == ["test_series", "test_series"]
    assert result["provider_entity_id"].tolist() == ["AUS", "AUS"]
    assert result["year"].tolist() == [2021, 2022]
    assert result["value"].tolist() == [100.0, 110.0]
    assert result["currency_code"].tolist() == ["AUD", "AUD"]
