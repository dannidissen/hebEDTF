# hebEDTF

[![CI](https://github.com/dannidissen/hebEDTF/actions/workflows/ci.yml/badge.svg)](https://github.com/dannidissen/hebEDTF/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

**hebEDTF** is a Python library for converting Hebrew dates, month names, and year expressions into **Extended Date/Time Format (EDTF)** Level 0 and Level 1 strings.

It bridges the gap between Hebrew calendar expressions (including Hebrew years, months, and uncertainty markers) and standard metadata date formats widely used in archives, libraries, and digital humanities.

---

## 🚀 Features

- **Hebrew Date Parsing:** Convert exact Hebrew dates into EDTF ISO-compliant date strings (`YYYY-MM-DD`).
- **Year & Month Intervals:** Map Hebrew years (e.g. `תשפ"ד`) and Hebrew months to Gregorian intervals (`YYYY-MM-DD/YYYY-MM-DD`).
- **Uncertainty & Approximation:** Translate Hebrew qualifiers (e.g., "בערך", "סביב", "כנראה") into EDTF indicators (`~`, `?`, `%`).
- **Pure Python:** Built on top of [`pyluach`](https://github.com/simlist/pyluach) for fast and accurate Hebrew calendar math.

---

## 📦 Installation

Install the package directly via `pip`:

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

# Convert a Hebrew year to an EDTF Gregorian interval
edtf_range = hebrew_to_edtf('תשפ"ד')
print(edtf_range)
# Output: "2023-09-16/2024-10-02"
```

---

## 🧪 Running Tests

To run the test suite and code linter locally:

```bash
pytest
ruff check .
```

---

## 📜 License

Distributed under the terms of the [MIT License](LICENSE). Copyright (c) 2026 Danni Dissen.
