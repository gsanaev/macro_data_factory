"""Read World Bank configuration."""

from __future__ import annotations

from pathlib import Path

import yaml


def load_indicator_list(config_path: Path) -> list[str]:
    """Load the list of World Bank indicators from a YAML file."""

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    indicators = config.get("indicators", [])

    if not isinstance(indicators, list):
        raise ValueError("'indicators' must be a list.")

    return indicators