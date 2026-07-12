"""Command-line commands for the OECD provider."""

from pathlib import Path

import typer

from macro_data_factory.config.oecd import load_series
from macro_data_factory.processing.oecd import process_series
from macro_data_factory.providers.oecd import download_series
from macro_data_factory.validation.oecd import print_summary, summarize_dataset


app = typer.Typer(help="Download, process, and validate OECD data.")

OECD_CONFIG_PATH = Path("configs/oecd.yml")
RAW_OECD_DIR = Path("data/raw/oecd")
INTERIM_OECD_DIR = Path("data/interim/oecd")


def get_configured_series() -> list[dict[str, object]]:
    """Load configured OECD series and ensure that the list is not empty."""
    series_definitions = load_series(OECD_CONFIG_PATH)

    if not series_definitions:
        raise ValueError("No OECD series found in the configuration.")

    return series_definitions


@app.command()
def download() -> None:
    """Download all configured OECD series as raw CSV files."""
    series_definitions = get_configured_series()

    for series in series_definitions:
        series_name = str(series["name"])
        typer.echo(f"Downloading OECD series {series_name}")

        download_series(
            series=series,
            output_dir=RAW_OECD_DIR,
        )

    typer.echo(f"Downloaded {len(series_definitions)} OECD series.")


@app.command()
def process() -> None:
    """Process all local OECD raw files into interim Parquet files."""
    series_definitions = get_configured_series()

    for series in series_definitions:
        series_name = str(series["name"])
        typer.echo(f"Processing OECD series {series_name}")

        process_series(
            input_path=RAW_OECD_DIR / f"{series_name}.csv",
            output_path=INTERIM_OECD_DIR / f"{series_name}.parquet",
            series_name=series_name,
        )

    typer.echo(f"Processed {len(series_definitions)} OECD series.")


@app.command()
def validate() -> None:
    """Validate all configured OECD interim datasets."""
    series_definitions = get_configured_series()

    for series in series_definitions:
        series_name = str(series["name"])
        input_path = INTERIM_OECD_DIR / f"{series_name}.parquet"

        typer.echo(f"\nValidating OECD series {series_name}")

        summary = summarize_dataset(input_path)
        print_summary(summary)

    typer.echo(f"\nValidated {len(series_definitions)} OECD series.")


@app.command()
def build() -> None:
    """Run the complete configured OECD workflow."""
    series_definitions = get_configured_series()

    for series in series_definitions:
        series_name = str(series["name"])

        typer.echo(f"\nRunning OECD pipeline for {series_name}")

        download_series(
            series=series,
            output_dir=RAW_OECD_DIR,
        )

        interim_path = INTERIM_OECD_DIR / f"{series_name}.parquet"

        process_series(
            input_path=RAW_OECD_DIR / f"{series_name}.csv",
            output_path=interim_path,
            series_name=series_name,
        )

        summary = summarize_dataset(interim_path)
        print_summary(summary)

    typer.echo("\nOECD workflow completed successfully.")
