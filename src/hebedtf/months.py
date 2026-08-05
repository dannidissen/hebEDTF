"""Hebrew Month normalization and mapping for hebEDTF."""

from pyluach import dates

MONTH_ALIASES = {
    'תשרי': 'TISHREI',
    'חשוון': 'CHESVAN',
    'חשון': 'CHESVAN',
    'מרחשוון': 'CHESVAN',
    'מרחשון': 'CHESVAN',
    'כסלו': 'KISLEV',
    'כסליו': 'KISLEV',
    'טבת': 'TEVET',
    'שבט': 'SHEVAT',
    'אדר': 'ADAR',
    'אדר א': 'ADAR_1',
    'אדר א\'': 'ADAR_1',
    'אדר א׳': 'ADAR_1',
    'אדר ראשון': 'ADAR_1',
    'אדר ב': 'ADAR_2',
    'אדר ב\'': 'ADAR_2',
    'אדר ב׳': 'ADAR_2',
    'אדר שני': 'ADAR_2',
    'ניסן': 'NISAN',
    'אייר': 'IYAR',
    'איר': 'IYAR',
    'סיוון': 'SIVAN',
    'סיון': 'SIVAN',
    'תמוז': 'TAMMUZ',
    'אב': 'AV',
    'מנחם אב': 'AV',
    'אלול': 'ELUL',
}


def normalize_month_name(month_text: str) -> str:
    """Normalize Hebrew month text into standard key."""
    cleaned = month_text.strip()
    if cleaned in MONTH_ALIASES:
        return MONTH_ALIASES[cleaned]

    if cleaned.startswith('ב') and cleaned[1:] in MONTH_ALIASES:
        return MONTH_ALIASES[cleaned[1:]]

    raise ValueError(f"Unknown Hebrew month name: '{month_text}'")


def get_hebrew_month_number(month_text: str, year: int) -> int:
    """Map Hebrew month name and year to pyluach month index (1-12 or 1-13)."""
    key = normalize_month_name(month_text)
    is_leap_year = dates.utils._is_leap(year)

    if key == 'NISAN':
        return 1
    elif key == 'IYAR':
        return 2
    elif key == 'SIVAN':
        return 3
    elif key == 'TAMMUZ':
        return 4
    elif key == 'AV':
        return 5
    elif key == 'ELUL':
        return 6
    elif key == 'TISHREI':
        return 7
    elif key == 'CHESVAN':
        return 8
    elif key == 'KISLEV':
        return 9
    elif key == 'TEVET':
        return 10
    elif key == 'SHEVAT':
        return 11
    elif key == 'ADAR':
        return 12
    elif key == 'ADAR_1':
        return 12
    elif key == 'ADAR_2':
        if not is_leap_year:
            raise ValueError(f"Adar II specified for non-leap year {year}")
        return 13
    else:
        raise ValueError(f"Unrecognized month key: {key}")
