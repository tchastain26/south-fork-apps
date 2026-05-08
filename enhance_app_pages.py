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

CATEGORY_SLUGS = {
    "Everyday Tools": "everyday-tools",
    "Text & Docs": "text-docs",
    "Code & Web": "code-web",
    "Design & Media": "design-media",
    "Productivity & Planning": "productivity-planning",
    "Fun & Games": "fun-games",
}

TOPIC_TITLES = {
    "calculators": "Calculators",
    "developer-tools": "Developer Tools",
    "text-tools": "Text Tools",
    "css-color-tools": "CSS & Color Tools",
    "generators": "Generators",
    "time-tools": "Time Tools",
}

HERO_CONTENT = {
    "word-counter": {
        "intro": "Use this free online word counter to measure draft length, reading time, speaking time, and paragraph structure before you publish, submit, or send.",
        "uses": [
            "Check article, essay, and newsletter length before you hit publish.",
            "Estimate reading or speaking time for scripts, meetings, and videos.",
            "Spot bloated sections by comparing paragraph and sentence counts.",
        ],
        "example": "Paste a draft and watch live counts update as you trim, expand, and polish the copy.",
        "topic": "text-tools",
    },
    "password-generator": {
        "intro": "Generate stronger passwords fast with adjustable length, symbols, numbers, and uppercase controls when you need a secure login or throwaway credential.",
        "uses": [
            "Create unique passwords for new accounts instead of reusing old ones.",
            "Compare length and character settings before you save a new login.",
            "Generate multiple options at once when rotating passwords across services.",
        ],
        "example": "Pick a length, enable the character sets you want, then copy one of the generated passwords that fits the site requirements.",
        "topic": "generators",
    },
    "qr-code-generator": {
        "intro": "Build QR codes for links, text, Wi-Fi credentials, and contact details in one place, then download a clean PNG you can use right away.",
        "uses": [
            "Create a QR code for menus, signs, handouts, and event tables.",
            "Share Wi-Fi access without typing a long password by hand.",
            "Turn a vCard or contact page into a scan-ready code for print.",
        ],
        "example": "Paste a URL or network name, preview the code, then download the PNG for print or social graphics.",
        "topic": "generators",
    },
    "json-formatter": {
        "intro": "Format, validate, and inspect JSON in the browser when you need readable payloads, quick debugging, or cleaner data before shipping it elsewhere.",
        "uses": [
            "Beautify minified API responses so nested objects are easier to inspect.",
            "Catch malformed JSON before it breaks an app, script, or webhook.",
            "Switch between pretty and compact output when copying data between tools.",
        ],
        "example": "Paste an API payload, validate it instantly, then copy the cleaned version back into your editor or request tool.",
        "topic": "developer-tools",
    },
    "regex-tester": {
        "intro": "Test regular expressions against real text with live matches, capture groups, and replacement previews before you move the pattern into production.",
        "uses": [
            "Debug patterns for logs, forms, validation rules, and content cleanup.",
            "See capture groups immediately instead of guessing what matched.",
            "Preview replacements before you run a find-and-replace across real data.",
        ],
        "example": "Drop in sample text, tweak the pattern, and verify the matches before you paste the regex into code.",
        "topic": "developer-tools",
    },
    "uuid-generator": {
        "intro": "Generate UUID v4 and v7 values in bulk when you need identifiers for databases, test fixtures, APIs, or content records.",
        "uses": [
            "Create batches of IDs for import files, mocks, and QA datasets.",
            "Switch output formats for braces, uppercase, or hyphenless IDs.",
            "Use UUID v7 when sortable identifiers are more useful than random-only values.",
        ],
        "example": "Choose the version and output style, generate a batch, then copy the IDs straight into your app or spreadsheet.",
        "topic": "developer-tools",
    },
    "robots-txt-builder": {
        "intro": "Build a clean robots.txt file with crawl rules, sitemap lines, and optional AI crawler blocking without hand-writing syntax from scratch.",
        "uses": [
            "Create a starter robots.txt for a new site in a few clicks.",
            "Block specific paths or crawler families without formatting mistakes.",
            "Add sitemap and crawl-delay lines while keeping the file readable.",
        ],
        "example": "Set your rules, review the generated text, then copy the finished file into your web root.",
        "topic": "developer-tools",
    },
    "css-gradient-generator": {
        "intro": "Build linear, radial, and conic gradients visually and copy production-ready CSS once the look is dialed in.",
        "uses": [
            "Mock up hero backgrounds, buttons, and cards without trial-and-error coding.",
            "Adjust color stops, angle, and gradient type while watching the preview.",
            "Copy the final CSS once the gradient is approved for a design system or page.",
        ],
        "example": "Pick your colors, move the stops until the preview feels right, then copy the CSS directly into your stylesheet.",
        "topic": "css-color-tools",
    },
    "css-clamp-generator": {
        "intro": "Generate responsive CSS clamp() values for type, spacing, and layout with real viewport ranges instead of hand-calculating the math.",
        "uses": [
            "Create fluid type scales between mobile and desktop breakpoints.",
            "Set responsive padding, gaps, and margins without extra media queries.",
            "Copy the finished clamp() line straight into a component stylesheet.",
        ],
        "example": "Enter the small and large values you want, define the viewport range, then copy the resulting clamp() declaration.",
        "topic": "css-color-tools",
    },
    "html-preview": {
        "intro": "Write HTML and see the rendered result side by side when you need a fast scratchpad for markup, snippets, or embed code.",
        "uses": [
            "Preview snippets before dropping them into a CMS or email builder.",
            "Test layout fragments without spinning up a local project.",
            "Catch simple markup issues by comparing the source and rendered output together.",
        ],
        "example": "Paste a snippet, edit in place, and verify the live preview before you move the markup somewhere permanent.",
        "topic": "developer-tools",
    },
    "markdown-to-html": {
        "intro": "Convert Markdown to clean HTML with a live preview when you are moving writing into a CMS, email tool, or static site workflow.",
        "uses": [
            "Turn notes or article drafts into HTML for publishing workflows.",
            "Check rendered headings, lists, and links before exporting the markup.",
            "Compare the raw Markdown and final HTML without switching tools.",
        ],
        "example": "Paste Markdown on the left, confirm the preview, then copy the generated HTML where you need it.",
        "topic": "text-tools",
    },
    "color-palette": {
        "intro": "Generate structured color palettes from one base color so you can explore usable combinations instead of guessing shades one by one.",
        "uses": [
            "Build complementary, analogous, triadic, or split-complementary schemes fast.",
            "Start a brand, slide, or UI palette from a single color you already trust.",
            "Copy the HEX values once you land on a direction that works.",
        ],
        "example": "Pick a base color, review the generated palette families, then copy the swatches you want into your design tool or CSS.",
        "topic": "css-color-tools",
    },
    "color-contrast-checker": {
        "intro": "Check foreground and background pairs against WCAG contrast standards before you ship a design, component, or brand palette.",
        "uses": [
            "Test text and background colors for AA and AAA accessibility targets.",
            "Compare alternatives when a brand color looks good but reads poorly.",
            "Validate color choices during UI design instead of after development.",
        ],
        "example": "Enter the two colors, review the score, then adjust the pair until the contrast passes the accessibility target you need.",
        "topic": "css-color-tools",
    },
    "unit-converter": {
        "intro": "Convert everyday measurements quickly across length, weight, temperature, volume, and speed without bouncing between niche calculators.",
        "uses": [
            "Switch between metric and imperial values while cooking, building, or traveling.",
            "Compare units in one place instead of opening several single-purpose tools.",
            "Double-check figures before entering them into forms, quotes, or reports.",
        ],
        "example": "Pick the measurement type, enter a value once, and read the converted results across the units you care about.",
        "topic": "calculators",
    },
    "bmi-calculator": {
        "intro": "Calculate BMI in either imperial or metric units and see the result with a quick category check and healthy range reference.",
        "uses": [
            "Check BMI from height and weight without doing the formula by hand.",
            "Switch between pounds and inches or kilograms and centimeters instantly.",
            "Use the result as a quick reference point during basic health tracking.",
        ],
        "example": "Enter height and weight, review the BMI score, then compare it with the healthy range shown beside the result.",
        "topic": "calculators",
    },
    "compound-interest": {
        "intro": "Model savings and investing growth with compound interest, recurring contributions, and a year-by-year breakdown you can actually read.",
        "uses": [
            "Estimate how a balance grows with monthly contributions over time.",
            "Compare timelines when you change the rate, term, or contribution amount.",
            "Use the chart and table to explain growth assumptions to someone else.",
        ],
        "example": "Set the opening balance, contribution, rate, and term, then review the projected growth across the full timeline.",
        "topic": "calculators",
    },
    "date-calculator": {
        "intro": "Calculate the gap between two dates or move forward and backward from a starting date when planning schedules, contracts, and deadlines.",
        "uses": [
            "Count days between milestones, trips, or billing periods.",
            "Add or subtract days from a date without mental calendar math.",
            "Check delivery, renewal, and deadline timing before you commit.",
        ],
        "example": "Choose the two dates or pick a starting point plus a number of days to get the result immediately.",
        "topic": "calculators",
    },
    "percentage-calculator": {
        "intro": "Handle the most common percentage questions in one place, including percent of a number, percentage change, and quick markups or markdowns.",
        "uses": [
            "Figure out discounts, tips, markups, and percentage increases fast.",
            "Compare change between two values without hand-running the formula.",
            "Check percentage math before you send pricing, budgets, or reports.",
        ],
        "example": "Pick the percentage mode you need, enter the values, and copy the result without opening a spreadsheet.",
        "topic": "calculators",
    },
    "timestamp-converter": {
        "intro": "Convert Unix timestamps to human-readable dates and back when debugging APIs, logs, schedulers, and database values.",
        "uses": [
            "Read raw timestamps from logs without jumping into a terminal or REPL.",
            "Switch between seconds and milliseconds when systems disagree on format.",
            "Generate a fresh timestamp value for testing payloads and automation rules.",
        ],
        "example": "Paste the raw timestamp or date string, then copy the converted value you need for the next step.",
        "topic": "time-tools",
    },
    "text-diff": {
        "intro": "Compare two blocks of text line by line to see additions, deletions, and edits without loading a full code diff tool.",
        "uses": [
            "Check changes between drafts, prompts, configs, and copied snippets.",
            "See what moved or changed before you overwrite an important block of text.",
            "Review line-level edits quickly when a plain text file has no version history.",
        ],
        "example": "Paste the original on one side and the revision on the other to highlight exactly what changed.",
        "topic": "text-tools",
    },
}

