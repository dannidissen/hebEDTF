"""Tests for hebedtf.parser module."""

import pytest

from hebedtf.parser import parse_hebrew_date_text


def test_parse_year_only():
    comp = parse_hebrew_date_text("תשפ\"ד")
    assert comp.day is None
    assert comp.month_str is None
    assert comp.year == 5784


def test_parse_year_only_with_prefix():
    comp = parse_hebrew_date_text("שנת ה'תרפ\"ז")
    assert comp.day is None
    assert comp.month_str is None
    assert comp.year == 5687


def test_parse_month_and_year():
    comp = parse_hebrew_date_text("תשרי תשפ\"ד")
    assert comp.day is None
    assert comp.month_str == "תשרי"
    assert comp.year == 5784


def test_parse_month_and_year_with_prefix():
    comp = parse_hebrew_date_text("בחודש אדר ב' תשפ\"ד")
    assert comp.day is None
    assert comp.month_str == "אדר ב'"
    assert comp.year == 5784


def test_parse_full_date():
    comp = parse_hebrew_date_text("כ\"ג בתשרי תשפ\"ד")
    assert comp.day == 23
    assert comp.month_str == "בתשרי"
    assert comp.year == 5784


def test_parse_full_date_without_be():
    comp = parse_hebrew_date_text("א' ניסן ה'תשפ\"ד")
    assert comp.day == 1
    assert comp.month_str == "ניסן"
    assert comp.year == 5784


def test_parse_full_date_adar_ii():
    comp = parse_hebrew_date_text("ט\"ו אדר שני תשפ\"ד")
    assert comp.day == 15
    assert comp.month_str == "אדר שני"
    assert comp.year == 5784


def test_parse_invalid_text():
    with pytest.raises(ValueError):
        parse_hebrew_date_text("טקסט לא קשור")
