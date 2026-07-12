"""Build the annual macroeconomic country-year panel."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


KEY_COLUMNS = [
    "provider_country_id",
    "country_code",
    "country_name",
    "year",
]


def load_indicator_data(
    input_path: Path,
    indicator_names: dict[str, str],
) -> pd.DataFrame:
    """Load one interim indicator dataset and prepare it for merging."""
    if not input_path.exists():
        raise FileNotFoundError(f"Interim indicator file not found: {input_path}")

    dataframe = pd.read_parquet(input_path)

    required_columns = {
        "indicator_code",
        "provider_country_id",
        "country_code",
        "country_name",
        "year",
        "value",
    }

    missing_columns = required_columns.difference(dataframe.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns in {input_path}: {missing}")

    indicator_codes = dataframe["indicator_code"].dropna().unique()

    if len(indicator_codes) != 1:
        raise ValueError(
            f"Expected one indicator code in {input_path}, "
            f"found {len(indicator_codes)}."
        )

    indicator_code = str(indicator_codes[0])

    if indicator_code not in indicator_names:
        raise ValueError(
            f"Indicator code {indicator_code} not is not defined in the configuration."
        )

    variable_name = indicator_names[indicator_code]

    if dataframe.duplicated(KEY_COLUMNS).any():
        raise ValueError(f"Duplicate country-year keys found in {input_path}")

    return dataframe[KEY_COLUMNS + ["value"]].rename(columns={"value": variable_name})


def build_annual_macro_panel(
    input_dir: Path,
    output_path: Path,
    indicator_names: dict[str, str],
    indicator_codes: list[str],
) -> Path:
    """Merge all interim World Bank indicators into one annual panel."""
    input_files = [
        input_dir / f"{indicator_code}.parquet" for indicator_code in indicator_codes
    ]

    if not input_files:
        raise FileNotFoundError(f"No interim Parquet files found in: {input_dir}")

    panel: pd.DataFrame | None = None

    for input_file in input_files:
        indicator_data = load_indicator_data(
            input_file,
            indicator_names=indicator_names,
        )

        if panel is None:
            panel = indicator_data
        else:
            panel = panel.merge(
                indicator_data,
                on=KEY_COLUMNS,
                how="outer",
                validate="one_to_one",
            )

    if panel is None:
        raise RuntimeError("Annual macro panel could not be built.")

    panel = panel.sort_values(["provider_country_id", "year"]).reset_index(drop=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    panel.to_parquet(output_path, index=False)

    stata_output_path = output_path.with_suffix(".dta")

    panel.to_stata(
        stata_output_path,
        write_index=False,
        version=118,
    )

    print(f"Built annual macro panel at {output_path}")
    print(f"Built Stata dataset at {stata_output_path}")
    print(f"Rows: {len(panel)}")
    print(f"Columns: {len(panel.columns)}")

    return output_path
