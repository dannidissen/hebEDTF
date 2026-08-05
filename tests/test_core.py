"""Comprehensive tests for hebEDTF core module and EDTF spec compliance."""

import edtf
import pytest

from hebedtf import hebrew_to_edtf


def check_valid_edtf(edtf_str: str) -> bool:
    """Helper to validate generated string using python-edtf library."""
    res = edtf.parse_edtf(edtf_str)
    return res is not None


# --- 1. Full Date Tests ---

@pytest.mark.parametrize("hebrew_input, expected_edtf", [
    ("א' תשרי תשפ\"ד", "2023-09-16"),
    ("א' בתשרי תשפ\"ד", "2023-09-16"),
    ("י' בתשרי תשפ\"ד", "2023-09-25"),  # Yom Kippur
    ("כ\"ה בכסלו תשפ\"ד", "2023-12-08"),  # Hanukkah
    ("ט\"ו בניסן תשפ\"ד", "2024-04-23"),  # Passover
    ("א' ניסן ה'תשפ\"ד", "2024-04-09"),
    ("ט\"ו באב תרפ\"ז", "1927-08-13"),
    ("כ\"ג בתשרי תרפ\"ז", "1926-10-01"),
    ("א' תשרי תשפ\"ה", "2024-10-03"),
    ("כ\"ט אלול תשפ\"ד", "2024-10-02"),
    ("א' חשוון תשפ\"ד", "2023-10-16"),
    ("א' מרחשון תשפ\"ד", "2023-10-16"),
    ("א' כסליו תשפ\"ד", "2023-11-14"),
    ("א' טבת תשפ\"ד", "2023-12-13"),
    ("א' שבט תשפ\"ד", "2024-01-11"),
    ("א' תמוז תשפ\"ד", "2024-07-07"),
    ("א' אב תשפ\"ד", "2024-08-05"),
    ("א' מנחם אב תשפ\"ד", "2024-08-05"),
    ("א' אלול תשפ\"ד", "2024-09-04"),
    ("י\"ד באדר תשפ\"ג", "2023-03-07"),  # Purim 5783 (non-leap)
    ("י\"ד באדר א' תשפ\"ד", "2024-02-23"),  # Purim Katan 5784 (leap)
    ("י\"ד באדר ב' תשפ\"ד", "2024-03-24"),  # Purim 5784 (leap)
    ("י\"ד אדר שני תשפ\"ד", "2024-03-24"),
    ("י\"ד אדר ראשון תשפ\"ד", "2024-02-23"),
])
def test_full_dates(hebrew_input, expected_edtf):
    res = hebrew_to_edtf(hebrew_input)
    assert res == expected_edtf
    assert check_valid_edtf(res)


# --- 2. Month + Year Interval Tests ---

@pytest.mark.parametrize("hebrew_input, expected_edtf", [
    ("תשרי תשפ\"ד", "2023-09-16/2023-10-15"),
    ("חודש תשרי תשפ\"ד", "2023-09-16/2023-10-15"),
    ("בחודש תשרי תשפ\"ד", "2023-09-16/2023-10-15"),
    ("חשוון תשפ\"ד", "2023-10-16/2023-11-13"),
    ("ניסן תשפ\"ד", "2024-04-09/2024-05-08"),
    ("אלול תשפ\"ד", "2024-09-04/2024-10-02"),
    ("אדר א' תשפ\"ד", "2024-02-10/2024-03-10"),
    ("אדר ב' תשפ\"ד", "2024-03-11/2024-04-08"),
    ("אדר תשפ\"ג", "2023-02-22/2023-03-22"),
])
def test_month_intervals(hebrew_input, expected_edtf):
    res = hebrew_to_edtf(hebrew_input)
    assert res == expected_edtf
    assert check_valid_edtf(res)


# --- 3. Year Only Interval Tests ---

@pytest.mark.parametrize("hebrew_input, expected_edtf", [
    ("תשפ\"ד", "2023-09-16/2024-10-02"),
    ("שנת תשפ\"ד", "2023-09-16/2024-10-02"),
    ("בשנת תשפ\"ד", "2023-09-16/2024-10-02"),
    ("ה'תשפ\"ד", "2023-09-16/2024-10-02"),
    ("תרפ\"ז", "1926-09-09/1927-09-26"),
    ("ה'תרפ\"ז", "1926-09-09/1927-09-26"),
    ("תשפ\"ג", "2022-09-26/2023-09-15"),
    ("תשפ\"ה", "2024-10-03/2025-09-22"),
])
def test_year_intervals(hebrew_input, expected_edtf):
    res = hebrew_to_edtf(hebrew_input)
    assert res == expected_edtf
    assert check_valid_edtf(res)


# --- 4. Edge Cases & Error Handling ---

def test_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        hebrew_to_edtf("")


def test_invalid_hebrew_text_raises_value_error():
    with pytest.raises(ValueError):
        hebrew_to_edtf("Invalid text 123")


def test_adar_2_in_non_leap_year_raises_value_error():
    with pytest.raises(ValueError):
        hebrew_to_edtf("אדר ב' תשפ\"ג")  # 5783 is not leap
