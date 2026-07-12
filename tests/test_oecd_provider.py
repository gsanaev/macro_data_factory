"""Tests for OECD URL construction."""

from macro_data_factory.providers.oecd import build_data_url


def test_build_data_url() -> None:
    """Build the expected OECD SDMX data URL."""
    series = {
        "name": "test_series",
        "agency": "OECD.SDD.NAD",
        "dataset": "DSD_NAMAIN10@DF_TABLE1_EXPENDITURE",
        "version": "2.0",
        "selection": "A.AUS...B1GQ....XDC.V..",
    }

    url = build_data_url(series)

    assert url == (
        "https://sdmx.oecd.org/public/rest/data/"
        "OECD.SDD.NAD,"
        "DSD_NAMAIN10@DF_TABLE1_EXPENDITURE,"
        "2.0/"
        "A.AUS...B1GQ....XDC.V.."
    )
