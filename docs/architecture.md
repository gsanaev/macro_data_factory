# Architecture

## Purpose

Macro Data Factory is a reusable research data infrastructure for empirical economics.

Its responsibility is to acquire, validate, harmonize, document, merge, and export research-quality datasets. Econometric analysis and paper-specific work belong in separate downstream repositories.

## Architectural Principles

- Separate data acquisition from data processing.
- Separate data engineering from econometric analysis.
- Preserve raw source data and complete provenance.
- Use configuration for dataset definitions where practical.
- Validate data before release.
- Build reusable dataset products rather than one universal master dataset.
- Add complexity only when a concrete need justifies it.

## Repository Structure

```text
macro_data_factory/
├── .github/
│   └── workflows/
├── configs/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── releases/
├── docs/
├── src/
│   └── macro_data_factory/
├── tests/
├── LICENSE
├── README.md
├── pyproject.toml
└── uv.lock