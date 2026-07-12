"""Command-line interface for Macro Data Factory."""

from pathlib import Path

import typer

from macro_data_factory.config.world_bank import load_indicator_list
from macro_data_factory.processing.world_bank import process_indicator
from macro_data_factory.providers.world_bank import download_indicator
from macro_data_factory.validation.world_bank import print_summary, summarize_dataset

app = typer.Typer(help="Build reproducible research datasets for empirical economics.")

RAW_WORLD_BANK_DIR = Path("data/raw/world_bank")
INTERIM_WORLD_BANK_DIR = Path("data/interim/world_bank")
WORLD_BANK_CONFIG_PATH = Path("configs/world_bank.yml")


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


@app.command()
def validate(indicator: str) -> None:
    """Validate one interim World Bank Parquet file."""
    input_path = INTERIM_WORLD_BANK_DIR / f"{indicator}.parquet"

    summary = summarize_dataset(input_path)
    print_summary(summary)


@app.command("world-bank")
def world_bank() -> None:
    """Download and process all configured World Bank indicators."""
    indicators = load_indicator_list(WORLD_BANK_CONFIG_PATH)

    if not indicators:
        raise ValueError("No World Bank indicators found in the configuration.")

    for indicator in indicators:
        typer.echo(f"Running pipeline for {indicator}")

        download_indicator(
            indicator=indicator,
            output_dir=RAW_WORLD_BANK_DIR,
        )

        process_indicator(
            input_path=RAW_WORLD_BANK_DIR / f"{indicator}.json",
            output_path=INTERIM_WORLD_BANK_DIR / f"{indicator}.parquet",
        )

    typer.echo(f"Completed {len(indicators)} World Bank indicators.")


if __name__ == "__main__":
    app()
