#!/usr/bin/env python3
"""Build a self-contained branded edition of the break-even calculator."""

import argparse
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def replace_one(page, pattern, replacement):
    page, count = re.subn(pattern, lambda _: replacement, page, flags=re.S)
    if count != 1:
        raise ValueError(f"Expected one match for {pattern}, found {count}")
    return page


def build(name, accent):
    page = (ROOT / "embed/break-even-calculator/index.html").read_text(encoding="utf-8")
    name = html.escape(name)
    page = replace_one(page, r"<title>[^<]+</title>", f"<title>{name} | Break-Even Calculator</title>")
    page = replace_one(page, r'<link rel="canonical"[^>]+>\s*', "")
    page = replace_one(page, r'<link href="https://fonts\.googleapis\.com/[^>]+>\s*', "")
    page = replace_one(page, r'<span class="eyebrow">[^<]+</span>', f'<span class="eyebrow">{name}</span>')
    page = replace_one(page, r"--accent: #[\da-fA-F]{6};", f"--accent: {accent};")
    page = replace_one(page, r'<div class="sfa-embed-credit">.*?</div>\s*', "")
    page = replace_one(page, r"<script>var SFA_SLUG.*?</script>\s*<script>.*?</script>", "")
    return page


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument("--accent", default="#7ddb84")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    name = args.name.strip()
    if not 1 <= len(name) <= 80:
        parser.error("Name must contain 1 to 80 characters.")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", args.accent):
        parser.error("Accent must be a six-digit hex color.")
    args.output.write_text(build(name, args.accent), encoding="utf-8")


if __name__ == "__main__":
    main()
