"""Read World Bank configuration."""

from __future__ import annotations

from pathlib import Path

import yaml


def load_indicators(config_path: Path) -> list[dict[str, str]]:
    """Load World Bank indicators from a YAML configuration file."""

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    indicators = config.get("indicators", [])

    if not isinstance(indicators, list):
        raise ValueError("'indicators' must be a list.")

    for indicator in indicators:
        if "code" not in indicator or "name" not in indicator:
            raise ValueError(
                "Each indicator must define 'code' and 'name'."
            )

    return indicators