DISCOVERY_CSS = """
/* SFA_DISCOVERY_START */
.sfa-feature,
.sfa-related{
  width:min(1080px,calc(100% - 2rem));
  margin:2rem auto 0;
}
.sfa-feature-shell,
.sfa-related-shell{
  border:1px solid rgba(63,73,62,.45);
  background:rgba(29,32,30,.78);
  border-radius:16px;
  padding:1rem;
  backdrop-filter:blur(12px);
}
.sfa-feature-shell{
  display:grid;
  grid-template-columns:minmax(0,1.1fr) minmax(280px,.9fr);
  gap:1rem;
  align-items:start;
}
.sfa-kicker{
  color:#7ddb84;
  font-size:.72rem;
  font-weight:800;
  text-transform:uppercase;
  letter-spacing:.12em;
  margin:0 0 .55rem;
}
.sfa-feature h2{
  margin:0 0 .65rem;
  font-size:clamp(1.3rem,2vw,1.85rem);
  line-height:1.1;
  color:#e8e8e8;
}
.sfa-feature p{
  margin:0;
}
.sfa-feature-copy > p + p{
  margin-top:.85rem;
}
.sfa-bullets{
  margin:.95rem 0 0;
  padding-left:1.15rem;
  color:#d3dbd4;
}
.sfa-bullets li{
  margin:.5rem 0;
  line-height:1.55;
}
.sfa-example{
  margin-top:1rem;
  padding:.95rem 1rem;
  border:1px solid rgba(125,219,132,.18);
  border-radius:14px;
  background:rgba(17,20,18,.82);
}
.sfa-example strong{
  display:block;
  color:#e8e8e8;
  font-size:.92rem;
  margin-bottom:.35rem;
}
.sfa-example span{
  display:block;
  color:#aab5ac;
  font-size:.92rem;
  line-height:1.55;
}
.sfa-links{
  display:flex;
  flex-wrap:wrap;
  gap:.7rem;
  margin-top:1rem;
}
.sfa-links a{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-height:2.55rem;
  padding:0 .95rem;
  border-radius:999px;
  border:1px solid rgba(125,219,132,.28);
  color:#7ddb84;
  text-decoration:none;
  font-size:.82rem;
  font-weight:700;
}
.sfa-links a:hover{
  background:rgba(125,219,132,.1);
}
.sfa-preview{
  margin:0;
}
.sfa-preview img{
  display:block;
  width:100%;
  border-radius:14px;
  border:1px solid rgba(63,73,62,.6);
  background:#111412;
}
.sfa-preview figcaption{
  margin-top:.7rem;
  color:#aab5ac;
  font-size:.82rem;
  line-height:1.55;
}
.sfa-related{
  padding:1.25rem 0 0;
  border-top:1px solid rgba(125,219,132,.18);
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
  .sfa-feature-shell,
  .sfa-related-grid{
    grid-template-columns:1fr;
  }
}
/* SFA_DISCOVERY_END */
""".strip()


