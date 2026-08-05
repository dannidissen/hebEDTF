"""Command Line Interface (CLI) for hebEDTF."""

import argparse
import json
import sys
from typing import List, Optional

from hebedtf import __version__, hebrew_to_edtf


def main(args: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="hebedtf",
        description="Convert Hebrew date expressions to EDTF.",
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Hebrew date text (e.g. 'כ\"ג בתשרי תשפ\"ד', 'בערך תש\"ח')",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON containing input text and EDTF string.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parsed_args = parser.parse_args(args)
    input_text = parsed_args.text

    if not input_text:
        try:
            if not sys.stdin.isatty():
                input_text = sys.stdin.read().strip()
        except (OSError, AttributeError):
            input_text = None

    if not input_text:
        parser.print_help()
        return 1

    try:
        edtf_result = hebrew_to_edtf(input_text)
        if parsed_args.json:
            out = json.dumps(
                {"input": input_text, "edtf": edtf_result},
                ensure_ascii=False,
                indent=2,
            )
            print(out)
        else:
            print(edtf_result)
        return 0
    except Exception as err:
        if parsed_args.json:
            out = json.dumps(
                {"input": input_text, "error": str(err)},
                ensure_ascii=False,
                indent=2,
            )
            print(out, file=sys.stderr)
        else:
            print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
