# Macro Data Factory

> A reproducible research data infrastructure for empirical economics.

## Overview

Macro Data Factory is a long-term research data infrastructure designed to build, validate, harmonize, document, and export high-quality macroeconomic datasets from authoritative international data providers.

Unlike a typical empirical research repository, Macro Data Factory is **not** intended to produce econometric analyses, regression results, or research manuscripts.

Its primary purpose is to produce **research-ready datasets** that can be reused across multiple empirical research projects.

## Mission

Macro Data Factory is not a repository for a single paper.

It is a repository for building research-quality datasets that support an entire empirical research program.

The repository emphasizes:

- reproducibility
- modularity
- transparency
- metadata
- validation
- long-term maintainability

## Project Scope

The repository will eventually support data acquisition and harmonization from international data providers such as:

- World Bank
- OECD
- Eurostat
- ILO
- FAO
- UNDP
- FRED
- IMF
- and other relevant public databases

The primary outputs are:

- research-ready country-year datasets
- research-ready country-quarter datasets
- research-ready country-month datasets
- metadata
- validation reports
- Stata datasets
- Parquet datasets

## Guiding Principles

- Build reusable datasets rather than project-specific datasets.
- Separate data engineering from econometric analysis.
- Separate data acquisition from paper writing.
- Make every processing step reproducible.
- Preserve complete metadata and source traceability.
- Design the repository so new datasets and data providers can be added easily.

## Technology

- Python for data engineering
- Stata for downstream econometric analysis
- uv for project management
- Git and GitHub for version control
- GitHub Actions for continuous integration

## Repository Status

🚧 This project is currently under active development.

The repository architecture is being designed before implementation begins in order to ensure long-term maintainability and reproducibility.

## License

This project is released under the MIT License.