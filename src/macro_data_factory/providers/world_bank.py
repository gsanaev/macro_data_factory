"""Download raw indicator data from the World Bank API."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

BASE_URL = "https://api.worldbank.org/v2"
DEFAULT_TIMEOUT = 30


def build_indicator_url(indicator: str) -> str:
    """Build the World Bank API URL for one indicator."""
    indicator = indicator.strip()

    if not indicator:
        raise ValueError("Indicator code must not be empty.")

    return f"{BASE_URL}/country/all/indicator/{indicator}"


def fetch_indicator(
    indicator: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> Any:
    """Download one indicator from the World Bank API.

    The function returns the original decoded JSON response without
    cleaning or reshaping it.
    """
    url = build_indicator_url(indicator)

    params = {
        "format": "json",
        "per_page": 20_000,
    }

    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()

    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(
            f"Unexpected World Bank API response for indicator {indicator!r}."
        )

    return payload


def save_raw_response(
    payload: Any,
    indicator: str,
    output_dir: Path,
) -> Path:
    """Save the original World Bank JSON response to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{indicator}.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    return output_path


def download_indicator(
    indicator: str,
    output_dir: Path,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> Path:
    """Download one World Bank indicator and save its raw JSON response."""
    payload = fetch_indicator(indicator, timeout=timeout)
    output_path = save_raw_response(payload, indicator, output_dir)

    print(f"Downloaded {indicator} to {output_path}")

    return output_path