def app_url(slug: str) -> str:
    return f"{BASE_URL}/South%20Fork%20Apps%20Collection/{slug}/"


def asset_url(slug: str, filename: str) -> str:
    return f"{app_url(slug)}{filename}"


def category_url(category: str) -> str:
    return f"{BASE_URL}/categories/{CATEGORY_SLUGS[category]}/"


def topic_url(slug: str) -> str:
    return f"{BASE_URL}/topics/{slug}/"


def strip_tags(text: str) -> str:
    clean = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(clean)).strip()


def extract_page_title(text: str, fallback: str) -> str:
    match = re.search(r"<title>(.*?)\s*\|\s*South Fork Apps</title>", text, re.S | re.I)
    if not match:
        return fallback
    value = strip_tags(match.group(1))
    return value or fallback


def extract_meta_description(text: str, fallback: str) -> str:
    match = re.search(r'<meta name="description" content="([^"]*)">', text, re.I)
    if not match:
        return fallback
    value = html.unescape(match.group(1)).strip()
    return value or fallback


def app_cards_from_homepage() -> list[dict[str, str]]:
    text = INDEX_PATH.read_text(encoding="utf-8")
    start = text.index('<div id="appGrid"')
    end = text.index('<div id="noResults"')
    grid = text[start:end]
    pattern = re.compile(
        r'<div data-app-card data-title="([^"]+)" data-description="([^"]+)" '
        r'data-category="([^"]+)".*?<a href="/South%20Fork%20Apps%20Collection/([^/]+)/"',
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


def normalize_primary_heading(text: str, app: dict[str, str]) -> str:
    match = re.search(r"<h1\b([^>]*)>(.*?)</h1>", text, re.S | re.I)
    if not match:
        h2_match = re.search(r"<h2\b([^>]*)>(.*?)</h2>", text, re.S | re.I)
        if h2_match:
            replacement = f"<h1{h2_match.group(1)}>{html.escape(app['title'])}</h1>"
            return text[: h2_match.start()] + replacement + text[h2_match.end() :]

        title_block = re.search(r"<div\b([^>]*)\bid=['\"]title['\"]([^>]*)>.*?</div>", text, re.S | re.I)
        if title_block:
            attrs = f"{title_block.group(1)} id=\"title\"{title_block.group(2)}"
            replacement = f"<h1{attrs}>{html.escape(app['title'])}</h1>"
            return text[: title_block.start()] + replacement + text[title_block.end() :]

        return text

    current = strip_tags(match.group(2)).lower()
    target = app["title"].lower()
    if current == target:
        return text

    replacement = f"<h1{match.group(1)}>{html.escape(app['title'])}</h1>"
    return text[: match.start()] + replacement + text[match.end() :]


def normalize_hero_intro(text: str, intro: str) -> str:
    pattern = re.compile(r"(<h1\b[^>]*>.*?</h1>\s*<p\b[^>]*>)(.*?)(</p>)", re.S | re.I)
    match = pattern.search(text)
    if not match:
        return text
    return text[: match.start()] + match.group(1) + html.escape(intro) + match.group(3) + text[match.end() :]


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
        "mainEntityOfPage": app_url(app["slug"]),
    }

    hero = HERO_CONTENT.get(app["slug"])
    if hero:
        payload["featureList"] = hero["uses"]

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


