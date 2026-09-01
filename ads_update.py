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
COLLECTION_DIR = ROOT / "tools"

PUBLISHER_ID = "ca-pub-3076043873825717"
MARKER = "SFA_ADS"

ADS_BLOCK = f"""
<!-- {MARKER}_START -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUBLISHER_ID}" crossorigin="anonymous"></script>
<!-- {MARKER}_END -->
""".strip()

SKIP_DIRS = {"2025"}
SKIP_FILES = {"404.html"}

# AdSense's inventory value policy prohibits ads on screens with low-value
# content. A page thinner than this carries no loader, and an existing block is
# stripped, so a navigational index or a stub can never quietly start serving.
MIN_WORDS_FOR_ADS = 250


def visible_words(text: str) -> int:
    body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", text)
    return len(re.sub(r"(?s)<[^>]+>", " ", body).split())


def remove_marked_block(text: str, marker: str) -> str:
    pattern = re.compile(
        rf"\n?(?:<!--|/\*)\s*{re.escape(marker)}_START\s*(?:-->|\*/).*?(?:<!--|/\*)\s*{re.escape(marker)}_END\s*(?:-->|\*/)\n?",
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
    added = already_ok = skipped_present = skipped_noindex = skipped_thin = failed = 0

    for path in monetizable_pages():
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")

        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', text, re.I):
            skipped_noindex += 1
            continue

        if visible_words(text) < MIN_WORDS_FOR_ADS:
            stripped = remove_marked_block(text, MARKER)
            if stripped != text:
                path.write_text(stripped, encoding="utf-8")
                print(f"REMOVED {rel}: {visible_words(text)} words, under the {MIN_WORDS_FOR_ADS} word floor")
            skipped_thin += 1
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
        else:
            already_ok += 1

    total = added + already_ok + skipped_present + skipped_noindex + skipped_thin + failed
    print(f"scanned {total} pages")
    print(f"  loader added:        {added}")
    print(f"  already correct:     {already_ok}")
    print(f"  pre-existing tag:    {skipped_present}")
    print(f"  skipped (noindex):   {skipped_noindex}")
    print(f"  skipped (too thin):  {skipped_thin}")
    print(f"  failed:              {failed}")


if __name__ == "__main__":
    main()
