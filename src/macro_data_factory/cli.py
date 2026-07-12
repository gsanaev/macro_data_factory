"""Command-line interface for Macro Data Factory."""

from pathlib import Path

import typer

from macro_data_factory.config.world_bank import load_indicators
from macro_data_factory.processing.world_bank import process_indicator
from macro_data_factory.providers.world_bank import download_indicator
from macro_data_factory.validation.world_bank import print_summary, summarize_dataset
from macro_data_factory.products.annual_macro_panel import (
    build_annual_macro_panel,
)
from macro_data_factory.validation.annual_macro_panel import (
    print_annual_macro_panel_summary,
    summarize_annual_macro_panel,
)

app = typer.Typer(help="Build reproducible research datasets for empirical economics.")

RAW_WORLD_BANK_DIR = Path("data/raw/world_bank")
INTERIM_WORLD_BANK_DIR = Path("data/interim/world_bank")
WORLD_BANK_CONFIG_PATH = Path("configs/world_bank.yml")
PROCESSED_DIR = Path("data/processed")


@app.command("build-annual-panel")
def build_annual_panel() -> None:
    """Build the annual macroeconomic panel from interim datasets."""
    indicators = load_indicators(WORLD_BANK_CONFIG_PATH)

    indicator_names = {
        indicator["code"]: indicator["name"]
        for indicator in indicators
    }

    build_annual_macro_panel(
        input_dir=INTERIM_WORLD_BANK_DIR,
        output_path=PROCESSED_DIR / "annual_macro_panel.parquet",
        indicator_names=indicator_names,
    )


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
    indicators = load_indicators(WORLD_BANK_CONFIG_PATH)

    if not indicators:
        raise ValueError("No World Bank indicators found in the configuration.")

    for indicator in indicators:
        indicator_code = indicator["code"]
        
        typer.echo(f"Running pipeline for {indicator_code}")

        download_indicator(
            indicator=indicator_code,
            output_dir=RAW_WORLD_BANK_DIR,
        )

        process_indicator(
            input_path=RAW_WORLD_BANK_DIR / f"{indicator_code}.json",
            output_path=INTERIM_WORLD_BANK_DIR / f"{indicator_code}.parquet",
        )

    typer.echo(f"Completed {len(indicators)} World Bank indicators.")


@app.command("build-world-bank")
def build_world_bank() -> None:
    """Run the complete configured World Bank workflow."""
    indicators = load_indicators(WORLD_BANK_CONFIG_PATH)

    if not indicators:
        raise ValueError("No World Bank indicators found in the configuration.")

    indicator_names = {
        indicator["code"]: indicator["name"]
        for indicator in indicators
    }

    for indicator in indicators:
        indicator_code = indicator["code"]

        typer.echo(f"\nRunning pipeline for {indicator_code}")

        download_indicator(
            indicator=indicator_code,
            output_dir=RAW_WORLD_BANK_DIR,
        )

        interim_path = INTERIM_WORLD_BANK_DIR / f"{indicator_code}.parquet"

        process_indicator(
            input_path=RAW_WORLD_BANK_DIR / f"{indicator_code}.json",
            output_path=interim_path,
        )

        summary = summarize_dataset(interim_path)
        print_summary(summary)

    panel_path = PROCESSED_DIR / "annual_macro_panel.parquet"

    build_annual_macro_panel(
        input_dir=INTERIM_WORLD_BANK_DIR,
        output_path=panel_path,
        indicator_names=indicator_names,
    )

    panel_summary = summarize_annual_macro_panel(panel_path)
    print_annual_macro_panel_summary(panel_summary)

    typer.echo("\nWorld Bank workflow completed successfully.")
    

@app.command("validate-annual-panel")
def validate_annual_panel() -> None:
    """Validate the processed annual macroeconomic panel."""
    input_path = PROCESSED_DIR / "annual_macro_panel.parquet"

    summary = summarize_annual_macro_panel(input_path)
    print_annual_macro_panel_summary(summary)


if __name__ == "__main__":
    app()
