#!/usr/bin/env python3
"""Generate static redirect shims for legacy URLs reported by Search Console."""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE_URL = "https://southforkapps.com"
COLLECTION_PREFIX = "/South%20Fork%20Apps%20Collection"


REDIRECTS = {
    "2025/05/23/github.html": "/",
    "2025/04/26/welcome-to-south-fork-apps.html": "/",
    "2025/05/26/South Fork Apps Collection/typing-test/South Fork Apps Collection/url-decoder/index.html": f"{COLLECTION_PREFIX}/url-decoder/",
    "2025/05/23/South Fork Apps Collection/symbol-pad/South Fork Apps Collection/jwt-decoder/index.html": f"{COLLECTION_PREFIX}/jwt-decoder/",
    "2025/05/23/South Fork Apps Collection/json-formatter/South Fork Apps Collection/age-calculator/index.html": f"{COLLECTION_PREFIX}/age-calculator/",
    "2025/05/23/South Fork Apps Collection/text-repeater/South Fork Apps Collection/timestamp-converter/index.html": f"{COLLECTION_PREFIX}/timestamp-converter/",
    "2025/05/26/South Fork Apps Collection/tab-space-converter/index.html": f"{COLLECTION_PREFIX}/tab-space-converter/",
    "2025/05/23/South Fork Apps Collection/json-formatter/South Fork Apps Collection/url-encoder/index.html": f"{COLLECTION_PREFIX}/url-encoder/",
    "2025/05/23/South Fork Apps Collection/json-formatter/index.html": f"{COLLECTION_PREFIX}/json-formatter/",
    "2025/05/23/South Fork Apps Collection/word-frequency/South Fork Apps Collection/decision-spinner/index.html": f"{COLLECTION_PREFIX}/decision-spinner/",
    "2025/05/23/South Fork Apps Collection/word-frequency/South Fork Apps Collection/dog-poop-tracker/index.html": f"{COLLECTION_PREFIX}/dog-poop-tracker/",
    "2025/05/23/South Fork Apps Collection/word-frequency/South Fork Apps Collection/random-quote/index.html": f"{COLLECTION_PREFIX}/random-quote/",
    "2025/05/26/South Fork Apps Collection/text-case-converter/index.html": f"{COLLECTION_PREFIX}/text-case-converter/",
    "2025/05/23/South Fork Apps Collection/word-frequency/South Fork Apps Collection/meeting-cost-tracker/index.html": f"{COLLECTION_PREFIX}/meeting-cost-tracker/",
    "2025/05/23/South Fork Apps Collection/word-frequency/South Fork Apps Collection/symbol-pad/index.html": f"{COLLECTION_PREFIX}/symbol-pad/",
    "2025/05/23/South Fork Apps Collection/word-frequency/South Fork Apps Collection/cron-builder/index.html": f"{COLLECTION_PREFIX}/cron-builder/",
    "2025/05/23/South Fork Apps Collection/symbol-pad/South Fork Apps Collection/text-case-converter/index.html": f"{COLLECTION_PREFIX}/text-case-converter/",
    "2025/05/23/South Fork Apps Collection/symbol-pad/South Fork Apps Collection/smart-quotes-converter/index.html": f"{COLLECTION_PREFIX}/smart-quotes-converter/",
    "2025/05/26/South Fork Apps Collection/css-unit-converter/South Fork Apps Collection/bingo-maker/index.html": f"{COLLECTION_PREFIX}/bingo-maker/",
    "2025/05/26/South Fork Apps Collection/typing-test/South Fork Apps Collection/haiku-checker/index.html": f"{COLLECTION_PREFIX}/haiku-checker/",
    "2025/05/23/South Fork Apps Collection/text-repeater/South Fork Apps Collection/compound-interest/index.html": f"{COLLECTION_PREFIX}/compound-interest/",
    "2025/05/26/South Fork Apps Collection/life-stats/index.html": f"{COLLECTION_PREFIX}/life-stats/",
    "2025/05/26/South Fork Apps Collection/box-shadow-generator/index.html": f"{COLLECTION_PREFIX}/box-shadow-generator/",
}


def render_redirect(target_path: str) -> str:
    target_url = BASE_URL + target_path
    safe_target = escape(target_url, quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{safe_target}">
<meta http-equiv="refresh" content="0; url={safe_target}">
<title>Redirecting | South Fork Apps</title>
<script>window.location.replace({target_url!r});</script>
</head>
<body>
<p>This South Fork Apps URL has moved. <a href="{safe_target}">Continue to the current page</a>.</p>
</body>
</html>
"""


def main() -> None:
    for legacy_path, target_path in REDIRECTS.items():
        output_path = ROOT / legacy_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_redirect(target_path), encoding="utf-8")
        print(f"{legacy_path} -> {target_path}")


if __name__ == "__main__":
    main()
