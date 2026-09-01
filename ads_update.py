#!/usr/bin/env python3
"""Ensure the AdSense loader is present in the <head> of every monetizable page.

South Fork Apps carried the AdSense tag on the homepage only, so the 249 app
pages that Google actually sends search traffic to earned nothing. This script
sweeps every indexable page and injects the loader once, inside a marked block
so it can be re-run safely.

Deliberately skipped:
  * 404.html            - AdSense policy prohibits ads on error pages.
  * 2025/**             - legacy noindex redirect stubs, no content to monetize.
  * any noindex page    - same reason.

Run from the repo root:  python3 ads_update.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COLLECTION_DIR = ROOT / "South Fork Apps Collection"

PUBLISHER_ID = "ca-pub-3076043873825717"
MARKER = "SFA_ADS"

ADS_BLOCK = f"""
<!-- {MARKER}_START -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUBLISHER_ID}" crossorigin="anonymous"></script>
<!-- {MARKER}_END -->
""".strip()

SKIP_DIRS = {"2025"}
SKIP_FILES = {"404.html"}


def remove_marked_block(text: str, marker: str) -> str:
    pattern = re.compile(
        rf"\n?(?:<!--|/\*) {re.escape(marker)}_START(?: -->|\*/).*?(?:<!--|/\*) {re.escape(marker)}_END(?: -->|\*/)\n?",
        re.S,
    )
    return pattern.sub("\n", text)


def inject_ads_block(text: str) -> str:
    """Insert the loader once. Idempotent: an existing block is replaced, not doubled."""
    text = remove_marked_block(text, MARKER)

    # An unmarked publisher tag already on the page (the homepage) is left alone.
    if PUBLISHER_ID in text:
        return text

    social_end = "<!-- SFA_SOCIAL_END -->"
    if social_end in text:
        return text.replace(social_end, social_end + "\n" + ADS_BLOCK, 1)

    if "</head>" in text:
        return text.replace("</head>", ADS_BLOCK + "\n</head>", 1)

    return text


def monetizable_pages() -> list[Path]:
    pages: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts or rel.parts[0] in SKIP_DIRS:
            continue
        if path.name in SKIP_FILES or " 2." in path.name:
            continue
        pages.append(path)
    return pages


def main() -> None:
    added = skipped_present = skipped_noindex = failed = 0

    for path in monetizable_pages():
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")

        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', text, re.I):
            skipped_noindex += 1
            continue

        if PUBLISHER_ID in text and f"{MARKER}_START" not in text:
            skipped_present += 1
            continue

        updated = inject_ads_block(text)
        if PUBLISHER_ID not in updated:
            print(f"FAILED  {rel}: no </head> to inject into")
            failed += 1
            continue

        if updated != text:
            path.write_text(updated, encoding="utf-8")
            added += 1

    total = added + skipped_present + skipped_noindex + failed
    print(f"scanned {total} pages")
    print(f"  loader added:        {added}")
    print(f"  already had tag:     {skipped_present}")
    print(f"  skipped (noindex):   {skipped_noindex}")
    print(f"  failed:              {failed}")


if __name__ == "__main__":
    main()
