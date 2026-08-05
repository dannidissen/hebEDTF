"""Core conversion functions for hebEDTF."""

from datetime import timedelta

from pyluach import dates

from hebedtf.months import get_hebrew_month_number
from hebedtf.parser import parse_hebrew_date_text


def hebrew_to_edtf(text: str) -> str:
    """Convert a Hebrew date string or year/month expression to EDTF format.

    Args:
        text: Hebrew date expression (e.g. "א' תשרי תשפ\"ד", "תשפ\"ד")

    Returns:
        EDTF formatted string (e.g. "2023-09-16", "2023-09-16/2024-10-02")
    """
    components = parse_hebrew_date_text(text)

    if components.day is not None and components.month_str is not None:
        month_num = get_hebrew_month_number(components.month_str, components.year)
        heb_d = dates.HebrewDate(components.year, month_num, components.day)
        greg_date = heb_d.to_greg().to_pydate()
        return greg_date.isoformat()

    elif components.month_str is not None:
        month_num = get_hebrew_month_number(components.month_str, components.year)
        start_d = dates.HebrewDate(components.year, month_num, 1).to_greg().to_pydate()
        month_len = dates.utils._month_length(components.year, month_num)
        end_d = dates.HebrewDate(
            components.year, month_num, month_len
        ).to_greg().to_pydate()
        return f"{start_d.isoformat()}/{end_d.isoformat()}"

    else:
        start_d = dates.HebrewDate(components.year, 7, 1).to_greg().to_pydate()
        next_tishrei = dates.HebrewDate(components.year + 1, 7, 1).to_greg().to_pydate()
        end_d = next_tishrei - timedelta(days=1)
        return f"{start_d.isoformat()}/{end_d.isoformat()}"
