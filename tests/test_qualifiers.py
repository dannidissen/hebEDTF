"""Tests for hebedtf.qualifiers module."""

from hebedtf.qualifiers import EDTFIntervalType, EDTFQualifier, extract_qualifiers


def test_extract_qualifiers_approximate():
    q = extract_qualifiers("בערך תשפ\"ד")
    assert q.qualifier == EDTFQualifier.APPROXIMATE
    assert q.clean_text == "תשפ\"ד"

    q2 = extract_qualifiers("סביבות תרפ\"ז")
    assert q2.qualifier == EDTFQualifier.APPROXIMATE
    assert q2.clean_text == "תרפ\"ז"

    q3 = extract_qualifiers("כ-תשפ\"ד")
    assert q3.qualifier == EDTFQualifier.APPROXIMATE
    assert q3.clean_text == "תשפ\"ד"


def test_extract_qualifiers_uncertain():
    q = extract_qualifiers("כנראה תשפ\"ד")
    assert q.qualifier == EDTFQualifier.UNCERTAIN
    assert q.clean_text == "תשפ\"ד"

    q2 = extract_qualifiers("תשפ\"ד (?)")
    assert q2.qualifier == EDTFQualifier.UNCERTAIN
    assert q2.clean_text == "תשפ\"ד"


def test_extract_qualifiers_both():
    q = extract_qualifiers("בערך תשפ\"ד (?)")
    assert q.qualifier == EDTFQualifier.BOTH
    assert q.clean_text == "תשפ\"ד"


def test_extract_qualifiers_before():
    q = extract_qualifiers("לפני תשפ\"ד")
    assert q.interval_type == EDTFIntervalType.BEFORE
    assert q.clean_text == "תשפ\"ד"


def test_extract_qualifiers_after():
    q = extract_qualifiers("אחרי תשפ\"ד")
    assert q.interval_type == EDTFIntervalType.AFTER
    assert q.clean_text == "תשפ\"ד"

    q2 = extract_qualifiers("מ-תרפ\"ז ואילך")
    assert q2.interval_type == EDTFIntervalType.AFTER
    assert q2.clean_text == "תרפ\"ז"


def test_extract_qualifiers_between():
    q = extract_qualifiers("בין תשפ\"ג ל-תשפ\"ד")
    assert q.interval_type == EDTFIntervalType.RANGE
    assert q.clean_text == "תשפ\"ג"
    assert q.range_text2 == "תשפ\"ד"

    q2 = extract_qualifiers("מ-תרפ\"ז עד תשפ\"ד")
    assert q2.interval_type == EDTFIntervalType.RANGE
    assert q2.clean_text == "תרפ\"ז"
    assert q2.range_text2 == "תשפ\"ד"
