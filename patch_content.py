#!/usr/bin/env python3
"""Merge extra fields into existing app_content.json entries without replacing them."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "app_content.json"

def main() -> None:
    patch = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    cur = json.loads(MAIN.read_text(encoding="utf-8"))
    missing = [s for s in patch if s not in cur]
    if missing:
        raise SystemExit(f"not yet authored, patch would create partial entries: {missing}")
    added = 0
    for slug, fields in patch.items():
        for k, v in fields.items():
            if k in cur[slug]:
                print(f"  overwriting {slug}.{k}")
            cur[slug][k] = v
            added += 1
    MAIN.write_text(json.dumps(cur, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"patched {len(patch)} entries, {added} fields")

if __name__ == "__main__":
    main()
