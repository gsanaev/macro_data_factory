"""Command-line interface for Macro Data Factory."""

from pathlib import Path

import typer

from macro_data_factory.processing.world_bank import process_indicator
from macro_data_factory.providers.world_bank import download_indicator

app = typer.Typer(help="Build reproducible research datasets for empirical economics.")

RAW_WORLD_BANK_DIR = Path("data/raw/world_bank")
INTERIM_WORLD_BANK_DIR = Path("data/interim/world_bank")


@app.command()
def download(indicator: str) -> None:
    """Download one World Bank indicator as raw JSON."""
    download_indicator(
        indicator=indicator,
        output_dir=RAW_WORLD_BANK_DIR,
    )


@app.command()
def process(indicator: str) -> None:
    """Process one local World Bank JSON file into Parquet."""
    input_path = RAW_WORLD_BANK_DIR / f"{indicator}.json"
    output_path = INTERIM_WORLD_BANK_DIR / f"{indicator}.parquet"

    process_indicator(
        input_path=input_path,
        output_path=output_path,
    )


@app.command()
def pipeline(indicator: str) -> None:
    """Download and process one World Bank indicator."""
    download_indicator(
        indicator=indicator,
        output_dir=RAW_WORLD_BANK_DIR,
    )

    process_indicator(
        input_path=RAW_WORLD_BANK_DIR / f"{indicator}.json",
        output_path=INTERIM_WORLD_BANK_DIR / f"{indicator}.parquet",
    )


if __name__ == "__main__":
    app()
