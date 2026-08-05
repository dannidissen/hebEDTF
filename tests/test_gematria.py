"""Tests for hebedtf.gematria module."""

import pytest

from hebedtf.gematria import parse_gematria, parse_hebrew_day, parse_hebrew_year


def test_parse_gematria_single_letters():
    assert parse_gematria("א") == 1
    assert parse_gematria("י") == 10
    assert parse_gematria("ק") == 100
    assert parse_gematria("ת") == 400


def test_parse_gematria_combinations():
    assert parse_gematria("כ\"ג") == 23
    assert parse_gematria("ט\"ו") == 15
    assert parse_gematria("ט\"ז") == 16
    assert parse_gematria("תרפ\"ז") == 687
    assert parse_gematria("תשפ\"ד") == 784


def test_parse_gematria_punctuation_variations():
    assert parse_gematria("כג") == 23
    assert parse_gematria("כ'ג") == 23
    assert parse_gematria("כ״ג") == 23
    assert parse_gematria("תרפז") == 687


def test_parse_hebrew_day():
    assert parse_hebrew_day("א'") == 1
    assert parse_hebrew_day("י\"ד") == 14
    assert parse_hebrew_day("ט\"ו") == 15
    assert parse_hebrew_day("כ\"ט") == 29
    assert parse_hebrew_day("ל'") == 30

    with pytest.raises(ValueError):
        parse_hebrew_day("ל\"א")


def test_parse_hebrew_year():
    assert parse_hebrew_year("תשפ\"ד") == 5784
    assert parse_hebrew_year("תשפד") == 5784
    assert parse_hebrew_year("ה'תשפ\"ד") == 5784
    assert parse_hebrew_year("התשפ\"ד") == 5784
    assert parse_hebrew_year("תרפ\"ז") == 5687
    assert parse_hebrew_year("ה'תרפ\"ז") == 5687
    assert parse_hebrew_year("תש\"ג") == 5703
