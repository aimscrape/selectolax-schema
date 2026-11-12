from __future__ import annotations

import json
from pathlib import Path

import pytest

from selectolax_schema import extract, extract_from_file
from selectolax_schema.cli import main


def test_text_excludes_script_style_and_comments_without_mutating_tree() -> None:
    html = (
        '<div id="content">before<span>child</span><!-- comment -->'
        '<script>bad()</script><style>.bad {}</style>after</div>'
    )
    spec = {
        "fields": {
            "text": {"css": "#content", "type": "string"},
            "script": {"css": "#content script", "type": "string"},
            "style_html": {
                "css": "#content style",
                "type": "string",
                "attr": "innerHTML",
            },
        }
    }

    result = extract(html, spec)

    assert result["text"] == "beforechildafter"
    # Reading the parent text must not decompose or otherwise mutate the tree.
    assert result["script"] == ""
    assert result["style_html"] == '<style>.bad {}</style>'


@pytest.mark.parametrize("example", ["article", "product_list", "profiles"])
def test_documented_examples_match_expected_output(example: str) -> None:
    root = Path(__file__).resolve().parents[1]
    example_dir = root / "example" / example
    html = (example_dir / "page.html").read_text(encoding="utf-8")
    expected = json.loads((example_dir / "expected.json").read_text(encoding="utf-8"))

    assert extract_from_file(html, str(example_dir / "spec.yml")) == expected


def test_cli_extracts_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    spec_path = tmp_path / "spec.yml"
    html_path = tmp_path / "page.html"
    spec_path.write_text(
        'fields:\n  title: {css: "h1", type: "string"}\n',
        encoding="utf-8",
    )
    html_path.write_text("<h1>Hello</h1>", encoding="utf-8")

    exit_code = main(["--spec", str(spec_path), "--html-file", str(html_path)])

    assert exit_code == 0
    assert json.loads(capsys.readouterr().out) == {"title": "Hello"}


def test_cli_reports_validation_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    spec_path = tmp_path / "spec.yml"
    spec_path.write_text(
        'fields:\n  title: {css: "h1", type: "string", required: true}\n',
        encoding="utf-8",
    )

    exit_code = main(["--spec", str(spec_path), "--html", "<p>Missing</p>"])

    captured = capsys.readouterr()
    assert exit_code == 3
    assert captured.out == ""
    assert "Validation error: fields.title is required." in captured.err


def test_cli_emits_json_schema(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    spec_path = tmp_path / "spec.yml"
    spec_path.write_text(
        'fields:\n  title: {css: "h1", type: "string"}\n',
        encoding="utf-8",
    )

    exit_code = main(["--spec", str(spec_path), "--schema"])

    assert exit_code == 0
    emitted = json.loads(capsys.readouterr().out)
    assert emitted["title"] == "selectolax-schema output"
    assert emitted["properties"]["title"]["type"] == ["string", "null"]
