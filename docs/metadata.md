# Metadata Standard

## Purpose

Metadata ensures that every variable and dataset produced by Macro Data Factory can be understood, verified, and traced to its original source.

Metadata should be maintained alongside the data-processing pipeline and included with every released dataset product.

## Source Metadata

Each data source should record:

- provider name
- database or dataset name
- source URL or API endpoint
- retrieval method
- retrieval date
- source version or vintage, when available
- license or usage conditions
- relevant source documentation

## Variable Metadata

Each variable should record:

- internal variable name
- original variable or series identifier
- variable label
- definition
- unit of measurement
- frequency
- provider
- source dataset
- geographical coverage
- temporal coverage
- transformations applied
- aggregation method, when applicable
- seasonal-adjustment status, when applicable
- known limitations or comparability concerns

## Dataset Metadata

Each dataset product should record:

- product name
- product version
- unit of observation
- frequency
- country coverage
- time coverage
- included variables
- build date
- source retrieval dates
- code version or Git commit
- validation status
- available export formats
- known limitations

## Provenance

Every released variable should be traceable through the following chain:

```text
released variable
        ↓
internal variable definition
        ↓
transformation history
        ↓
original provider series
        ↓
source dataset and retrieval record