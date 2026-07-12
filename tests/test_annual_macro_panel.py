"""Tests for building the annual macro panel."""

from pathlib import Path

import pandas as pd

from macro_data_factory.products.annual_macro_panel import (
    build_annual_macro_panel,
)


def write_indicator(
    path: Path,
    indicator_code: str,
    values: list[float],
) -> None:
    """Write a small interim indicator dataset."""
    dataframe = pd.DataFrame(
        {
            "indicator_code": [indicator_code, indicator_code],
            "provider_country_id": ["AF", "AF"],
            "country_code": ["AFG", "AFG"],
            "country_name": ["Afghanistan", "Afghanistan"],
            "year": [2020, 2021],
            "value": values,
        }
    )
    dataframe.to_parquet(path, index=False)


def test_build_panel_uses_only_configured_indicators(
    tmp_path: Path,
) -> None:
    """Ignore interim files that are not listed in configuration."""
    input_dir = tmp_path / "interim"
    input_dir.mkdir()

    write_indicator(
        input_dir / "SP.POP.TOTL.parquet",
        "SP.POP.TOTL",
        [100.0, 110.0],
    )
    write_indicator(
        input_dir / "NY.GDP.MKTP.CD.parquet",
        "NY.GDP.MKTP.CD",
        [200.0, 220.0],
    )
    write_indicator(
        input_dir / "OLD.INDICATOR.parquet",
        "OLD.INDICATOR",
        [1.0, 2.0],
    )

    output_path = tmp_path / "annual_macro_panel.parquet"

    build_annual_macro_panel(
        input_dir=input_dir,
        output_path=output_path,
        indicator_names={
            "SP.POP.TOTL": "population_total",
            "NY.GDP.MKTP.CD": "gdp_current_usd",
        },
        indicator_codes=[
            "SP.POP.TOTL",
            "NY.GDP.MKTP.CD",
        ],
    )

    dataframe = pd.read_parquet(output_path)

    assert dataframe.shape == (2, 6)
    assert dataframe.columns.tolist() == [
        "provider_country_id",
        "country_code",
        "country_name",
        "year",
        "population_total",
        "gdp_current_usd",
    ]
    assert "OLD.INDICATOR" not in dataframe.columns
    assert not dataframe.duplicated(["provider_country_id", "year"]).any()

    assert output_path.with_suffix(".dta").exists()
