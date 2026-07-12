"""Download raw data from the OECD SDMX API."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import requests


BASE_URL = "https://sdmx.oecd.org/public/rest/data"
DEFAULT_TIMEOUT = 60


def build_data_url(series: dict[str, Any]) -> str:
    """Build an OECD SDMX data URL from one series definition."""
    agency = str(series["agency"]).strip()
    dataset = str(series["dataset"]).strip()
    version = str(series["version"]).strip()
    selection = str(series["selection"]).strip()

    if not all([agency, dataset, version, selection]):
        raise ValueError(
            "OECD agency, dataset, version, and selection must not be empty."
        )

    return f"{BASE_URL}/{agency},{dataset},{version}/{selection}"


def fetch_series(
    series: dict[str, Any],
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> bytes:
    """Download one configured OECD series and return the raw response."""
    url = build_data_url(series)
    parameters = series.get("parameters", {})

    response = requests.get(
        url,
        params=parameters,
        timeout=timeout,
    )
    response.raise_for_status()

    if not response.content:
        raise ValueError(f"OECD returned an empty response for {series['name']!r}.")

    return response.content


def save_raw_response(
    content: bytes,
    series_name: str,
    output_dir: Path,
) -> Path:
    """Save an untouched OECD CSV response to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{series_name}.csv"
    output_path.write_bytes(content)

    return output_path


def download_series(
    series: dict[str, Any],
    output_dir: Path,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> Path:
    """Download one configured OECD series and save its raw CSV response."""
    series_name = str(series["name"]).strip()

    if not series_name:
        raise ValueError("OECD series name must not be empty.")

    content = fetch_series(series, timeout=timeout)
    output_path = save_raw_response(
        content=content,
        series_name=series_name,
        output_dir=output_dir,
    )

    print(f"Downloaded {series_name} to {output_path}")

    return output_path
