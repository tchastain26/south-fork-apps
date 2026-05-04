#!/usr/bin/env python3

from __future__ import annotations

import html
import json
import re
from pathlib import Path

BASE_URL = "https://southforkapps.com"
ROOT = Path(__file__).resolve().parent
COLLECTION_DIR = ROOT / "South Fork Apps Collection"
INDEX_PATH = ROOT / "index.html"

CATEGORY_SCHEMA = {
    "Everyday Tools": {"type": "SoftwareApplication", "applicationCategory": "UtilitiesApplication"},
    "Text & Docs": {"type": "SoftwareApplication", "applicationCategory": "ProductivityApplication"},
    "Code & Web": {"type": "DeveloperApplication", "applicationCategory": "DeveloperApplication"},
    "Design & Media": {"type": "SoftwareApplication", "applicationCategory": "DesignApplication"},
    "Productivity & Planning": {"type": "SoftwareApplication", "applicationCategory": "ProductivityApplication"},
    "Fun & Games": {"type": "GameApplication", "applicationCategory": "GameApplication"},
}

DISCOVERY_CSS = """
/* SFA_DISCOVERY_START */
.sfa-related{
  width:min(1080px,calc(100% - 2rem));
  margin:2rem auto 0;
  padding:1.25rem 0 0;
  border-top:1px solid rgba(125,219,132,.18);
}
.sfa-related-shell{
  border:1px solid rgba(63,73,62,.45);
  background:rgba(29,32,30,.78);
  border-radius:16px;
  padding:1rem;
  backdrop-filter:blur(12px);
}
.sfa-related-header{
  display:flex;
  justify-content:space-between;
  align-items:baseline;
  gap:.75rem;
  margin-bottom:1rem;
  flex-wrap:wrap;
}
.sfa-related-title{
  font-size:1rem;
  font-weight:800;
  color:#e8e8e8;
}
.sfa-related-meta{
  color:#aab5ac;
  font-size:.78rem;
  text-transform:uppercase;
  letter-spacing:.08em;
  font-weight:700;
}
.sfa-related-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:.85rem;
}
.sfa-related-card{
  display:block;
  padding:1rem;
  border:1px solid rgba(63,73,62,.55);
  border-radius:14px;
  background:rgba(17,20,18,.88);
  text-decoration:none;
  transition:transform .15s ease,border-color .15s ease,background .15s ease;
}
.sfa-related-card:hover{
  transform:translateY(-1px);
  border-color:rgba(125,219,132,.45);
  background:rgba(29,32,30,.96);
}
.sfa-related-card strong{
  display:block;
  color:#e8e8e8;
  font-size:.98rem;
  line-height:1.25;
  margin-bottom:.45rem;
}
.sfa-related-card span{
  display:block;
  color:#aab5ac;
  font-size:.84rem;
  line-height:1.5;
}
@media (max-width:820px){
  .sfa-related-grid{grid-template-columns:1fr;}
}
/* SFA_DISCOVERY_END */
""".strip()


def app_url(slug: str) -> str:
    return f"{BASE_URL}/South%20Fork%20Apps%20Collection/{slug}/"


def asset_url(slug: str, filename: str) -> str:
    return f"{app_url(slug)}{filename}"


def app_cards_from_homepage() -> list[dict[str, str]]:
    text = INDEX_PATH.read_text(encoding="utf-8")
    start = text.index('<div id="appGrid"')
    end = text.index('<div id="noResults"')
    grid = text[start:end]
    pattern = re.compile(
        r'<div data-app-card data-title="([^"]+)" data-description="([^"]+)" '
        r'data-category="([^"]+)".*?<a href="\./South Fork Apps Collection/([^/]+)/"',
        re.S,
    )
    apps = []
    for title, desc, category, slug in pattern.findall(grid):
        apps.append(
            {
                "slug": slug,
                "title": html.unescape(title),
                "description": html.unescape(desc),
                "category": html.unescape(category),
            }
        )
    return apps


def remove_marked_block(text: str, marker: str) -> str:
    pattern = re.compile(
        rf"\n?(?:<!--|/\*) {re.escape(marker)}_START(?: -->|\*/).*?(?:<!--|/\*) {re.escape(marker)}_END(?: -->|\*/)\n?",
        re.S,
    )
    return pattern.sub("\n", text)


