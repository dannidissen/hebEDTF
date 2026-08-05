# hebEDTF

[![CI](https://github.com/dannidissen/hebEDTF/actions/workflows/ci.yml/badge.svg)](https://github.com/dannidissen/hebEDTF/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

**hebEDTF** is a Python library for parsing Hebrew date expressions and converting them into standard **Extended Date/Time Format (EDTF)** Level 0 and Level 1 strings.

It bridges the gap between natural Hebrew calendar phrases (exact dates, months, year ranges, uncertainty, and open intervals) and ISO/EDTF metadata specifications used in digital humanities, library records, and museum archives.

---

## 🚀 Features

- **Hebrew Date Parsing:** Converts exact Hebrew dates into EDTF ISO-compliant date strings (`YYYY-MM-DD`).
- **Year & Month Intervals:** Maps Hebrew years (e.g., `תשפ"ד`) and Hebrew months to exact Gregorian intervals (`YYYY-MM-DD/YYYY-MM-DD`).
- **Uncertainty & Approximation Qualifiers:** Translates Hebrew qualifiers (`בערך`, `סביב`, `משוער`, `כ-`, `כנראה`, `ספק`, `?`) into EDTF Level 1 indicators (`~`, `?`, `%`).
- **Open & Bounded Intervals:** Supports open-ended dates (`לפני`, `אחרי`, `ואילך`) and date ranges (`בין ... ל-...`, `מ-... עד ...`).
- **Validated Against Real Catalog Data:** Tested against a corpus of **110+ real-world Hebrew date expressions** from auction catalogs and library records (National Library of Israel, Kedem, Kestenbaum, BidSpirit). Every generated output is strictly validated against `python-edtf`.

---

## 📦 Installation

Install directly via `pip`:

```bash
pip install git+https://github.com/dannidissen/hebEDTF.git
```

Or for development:

```bash
git clone https://github.com/dannidissen/hebEDTF.git
cd hebEDTF
pip install -e .[dev]
```

---

## 💡 Quickstart Example

```python
from hebedtf import hebrew_to_edtf

# 1. Exact Date
print(hebrew_to_edtf('א\' בתשרי תשפ"ד'))
# Output: "2023-09-16"

# 2. Hebrew Year Interval
print(hebrew_to_edtf('תשפ"ד'))
# Output: "2023-09-16/2024-10-02"

# 3. Approximate & Uncertain Date Expressions
print(hebrew_to_edtf('בערך תשפ"ד'))
# Output: "2023-09-16/2024-10-02~"

print(hebrew_to_edtf('כנראה ה\' באייר תש"ח'))
# Output: "1948-05-14?"

# 4. Open & Bounded Ranges
print(hebrew_to_edtf('לפני תש"ח'))
# Output: "../1947-09-15"

print(hebrew_to_edtf('בין תר"ס ל-תש"ח'))
# Output: "1899-09-05/1948-10-03"
```

---

## 🧪 Running Tests

```bash
pytest
ruff check .
```

---

## 📜 License

Distributed under the terms of the [MIT License](LICENSE). Copyright (c) 2026 Danni Dissen.
