"""Read OECD configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


REQUIRED_SERIES_FIELDS = {
    "name",
    "agency",
    "dataset",
    "version",
    "selection",
}


def load_series(config_path: Path) -> list[dict[str, Any]]:
    """Load OECD series definitions from a YAML configuration file."""
    if not config_path.exists():
        raise FileNotFoundError(f"OECD configuration file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("OECD configuration must contain a YAML mapping.")

    series = config.get("series", [])

    if not isinstance(series, list):
        raise ValueError("'series' must be a list.")

    for item in series:
        if not isinstance(item, dict):
            raise ValueError("Each OECD series definition must be a mapping.")

        missing_fields = REQUIRED_SERIES_FIELDS.difference(item)

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(
                f"OECD series definition is missing required fields: {missing}"
            )

        parameters = item.get("parameters", {})

        if not isinstance(parameters, dict):
            raise ValueError("'parameters' must be a mapping.")

    return series
