#!/usr/bin/env python3
"""Pull the real, checkable facts out of each tool's own source.

Content written from these facts describes what the tool actually does.
Content written without them is filler, which is what got the site flagged.
"""
from __future__ import annotations

import json, re, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOLS = ROOT / "tools"
MARKED = re.compile(r"(?s)<!-- SFA_(FEATURE|RELATED|JSONLD|BREADCRUMB|SOCIAL|ADS|DISCOVERY)_START.*?SFA_\1_END -->")


def strip(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def facts(p: Path) -> dict:
    raw = p.read_text(encoding="utf-8", errors="replace")
    body = MARKED.sub(" ", raw)                      # ignore injected blocks
    scripts = "\n".join(re.findall(r"(?is)<script(?![^>]*ld\+json)[^>]*>(.*?)</script>", body))
    markup = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", body)

    inputs = []
    for m in re.finditer(r"<input\b([^>]*)>", markup, re.I):
        a = m.group(1)
        g = lambda k: (re.search(rf'{k}="([^"]*)"', a, re.I) or [None, None])[1]
        if (g("type") or "text").lower() in {"hidden", "submit"}:
            continue
        inputs.append({k: v for k, v in {
            "id": g("id"), "type": g("type") or "text", "placeholder": g("placeholder"),
            "min": g("min"), "max": g("max"), "step": g("step"), "value": g("value"),
        }.items() if v})

    selects = []
    for m in re.finditer(r"(?is)<select\b([^>]*)>(.*?)</select>", markup):
        opts = [strip(o) for o in re.findall(r"(?is)<option[^>]*>(.*?)</option>", m.group(2))]
        sid = (re.search(r'id="([^"]*)"', m.group(1), re.I) or [None, None])[1]
        selects.append({"id": sid, "options": [o for o in opts if o][:14]})

    labels = [strip(x) for x in re.findall(r"(?is)<label[^>]*>(.*?)</label>", markup)]
    buttons = [strip(x) for x in re.findall(r"(?is)<button[^>]*>(.*?)</button>", markup)]
    heads = [strip(x) for x in re.findall(r"(?is)<h[2-4][^>]*>(.*?)</h[2-4]>", markup)]

    # numeric constants and named formulas the script actually implements
    consts = re.findall(r"(?m)^\s*(?:const|let|var)\s+([A-Z_][A-Z0-9_]{2,})\s*=\s*([^;\n]{1,70})", scripts)
    maths = re.findall(r"(?m)^\s*(?:const|let)\s+([a-zA-Z_$][\w$]*)\s*=\s*([^;\n]*(?:Math\.|\*|/|\+|-)[^;\n]*)", scripts)

    text_only = strip(markup)
    return {
        "slug": p.parent.name,
        "title": (re.search(r"<title>(.*?)\s*\|", raw, re.S) or [None, ""])[1].strip(),
        "description": (re.search(r'<meta name="description" content="([^"]*)"', raw) or [None, ""])[1],
        "words_now": len(text_only.split()),
        "inputs": inputs[:14],
        "selects": selects[:8],
        "labels": [l for l in labels if l][:18],
        "buttons": [b for b in buttons if b][:14],
        "headings": [h for h in heads if h][:14],
        "constants": [{"name": n, "value": v.strip()} for n, v in consts[:14]],
        "formulas": [{"name": n, "expr": e.strip()[:90]} for n, e in maths[:12]],
    }


def main() -> None:
    out = [facts(p) for p in sorted(TOOLS.glob("*/index.html"))]
    (ROOT / "app_facts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"extracted {len(out)} apps -> app_facts.json")
    thin = [a["slug"] for a in out if a["words_now"] < 300]
    print(f"pages under 300 words: {len(thin)}")


if __name__ == "__main__":
    main()
