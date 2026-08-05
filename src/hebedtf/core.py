"""Core conversion functions for hebEDTF."""

from datetime import timedelta

from pyluach import dates

from hebedtf.months import get_hebrew_month_number
from hebedtf.parser import parse_hebrew_date_text
from hebedtf.qualifiers import EDTFIntervalType, extract_qualifiers


def _base_hebrew_to_edtf_tuple(text: str) -> tuple[str, str, str]:
    """Helper returning (single_or_interval_edtf, start_iso, end_iso)."""
    components = parse_hebrew_date_text(text)

    if components.day is not None and components.month_str is not None:
        month_num = get_hebrew_month_number(components.month_str, components.year)
        heb_d = dates.HebrewDate(components.year, month_num, components.day)
        greg_date = heb_d.to_greg().to_pydate()
        iso = greg_date.isoformat()
        return (iso, iso, iso)

    elif components.month_str is not None:
        month_num = get_hebrew_month_number(components.month_str, components.year)
        start_d = dates.HebrewDate(components.year, month_num, 1).to_greg().to_pydate()
        month_len = dates.utils._month_length(components.year, month_num)
        end_d = dates.HebrewDate(
            components.year, month_num, month_len
        ).to_greg().to_pydate()
        start_iso = start_d.isoformat()
        end_iso = end_d.isoformat()
        return (f"{start_iso}/{end_iso}", start_iso, end_iso)

    else:
        start_d = dates.HebrewDate(components.year, 7, 1).to_greg().to_pydate()
        next_tishrei = dates.HebrewDate(components.year + 1, 7, 1).to_greg().to_pydate()
        end_d = next_tishrei - timedelta(days=1)
        start_iso = start_d.isoformat()
        end_iso = end_d.isoformat()
        return (f"{start_iso}/{end_iso}", start_iso, end_iso)


def hebrew_to_edtf(text: str) -> str:
    """Convert a Hebrew date string or expression into an EDTF Level 0/1 string.

    Supports:
        - Exact dates, month intervals, year intervals
        - Uncertainty ('?', "כנראה", "ספק") -> '?'
        - Approximation ('~', "בערך", "סביבות", "משוער", "כ-") -> '~'
        - Open intervals ("לפני", "אחרי", "ואילך") -> '../YYYY-MM-DD' or 'YYYY-MM-DD/..'
        - Bounded ranges ("בין X ל-Y", "מ-X עד Y") -> 'START_X/END_Y'
    """
    ext = extract_qualifiers(text)
    qual_suffix = ext.qualifier.value

    # Case 1: Bounded Range ("בין X ל-Y" or "מ-X עד Y")
    if ext.interval_type == EDTFIntervalType.RANGE and ext.range_text2:
        _, start1, _ = _base_hebrew_to_edtf_tuple(ext.clean_text)
        _, _, end2 = _base_hebrew_to_edtf_tuple(ext.range_text2)
        return f"{start1}/{end2}{qual_suffix}"

    # Case 2: Open Start ("לפני X", "טרום X")
    if ext.interval_type == EDTFIntervalType.BEFORE:
        _, start_iso, _ = _base_hebrew_to_edtf_tuple(ext.clean_text)
        return f"../{start_iso}{qual_suffix}"

    # Case 3: Open End ("אחרי X", "מ-X ואילך")
    if ext.interval_type == EDTFIntervalType.AFTER:
        _, _, end_iso = _base_hebrew_to_edtf_tuple(ext.clean_text)
        return f"{end_iso}/..{qual_suffix}"

    # Case 4: Standard Date / Month / Year
    base_edtf, _, _ = _base_hebrew_to_edtf_tuple(ext.clean_text)
    return f"{base_edtf}{qual_suffix}"