def insert_before_related_or_footer(text: str, block: str) -> str:
    marker = "<!-- SFA_RELATED_START -->"
    index = text.find(marker)
    if index != -1:
        return text[:index] + block + "\n" + text[index:]
    return insert_before_footerish(text, block)


def inject_feature_section(text: str, app: dict[str, str]) -> str:
    text = remove_marked_block(text, "SFA_FEATURE")
    hero = HERO_CONTENT.get(app["slug"])

    if hero:
        bullets = "\n".join(f"        <li>{html.escape(item)}</li>" for item in hero["uses"])
        topic_slug = hero["topic"]
        links = f"""
      <div class="sfa-links">
        <a href="{category_url(app['category'])}">More {html.escape(app['category'])}</a>
        <a href="{topic_url(topic_slug)}">{html.escape(TOPIC_TITLES[topic_slug])}</a>
        <a href="{BASE_URL}/privacy/">Privacy</a>
      </div>
""".rstrip()
        block = f"""<!-- SFA_FEATURE_START -->
<section class="sfa-feature" aria-labelledby="sfa-feature-title">
  <div class="sfa-feature-shell">
    <div class="sfa-feature-copy">
      <div class="sfa-kicker">Why people use this tool</div>
      <h2 id="sfa-feature-title">{html.escape(app['title'])}</h2>
      <p>{html.escape(hero['intro'])}</p>
      <ul class="sfa-bullets">
{bullets}
      </ul>
      <div class="sfa-example">
        <strong>Typical workflow</strong>
        <span>{html.escape(hero['example'])}</span>
      </div>
{links}
    </div>
    <figure class="sfa-preview">
      <img src="screenshot.jpg" alt="{html.escape(app['title'], quote=True)} interface preview" loading="lazy" decoding="async" width="1600" height="900">
      <figcaption>Live interface preview for {html.escape(app['title'])}. This screenshot is also the landing image Google can associate with the tool page.</figcaption>
    </figure>
  </div>
</section>
<!-- SFA_FEATURE_END -->"""
    else:
        block = f"""<!-- SFA_FEATURE_START -->
<section class="sfa-feature" aria-labelledby="sfa-feature-title">
  <div class="sfa-feature-shell">
    <div class="sfa-feature-copy">
      <div class="sfa-kicker">Preview</div>
      <h2 id="sfa-feature-title">{html.escape(app['title'])}</h2>
      <p>{html.escape(app['description'])}</p>
      <p>See the interface before you use it, then jump to more tools in the same lane if you need a nearby workflow.</p>
      <div class="sfa-links">
        <a href="{category_url(app['category'])}">More {html.escape(app['category'])}</a>
        <a href="{BASE_URL}/about/">About South Fork Apps</a>
        <a href="{BASE_URL}/privacy/">Privacy</a>
      </div>
    </div>
    <figure class="sfa-preview">
      <img src="screenshot.jpg" alt="{html.escape(app['title'], quote=True)} interface preview" loading="lazy" decoding="async" width="1600" height="900">
      <figcaption>Screenshot of the live {html.escape(app['title'])} interface.</figcaption>
    </figure>
  </div>
</section>
<!-- SFA_FEATURE_END -->"""

    return insert_before_related_or_footer(text, block)


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
        page_app = {
            **app,
            "title": extract_page_title(text, app["title"]),
            "description": extract_meta_description(text, app["description"]),
        }

        text = normalize_primary_heading(text, page_app)

        hero = HERO_CONTENT.get(slug)
        if hero:
            text = normalize_hero_intro(text, hero["intro"])

        text = inject_social_block(text, page_app)
        text = inject_jsonld(text, page_app)
        text = inject_discovery_css(text)
        text = inject_feature_section(text, page_app)
        text = inject_related_section(text, page_app, related_apps(apps, slug))
        path.write_text(text, encoding="utf-8")
        print(f"UPDATED {slug}")


if __name__ == "__main__":
    main()
