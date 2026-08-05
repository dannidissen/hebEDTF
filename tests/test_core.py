"""Tests for hebEDTF core module."""

import pytest

from hebedtf import hebrew_to_edtf


def test_hebrew_to_edtf_empty_raises_value_error():
    with pytest.raises(ValueError):
        hebrew_to_edtf("")


def test_hebrew_to_edtf_skeleton_year():
    res = hebrew_to_edtf('תשפ"ד')
    assert res == "2023-09-16/2024-10-03"
