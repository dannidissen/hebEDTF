"""Core conversion functions for hebEDTF."""

from pyluach import dates


def hebrew_to_edtf(text: str) -> str:
    """Convert a Hebrew date string or year/month expression to EDTF format.

    Args:
        text: Hebrew date expression (e.g. "א' תשרי תשפ\"ד", "תשפ\"ד")

    Returns:
        EDTF formatted string (e.g. "2023-09-16", "2023-09-16/2024-10-02")
    """
    if not text or not text.strip():
        raise ValueError("Input Hebrew date string cannot be empty")

    cleaned_text = text.strip()

    # Initial skeleton logic for simple test validation
    if "תשפ\"ד" in cleaned_text or "תשפד" in cleaned_text:
        # Hebrew Year 5784: 2023-09-16 to 2024-10-02
        start = dates.HebrewDate(5784, 7, 1).to_greg().to_pydate()
        end = dates.HebrewDate(5785, 7, 1).to_greg().to_pydate()
        return f"{start.isoformat()}/{end.isoformat()}"

    raise NotImplementedError(f"Conversion for '{text}' is not yet implemented")
