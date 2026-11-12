from __future__ import annotations

from importlib.metadata import version

import pytest

import selectolax_schema
from selectolax_schema.cli import main


def test_package_version_matches_distribution_metadata() -> None:
    assert selectolax_schema.__version__ == version("selectolax-schema")


def test_cli_reports_distribution_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])

    assert exc_info.value.code == 0
    assert capsys.readouterr().out.strip() == (
        f"selectolax-schema {selectolax_schema.__version__}"
    )
