"""Tests for OECD configuration loading."""

from pathlib import Path

import pytest

from macro_data_factory.config.oecd import load_series


def test_load_series(tmp_path: Path) -> None:
    """Load a valid OECD series definition."""
    config_path = tmp_path / "oecd.yml"
    config_path.write_text(
        """
series:
  - name: test_series
    agency: OECD.TEST
    dataset: TEST_DATASET
    version: "1.0"
    selection: A.AUS
    parameters:
      startPeriod: "2020"
      format: csvfilewithlabels
""",
        encoding="utf-8",
    )

    series = load_series(config_path)

    assert series == [
        {
            "name": "test_series",
            "agency": "OECD.TEST",
            "dataset": "TEST_DATASET",
            "version": "1.0",
            "selection": "A.AUS",
            "parameters": {
                "startPeriod": "2020",
                "format": "csvfilewithlabels",
            },
        }
    ]


def test_load_series_requires_all_fields(tmp_path: Path) -> None:
    """Reject an OECD series missing a required field."""
    config_path = tmp_path / "oecd.yml"
    config_path.write_text(
        """
series:
  - name: test_series
    agency: OECD.TEST
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing required fields"):
        load_series(config_path)