def inject_social_block(text: str, app: dict[str, str]) -> str:
    social = f"""
<!-- SFA_SOCIAL_START -->
<link rel="canonical" href="{app_url(app['slug'])}">
<meta property="og:site_name" content="South Fork Apps">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(app['title'], quote=True)}">
<meta property="og:description" content="{html.escape(app['description'], quote=True)}">
<meta property="og:url" content="{app_url(app['slug'])}">
<meta property="og:image" content="{asset_url(app['slug'], 'share.jpg')}">
<meta property="og:image:alt" content="{html.escape(app['title'], quote=True)} preview image">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(app['title'], quote=True)}">
<meta name="twitter:description" content="{html.escape(app['description'], quote=True)}">
<meta name="twitter:image" content="{asset_url(app['slug'], 'share.jpg')}">
<!-- SFA_SOCIAL_END -->
""".strip()
    text = remove_marked_block(text, "SFA_SOCIAL")
    desc_match = re.search(r'<meta name="description" content="[^"]*">\s*', text)
    if desc_match:
        return text[: desc_match.end()] + social + "\n" + text[desc_match.end() :]
    return text.replace("</head>", social + "\n</head>", 1)


def inject_jsonld(text: str, app: dict[str, str]) -> str:
    schema_info = CATEGORY_SCHEMA[app["category"]]
    payload = {
        "@context": "https://schema.org",
        "@type": schema_info["type"],
        "name": app["title"],
        "description": app["description"],
        "applicationCategory": schema_info["applicationCategory"],
        "operatingSystem": "Any",
        "url": app_url(app["slug"]),
        "image": asset_url(app["slug"], "share.jpg"),
        "screenshot": asset_url(app["slug"], "screenshot.jpg"),
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "author": {"@type": "Person", "name": "Tucker Chastain"},
        "publisher": {"@type": "Organization", "name": "South Fork Apps", "url": BASE_URL},
    }
    block = (
        "<!-- SFA_JSONLD_START -->\n"
        '<script type="application/ld+json">\n'
        + json.dumps(payload, indent=2)
        + "\n</script>\n"
        "<!-- SFA_JSONLD_END -->"
    )
    text = remove_marked_block(text, "SFA_JSONLD")
    return text.replace("</head>", block + "\n</head>", 1)


def inject_discovery_css(text: str) -> str:
    text = remove_marked_block(text, "SFA_DISCOVERY")
    return text.replace("</style>", "\n" + DISCOVERY_CSS + "\n</style>", 1)


def related_apps(all_apps: list[dict[str, str]], slug: str) -> list[dict[str, str]]:
    current = next(app for app in all_apps if app["slug"] == slug)
    siblings = [app for app in all_apps if app["category"] == current["category"]]
    siblings.sort(key=lambda item: item["title"].lower())
    current_index = next(index for index, item in enumerate(siblings) if item["slug"] == slug)
    picks = []
    for offset in range(1, 4):
        picks.append(siblings[(current_index + offset) % len(siblings)])
    return picks


def insert_before_footerish(text: str, block: str) -> str:
    footer_match = re.search(r"\n\s*<footer\b", text)
    if footer_match:
        return text[: footer_match.start()] + "\n" + block + "\n" + text[footer_match.start() :]

    version_match = re.search(r"\n\s*<p[^>]*>\s*v1\.0\s*</p>", text, re.I)
    if version_match:
        return text[: version_match.start()] + "\n" + block + "\n" + text[version_match.start() :]

    main_close = text.rfind("</main>")
    if main_close != -1:
        return text[:main_close] + "\n" + block + "\n" + text[main_close:]

    return text.replace("</body>", block + "\n</body>", 1)


def inject_related_section(text: str, app: dict[str, str], related: list[dict[str, str]]) -> str:
    text = remove_marked_block(text, "SFA_RELATED")
    cards = "\n".join(
        f"""        <a class="sfa-related-card" href="{app_url(item['slug'])}">
          <strong>{html.escape(item['title'])}</strong>
          <span>{html.escape(item['description'])}</span>
        </a>"""
        for item in related
    )
    block = f"""<!-- SFA_RELATED_START -->
<section class="sfa-related" aria-label="More apps in {html.escape(app['category'])}">
  <div class="sfa-related-shell">
    <div class="sfa-related-header">
      <div class="sfa-related-title">More {html.escape(app['category'])}</div>
      <div class="sfa-related-meta">South Fork Apps</div>
    </div>
    <div class="sfa-related-grid">
{cards}
    </div>
  </div>
</section>
<!-- SFA_RELATED_END -->"""
    return insert_before_footerish(text, block)


def main() -> None:
    apps = app_cards_from_homepage()
    app_lookup = {app["slug"]: app for app in apps}

    for path in sorted(COLLECTION_DIR.glob("*/index.html")):
        slug = path.parent.name
        app = app_lookup.get(slug)
        if not app:
            print(f"SKIP {slug}: not in homepage metadata")
            continue

        text = path.read_text(encoding="utf-8")
        text = inject_social_block(text, app)
        text = inject_jsonld(text, app)
        text = inject_discovery_css(text)
        text = inject_related_section(text, app, related_apps(apps, slug))
        path.write_text(text, encoding="utf-8")
        print(f"UPDATED {slug}")


if __name__ == "__main__":
    main()
