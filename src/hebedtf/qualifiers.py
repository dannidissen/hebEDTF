"""Qualifier and interval classification for hebEDTF."""

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class EDTFQualifier(Enum):
    NONE = ""
    APPROXIMATE = "~"
    UNCERTAIN = "?"
    BOTH = "%"


class EDTFIntervalType(Enum):
    NONE = auto()
    BEFORE = auto()  # Open start (e.g. ../2023)
    AFTER = auto()   # Open end (e.g. 2023/..)
    RANGE = auto()   # Bounded range (e.g. 2020/2023)


@dataclass
class ExtractedQualifiers:
    qualifier: EDTFQualifier
    interval_type: EDTFIntervalType
    clean_text: str
    range_text2: Optional[str] = None


BETWEEN_RE = re.compile(
    r"^(?:בין)\s+(.+?)\s+(?:ל-|ל\s+)(.+)$", re.IGNORECASE
)
FROM_TO_RE = re.compile(
    r"^(?:מ-|מ\s+)(.+?)\s+(?:עד|עד-)\s+(.+)$", re.IGNORECASE
)


def _combine_qualifiers(
    q1: ExtractedQualifiers, q2: ExtractedQualifiers
) -> EDTFQualifier:
    """Helper to combine qualifiers of two range endpoints."""
    if q1.qualifier == EDTFQualifier.BOTH or q2.qualifier == EDTFQualifier.BOTH:
        return EDTFQualifier.BOTH
    approx1 = q1.qualifier == EDTFQualifier.APPROXIMATE
    approx2 = q2.qualifier == EDTFQualifier.APPROXIMATE
    unc1 = q1.qualifier == EDTFQualifier.UNCERTAIN
    unc2 = q2.qualifier == EDTFQualifier.UNCERTAIN
    if (approx1 and unc2) or (unc1 and approx2):
        return EDTFQualifier.BOTH
    if q1.qualifier != EDTFQualifier.NONE:
        return q1.qualifier
    if q2.qualifier != EDTFQualifier.NONE:
        return q2.qualifier
    return EDTFQualifier.NONE


def extract_qualifiers(text: str) -> ExtractedQualifiers:
    """Analyze Hebrew text for uncertainty, approximation, open intervals, or ranges."""
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    raw = text.strip()

    between_match = BETWEEN_RE.match(raw)
    if between_match:
        part1 = between_match.group(1).strip()
        part2 = between_match.group(2).strip()
        q1 = extract_qualifiers(part1)
        q2 = extract_qualifiers(part2)
        final_q = _combine_qualifiers(q1, q2)
        return ExtractedQualifiers(
            qualifier=final_q,
            interval_type=EDTFIntervalType.RANGE,
            clean_text=q1.clean_text,
            range_text2=q2.clean_text,
        )

    from_to_match = FROM_TO_RE.match(raw)
    if from_to_match:
        part1 = from_to_match.group(1).strip()
        part2 = from_to_match.group(2).strip()
        q1 = extract_qualifiers(part1)
        q2 = extract_qualifiers(part2)
        final_q = _combine_qualifiers(q1, q2)
        return ExtractedQualifiers(
            qualifier=final_q,
            interval_type=EDTFIntervalType.RANGE,
            clean_text=q1.clean_text,
            range_text2=q2.clean_text,
        )

    interval_type = EDTFIntervalType.NONE
    clean = raw

    before_prefixes = ["לפני", "טרום", "קודם ל-", "קודם ל"]
    for prefix in before_prefixes:
        if clean.startswith(prefix + " ") or clean == prefix:
            interval_type = EDTFIntervalType.BEFORE
            clean = clean[len(prefix):].strip()
            break

    after_prefixes = ["אחרי", "לאחר"]
    for prefix in after_prefixes:
        if clean.startswith(prefix + " "):
            interval_type = EDTFIntervalType.AFTER
            clean = clean[len(prefix):].strip()
            break

    if clean.endswith(" ואילך") or clean.endswith(" ואילך."):
        interval_type = EDTFIntervalType.AFTER
        clean = re.sub(r"\s+ואילך\.?$", "", clean).strip()

    if clean.startswith("מ-"):
        clean = clean[2:].strip()

    is_approx = False
    is_uncertain = False

    if "?" in clean or "(?)" in clean:
        is_uncertain = True
        clean = clean.replace("(?)", "").replace("?", "").strip()

    if "~" in clean:
        is_approx = True
        clean = clean.replace("~", "").strip()

    approx_keywords = ["בערך", "סביבות", "סביב", "משוער", "קירוב"]
    for kw in approx_keywords:
        if (
            kw in clean.split()
            or clean.startswith(kw + " ")
            or clean.endswith(" " + kw)
        ):
            is_approx = True
            clean = re.sub(r"\b" + re.escape(kw) + r"\b", "", clean).strip()

    if re.match(r"^כ-[תשראקבגדהוזחטיכלמנסעפצק]", clean):
        is_approx = True
        clean = clean[2:].strip()

    uncertain_keywords = ["כנראה", "ספק", "אולי", "אפשר"]
    for kw in uncertain_keywords:
        if (
            kw in clean.split()
            or clean.startswith(kw + " ")
            or clean.endswith(" " + kw)
        ):
            is_uncertain = True
            clean = re.sub(r"\b" + re.escape(kw) + r"\b", "", clean).strip()

    if is_approx and is_uncertain:
        qualifier = EDTFQualifier.BOTH
    elif is_approx:
        qualifier = EDTFQualifier.APPROXIMATE
    elif is_uncertain:
        qualifier = EDTFQualifier.UNCERTAIN
    else:
        qualifier = EDTFQualifier.NONE

    clean = re.sub(r"\s+", " ", clean).strip()

    return ExtractedQualifiers(
        qualifier=qualifier,
        interval_type=interval_type,
        clean_text=clean,
    )
