"""Hebrew date text parser for hebEDTF."""

from dataclasses import dataclass
from typing import Optional

from hebedtf.gematria import parse_hebrew_day, parse_hebrew_year
from hebedtf.months import MONTH_ALIASES


@dataclass
class HebrewDateComponents:
    """Structured components extracted from a Hebrew date text."""
    day: Optional[int]
    month_str: Optional[str]
    year: int


def _is_month_match(token: str) -> bool:
    """Check if token matches a known Hebrew month name or alias."""
    clean = token.strip()
    if clean in MONTH_ALIASES:
        return True
    if clean.startswith('ב') and clean[1:] in MONTH_ALIASES:
        return True
    return False


def parse_hebrew_date_text(text: str) -> HebrewDateComponents:
    """Parse Hebrew date string into HebrewDateComponents."""
    if not text or not text.strip():
        raise ValueError("Date string cannot be empty")

    cleaned = text.strip()

    for noise in ["בשנת", "שנת", "בחודש", "חודש"]:
        if cleaned.startswith(noise + " "):
            cleaned = cleaned[len(noise) + 1:].strip()

    tokens = cleaned.split()

    if len(tokens) == 1:
        year = parse_hebrew_year(tokens[0])
        return HebrewDateComponents(day=None, month_str=None, year=year)

    try:
        possible_year = parse_hebrew_year(tokens[-1])
    except ValueError:
        raise ValueError(f"Could not parse year from '{text}'")

    middle_tokens = tokens[:-1]

    if not middle_tokens:
        return HebrewDateComponents(day=None, month_str=None, year=possible_year)

    month_candidate = " ".join(middle_tokens)
    if _is_month_match(month_candidate):
        return HebrewDateComponents(
            day=None, month_str=month_candidate, year=possible_year
        )

    day_token = middle_tokens[0]
    try:
        day_val = parse_hebrew_day(day_token)
        month_candidate = " ".join(middle_tokens[1:])
        if _is_month_match(month_candidate):
            return HebrewDateComponents(
                day=day_val, month_str=month_candidate, year=possible_year
            )
    except ValueError:
        pass

    if len(middle_tokens) >= 2:
        try:
            day_val = parse_hebrew_day(middle_tokens[0])
            month_cand = " ".join(middle_tokens[1:])
            if _is_month_match(month_cand):
                return HebrewDateComponents(
                    day=day_val, month_str=month_cand, year=possible_year
                )
        except ValueError:
            pass

    raise ValueError(f"Unable to parse Hebrew date string: '{text}'")
