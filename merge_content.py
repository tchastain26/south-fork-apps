#!/usr/bin/env python3
"""Merge a batch of authored tool content into app_content.json."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "app_content.json"

def main() -> None:
    batch = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    cur = json.loads(MAIN.read_text(encoding="utf-8")) if MAIN.exists() else {}
    slugs = {p.parent.name for p in (ROOT / "tools").glob("*/index.html")}
    unknown = [s for s in batch if s not in slugs]
    if unknown:
        raise SystemExit(f"unknown slugs: {unknown}")
    new = [s for s in batch if s not in cur]
    cur.update(batch)
    MAIN.write_text(json.dumps(cur, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"merged {len(batch)} ({len(new)} new). total {len(cur)}/{len(slugs)}")

if __name__ == "__main__":
    main()
