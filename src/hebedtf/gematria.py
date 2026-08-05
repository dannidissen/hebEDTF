"""Hebrew Gematria utilities for hebEDTF."""

import re

# Letter values mapping
GEMATRIA_MAP = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90,
    'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
}

# Quotes and punctuation characters to clean
QUOTES_REGEX = re.compile(r"['\"״׳`]")


def clean_hebrew_text(text: str) -> str:
    """Remove quotes, gershayim, and extra whitespace from Hebrew string."""
    if not text:
        return ""
    return QUOTES_REGEX.sub("", text).strip()


def parse_gematria(text: str) -> int:
    """Convert a simple Hebrew gematria string into its integer value."""
    cleaned = clean_hebrew_text(text)
    if not cleaned:
        raise ValueError("Empty gematria string")

    total = 0
    for char in cleaned:
        if char in GEMATRIA_MAP:
            total += GEMATRIA_MAP[char]
        else:
            raise ValueError(
                f"Invalid Hebrew character '{char}' in gematria string '{text}'"
            )

    return total


def parse_hebrew_day(text: str) -> int:
    """Parse a Hebrew day representation (1-30)."""
    val = parse_gematria(text)
    if not (1 <= val <= 30):
        raise ValueError(
            f"Hebrew day value '{val}' derived from '{text}' is out of range 1-30"
        )
    return val


def parse_hebrew_year(text: str) -> int:
    """Parse a Hebrew year string into full 4-digit Hebrew year (e.g. 5784)."""
    raw_cleaned = text.strip()
    if not raw_cleaned:
        raise ValueError("Empty Hebrew year string")

    has_thousands_prefix = False
    thousands_val = 5000

    prefix_tuple = ("ה'", "ה׳", 'ה"', "ה״")
    if raw_cleaned.startswith(prefix_tuple):
        has_thousands_prefix = True
        year_letters = raw_cleaned[2:]
    elif (
        len(raw_cleaned) >= 4
        and raw_cleaned.startswith("ה")
        and raw_cleaned[1] in ('ת', 'ש', 'ר', 'ק')
    ):
        has_thousands_prefix = True
        year_letters = raw_cleaned[1:]
    else:
        year_letters = raw_cleaned

    remainder_val = parse_gematria(year_letters)

    if has_thousands_prefix:
        return thousands_val + remainder_val
    else:
        if remainder_val < 1000:
            return 5000 + remainder_val
        return remainder_val
