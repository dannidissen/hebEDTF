"""Corpus tests for hebEDTF using real-world catalog date expressions."""

import json
from pathlib import Path

import edtf
import pytest

from hebedtf import hebrew_to_edtf

CORPUS_FILE = Path(__file__).parent / "fixtures" / "catalog_corpus.json"


def load_corpus():
    with open(CORPUS_FILE, encoding="utf-8") as f:
        return json.load(f)


CORPUS_DATA = load_corpus()


@pytest.mark.parametrize("entry", CORPUS_DATA, ids=lambda e: e["input"])
def test_catalog_corpus_entry(entry):
    hebrew_input = entry["input"]
    expected_edtf = entry["expected"]

    result = hebrew_to_edtf(hebrew_input)

    assert result == expected_edtf, (
        f"Failed for '{hebrew_input}': got '{result}', expected '{expected_edtf}'"
    )

    parsed_obj = edtf.parse_edtf(result)
    assert parsed_obj is not None, (
        f"Generated EDTF '{result}' for '{hebrew_input}' failed edtf.parse_edtf()"
    )
