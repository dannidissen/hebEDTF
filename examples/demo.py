"""hebEDTF Demo script - Batch conversion of Hebrew date expressions."""

import sys
from hebedtf import hebrew_to_edtf

# Force utf-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

catalog_samples = [
    'א\' בתשרי תשפ"ד',
    'תשפ"ד',
    'בערך תש"ח',
    'כנראה ה\' באייר תש"ח',
    'לפני תש"ח',
    'בין תר"ס ל-תש"ח',
    'י"ד באדר ב\' תשפ"ד',
]


def main():
    print("===================================================")
    print(" hebEDTF Batch Conversion Demo")
    print("===================================================\n")
    for sample in catalog_samples:
        edtf_out = hebrew_to_edtf(sample)
        print(f"  {sample:<25} ==>  {edtf_out}")
    print("\n===================================================")


if __name__ == "__main__":
    main()
