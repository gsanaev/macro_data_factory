"""Tests for World Bank configuration loading."""

from pathlib import Path

import pytest

from macro_data_factory.config.world_bank import load_indicators


def test_load_indicators(tmp_path: Path) -> None:
    """Load valid indicator records from YAML."""
    config_path = tmp_path / "world_bank.yml"
    config_path.write_text(
        """
indicators:
  - code: SP.POP.TOTL
    name: population_total
  - code: NY.GDP.MKTP.CD
    name: gdp_current_usd
""",
        encoding="utf-8",
    )

    indicators = load_indicators(config_path)

    assert indicators == [
        {"code": "SP.POP.TOTL", "name": "population_total"},
        {"code": "NY.GDP.MKTP.CD", "name": "gdp_current_usd"},
    ]


def test_load_indicators_requires_code_and_name(tmp_path: Path) -> None:
    """Reject indicator records without required fields."""
    config_path = tmp_path / "world_bank.yml"
    config_path.write_text(
        """
indicators:
  - code: SP.POP.TOTL
""",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Each indicator must define 'code' and 'name'.",
    ):
        load_indicators(config_path)
