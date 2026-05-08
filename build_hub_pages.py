#!/usr/bin/env python3

from __future__ import annotations

import html
import re
from pathlib import Path

BASE_URL = "https://southforkapps.com"
ROOT = Path(__file__).resolve().parent
INDEX_PATH = ROOT / "index.html"

CATEGORY_INFO = {
    "Everyday Tools": {
        "slug": "everyday-tools",
        "title": "Everyday Tools",
        "description": "Free online calculators, validators, converters, and practical browser tools for daily work.",
        "intro": "This category groups the practical tools you reach for when you need a quick answer, a cleaner number, or a fast utility without opening a spreadsheet or installing an app.",
        "bullets": [
            "Health, money, time, and conversion tools in one place.",
            "Built for quick checks, planning, and real-life tasks.",
            "Works well for people who need answers faster than a search result thread.",
        ],
        "related_topics": ["calculators", "generators", "time-tools"],
    },
    "Text & Docs": {
        "slug": "text-docs",
        "title": "Text and Document Tools",
        "description": "Free online text, writing, Markdown, formatting, extraction, and cleanup tools.",
        "intro": "These tools help with writing, editing, cleanup, formatting, and conversion when text work is the job, not a side effect.",
        "bullets": [
            "Useful for writers, editors, marketers, and messy copy-paste workflows.",
            "Includes word stats, cleanup tools, Markdown helpers, and extraction tools.",
            "Fast enough for daily draft work and one-off formatting fixes.",
        ],
        "related_topics": ["text-tools", "generators"],
    },
    "Code & Web": {
        "slug": "code-web",
        "title": "Code and Web Tools",
        "description": "Free online developer utilities for JSON, regex, UUIDs, timestamps, markup, and web workflows.",
        "intro": "This is the browser-first developer shelf: tools for debugging, converting, testing, and shipping small web tasks without opening a heavier stack.",
        "bullets": [
            "Made for API work, front-end chores, payload cleanup, and quick validation.",
            "Strong fit for developers, technical marketers, and no-code builders.",
            "Focused on speed, readable output, and copy-ready results.",
        ],
        "related_topics": ["developer-tools", "css-color-tools", "time-tools"],
    },
    "Design & Media": {
        "slug": "design-media",
        "title": "Design and Media Tools",
        "description": "Free online tools for color, contrast, gradients, SVGs, CSS visuals, and screen-friendly design work.",
        "intro": "These tools support the visual side of web work: colors, gradients, contrast, CSS effects, and assets that need to look right before they ship.",
        "bullets": [
            "Helpful for UI work, brand experiments, and fast front-end styling.",
            "Covers accessibility, palette building, CSS visuals, and asset prep.",
            "Designed to help you make decisions without round-tripping through a full design app.",
        ],
        "related_topics": ["css-color-tools", "generators"],
    },
    "Productivity & Planning": {
        "slug": "productivity-planning",
        "title": "Productivity and Planning Tools",
        "description": "Free online timers, boards, trackers, and planning tools for focused work and lightweight systems.",
        "intro": "This category collects the tools that help you think, plan, focus, and keep work moving without turning everything into a giant productivity system.",
        "bullets": [
            "Great for focus sessions, planning blocks, and lightweight task workflows.",
            "Includes timers, trackers, and planning helpers that stay out of the way.",
            "Useful when you want momentum, not a full project management suite.",
        ],
        "related_topics": ["time-tools", "calculators"],
    },
    "Fun & Games": {
        "slug": "fun-games",
        "title": "Fun and Games",
        "description": "Free playful web apps, randomizers, novelty generators, clocks, and browser toys.",
        "intro": "Not every useful tool has to be serious. This section collects the playful side of South Fork Apps: generators, pickers, clocks, and small browser toys that are still built with care.",
        "bullets": [
            "Good for breaks, icebreakers, classrooms, and harmless weirdness.",
            "Includes randomizers, novelty tools, and interactive experiments.",
            "Still browser-fast, still easy to share, just less serious.",
        ],
        "related_topics": ["generators", "time-tools"],
    },
}

TOPIC_INFO = {
    "text-tools": {
        "title": "Free Online Text Tools",
        "description": "Word count, text compare, Markdown, formatting, cleanup, and extraction tools that run in the browser.",
        "intro": "These are the text tools most people actually need: count it, compare it, clean it, convert it, or pull something out of it without opening a bigger editor.",
        "bullets": [
            "Best for writers, editors, prompt work, and copy cleanup.",
            "Focuses on fast output you can paste into the next step immediately.",
            "Useful for both one-off fixes and daily writing workflows.",
        ],
        "apps": [
            "word-counter",
            "text-diff",
            "markdown-to-html",
            "word-wrap",
            "email-extractor",
            "word-frequency",
            "reading-level-analyzer",
            "markdown-table-maker",
            "slugify-text",
            "dedupe-lines",
        ],
    },
    "developer-tools": {
        "title": "Free Online Developer Tools",
        "description": "JSON, regex, UUID, timestamp, HTML, robots.txt, and payload tools for browser-based dev workflows.",
        "intro": "This hub covers the small browser tools that save time during development: format data, test expressions, inspect timestamps, and generate output you can copy back into code.",
        "bullets": [
            "Useful for API work, front-end debugging, and data cleanup.",
            "Prioritizes fast validation and copy-ready output.",
            "Built for the boring chores that still eat developer time.",
        ],
        "apps": [
            "json-formatter",
            "regex-tester",
            "uuid-generator",
            "timestamp-converter",
            "html-preview",
            "robots-txt-builder",
            "json-yaml-converter",
            "csv-json-converter",
            "jwt-decoder",
            "chmod-calculator",
        ],
    },
    "calculators": {
        "title": "Free Online Calculators",
        "description": "Online calculators for dates, percentages, money, health, savings, sleep, and everyday planning.",
        "intro": "This page collects the calculators that solve everyday math without turning into full spreadsheet projects. If the question starts with how much, how long, how many, or what percent, start here.",
        "bullets": [
            "Covers money, dates, health, and real-world planning math.",
            "Good for quick checks before decisions, quotes, or schedules.",
            "Works well when you want an answer now instead of a formula later.",
        ],
        "apps": [
            "date-calculator",
            "percentage-calculator",
            "compound-interest",
            "unit-converter",
            "bmi-calculator",
            "loan-calculator",
            "savings-goal-planner",
            "sleep-cycle-calculator",
            "pay-converter",
            "recipe-scaler",
        ],
    },
    "css-color-tools": {
        "title": "Free CSS and Color Tools",
        "description": "Online tools for gradients, clamp values, contrast checks, palettes, filters, and CSS visuals.",
        "intro": "Use these tools when the job is visual front-end work: color choices, gradient experiments, responsive sizing, contrast checks, and CSS output you can ship.",
        "bullets": [
            "Strong fit for designers, developers, and anyone styling the web directly.",
            "Mixes accessibility, visual exploration, and production-ready CSS output.",
            "Useful for both fast experiments and repeatable UI work.",
        ],
        "apps": [
            "css-gradient-generator",
            "css-clamp-generator",
            "color-palette",
            "color-contrast-checker",
            "box-shadow-generator",
            "css-filter-generator",
            "css-unit-converter",
            "color-name-finder",
            "svg-to-data-url",
            "hex-code-color-generator",
        ],
    },
    "generators": {
        "title": "Free Online Generators",
        "description": "Password, QR code, UUID, ASCII art, lorem ipsum, quote, and other browser-based generators.",
        "intro": "This hub groups the generators people actually reuse: assets, IDs, filler, passwords, randomizers, and other tools that produce something ready to copy or share.",
        "bullets": [
            "Helpful when you need output quickly instead of another blank form.",
            "Includes both practical generators and a few lighter creative ones.",
            "Great for content work, setup tasks, and one-off browser jobs.",
        ],
        "apps": [
            "password-generator",
            "qr-code-generator",
            "uuid-generator",
            "passphrase-generator",
            "ascii-art-generator",
            "lorem-ipsum-generator",
            "hex-code-color-generator",
            "bingo-maker",
            "random-quote",
            "magic-8-ball",
        ],
    },
    "time-tools": {
        "title": "Free Online Time Tools",
        "description": "Online timestamp, timer, stopwatch, sleep, pace, meeting, and time conversion tools.",
        "intro": "These tools help when time is the main variable: convert it, count it down, plan around it, or turn it into a clearer schedule signal.",
        "bullets": [
            "Useful for deadlines, focus sessions, pacing, logs, and scheduling math.",
            "Combines developer time tools with everyday planning helpers.",
            "Designed for quick reads and practical next steps.",
        ],
        "apps": [
            "timestamp-converter",
            "countdown-timer",
            "pomodoro-timer",
            "stopwatch",
            "task-timer",
            "breath-timer",
            "meeting-cost-tracker",
            "pace-calculator",
            "millisecond-converter",
            "sleep-cycle-calculator",
        ],
    },
}


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


def app_url(slug: str) -> str:
    return f"{BASE_URL}/South%20Fork%20Apps%20Collection/{slug}/"


def category_url(category: str) -> str:
    return f"{BASE_URL}/categories/{CATEGORY_INFO[category]['slug']}/"


def topic_url(slug: str) -> str:
    return f"{BASE_URL}/topics/{slug}/"


def card_markup(app: dict[str, str]) -> str:
    return f"""<a class="card" href="{app_url(app['slug'])}">
  <div class="card-meta">{html.escape(app['category'])}</div>
  <h3>{html.escape(app['title'])}</h3>
  <p>{html.escape(app['description'])}</p>
</a>"""


def pill_link(href: str, label: str) -> str:
    return f'<a class="pill" href="{href}">{html.escape(label)}</a>'


def page_shell(*, title: str, description: str, canonical: str, body_class: str, eyebrow: str, heading: str, intro: str, bullets: list[str], main_html: str, jsonld_type: str = "CollectionPage", image: str | None = None) -> str:
    image_url = image or f"{BASE_URL}/South%20Fork%20Apps%20Collection/word-counter/share.jpg"
    bullets_html = "\n".join(f"<li>{html.escape(item)}</li>" for item in bullets)
    jsonld = f"""{{
  "@context": "https://schema.org",
  "@type": "{jsonld_type}",
  "name": "{html.escape(heading, quote=True)}",
  "description": "{html.escape(description, quote=True)}",
  "url": "{canonical}"
}}"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} | South Fork Apps</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:site_name" content="South Fork Apps">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{image_url}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title, quote=True)}">
  <meta name="twitter:description" content="{html.escape(description, quote=True)}">
  <meta name="twitter:image" content="{image_url}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #111412;
      --surface: rgba(29, 32, 30, 0.86);
      --surface-strong: rgba(17, 20, 18, 0.92);
      --border: rgba(63, 73, 62, 0.7);
      --accent: #7ddb84;
      --accent-soft: rgba(125, 219, 132, 0.12);
      --text: #e1e3df;
      --muted: #becaba;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: "Plus Jakarta Sans", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at 15% 20%, rgba(125, 219, 132, 0.08), transparent 35%),
        radial-gradient(circle at 85% 75%, rgba(170, 204, 218, 0.08), transparent 38%),
        linear-gradient(180deg, #0f1311 0%, #111412 100%);
    }}
    a {{ color: inherit; }}
    .wrap {{
      width: min(1180px, calc(100% - 2rem));
      margin: 0 auto;
    }}
    .nav {{
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(11, 18, 14, 0.82);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(63, 73, 62, 0.45);
    }}
    .nav-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      padding: 1rem 0;
    }}
    .brand {{
      font-family: "Epilogue", sans-serif;
      font-size: 1.1rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--accent);
      text-decoration: none;
    }}
    .nav-links {{
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
    }}
    .nav-links a {{
      text-decoration: none;
      color: var(--muted);
      font-size: 0.92rem;
    }}
    .nav-links a:hover,
    .nav-links a:focus-visible {{
      color: var(--accent);
    }}
    .hero {{
      padding: 4rem 0 2rem;
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      margin-bottom: 0.9rem;
    }}
    h1 {{
      margin: 0;
      font-family: "Epilogue", sans-serif;
      font-size: clamp(2.3rem, 5vw, 4.6rem);
      line-height: 0.98;
      letter-spacing: -0.05em;
    }}
    .intro {{
      margin-top: 1rem;
      max-width: 780px;
      color: var(--muted);
      font-size: 1.05rem;
      line-height: 1.75;
    }}
    .bullet-box {{
      margin-top: 1.5rem;
      padding: 1.1rem 1.2rem;
      border: 1px solid rgba(125, 219, 132, 0.16);
      border-radius: 18px;
      background: var(--surface-strong);
      max-width: 900px;
    }}
    .bullet-box ul {{
      margin: 0;
      padding-left: 1.1rem;
      color: var(--text);
    }}
    .bullet-box li {{
      margin: 0.45rem 0;
      line-height: 1.65;
    }}
    .section {{
      margin-top: 1.75rem;
      padding: 1.25rem;
      border: 1px solid rgba(63, 73, 62, 0.58);
      border-radius: 20px;
      background: var(--surface);
      backdrop-filter: blur(14px);
    }}
    .section h2 {{
      margin: 0 0 0.85rem;
      font-family: "Epilogue", sans-serif;
      font-size: 1.45rem;
      letter-spacing: -0.03em;
    }}
    .section p {{
      margin: 0 0 1rem;
      color: var(--muted);
      line-height: 1.75;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 1rem;
    }}
    .card {{
      display: block;
      padding: 1rem;
      border: 1px solid rgba(63, 73, 62, 0.62);
      border-radius: 16px;
      text-decoration: none;
      background: rgba(17, 20, 18, 0.9);
      transition: transform 0.14s ease, border-color 0.14s ease, background 0.14s ease;
    }}
    .card:hover,
    .card:focus-visible {{
      transform: translateY(-2px);
      border-color: rgba(125, 219, 132, 0.44);
      background: rgba(29, 32, 30, 0.96);
    }}
    .card-meta {{
      color: var(--accent);
      font-size: 0.74rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 0.75rem;
    }}
    .card h3 {{
      margin: 0 0 0.55rem;
      font-size: 1.05rem;
      line-height: 1.25;
    }}
    .card p {{
      margin: 0;
      color: var(--muted);
      font-size: 0.93rem;
      line-height: 1.6;
    }}
    .pill-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-top: 1rem;
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 2.45rem;
      padding: 0 0.95rem;
      border-radius: 999px;
      text-decoration: none;
      color: var(--accent);
      border: 1px solid rgba(125, 219, 132, 0.28);
      background: var(--accent-soft);
      font-size: 0.82rem;
      font-weight: 700;
    }}
    .meta-note {{
      color: var(--muted);
      font-size: 0.9rem;
      line-height: 1.65;
    }}
    footer {{
      margin-top: 3rem;
      border-top: 1px solid rgba(63, 73, 62, 0.45);
      padding: 1.3rem 0 2.4rem;
    }}
    .footer-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      align-items: center;
      justify-content: space-between;
    }}
    .footer-links nav {{
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
    }}
    .footer-links a {{
      color: var(--muted);
      text-decoration: none;
      font-size: 0.88rem;
    }}
    .footer-links a:hover,
    .footer-links a:focus-visible {{
      color: var(--accent);
    }}
    @media (max-width: 720px) {{
      .hero {{
        padding-top: 2.8rem;
      }}
      .nav-inner,
      .footer-links {{
        align-items: flex-start;
        flex-direction: column;
      }}
    }}
  </style>
  <script type="application/ld+json">
{jsonld}
  </script>
</head>
<body class="{body_class}">
  <nav class="nav">
    <div class="wrap nav-inner">
      <a class="brand" href="{BASE_URL}/">South Fork Apps</a>
      <div class="nav-links">
        <a href="{BASE_URL}/">Home</a>
        <a href="{BASE_URL}/categories/">Categories</a>
        <a href="{BASE_URL}/topics/">Topics</a>
        <a href="https://blog.southforkapps.com" target="_blank" rel="noopener">Field Notes</a>
      </div>
    </div>
  </nav>
  <main class="wrap">
    <section class="hero">
      <div class="eyebrow">{html.escape(eyebrow)}</div>
      <h1>{html.escape(heading)}</h1>
      <p class="intro">{html.escape(intro)}</p>
      <div class="bullet-box">
        <ul>
{bullets_html}
        </ul>
      </div>
    </section>
{main_html}
  </main>
  <footer>
    <div class="wrap footer-links">
      <div class="meta-note">Practical browser tools built by Tucker Chastain.</div>
      <nav>
        <a href="{BASE_URL}/about/">About</a>
        <a href="{BASE_URL}/privacy/">Privacy</a>
        <a href="{BASE_URL}/contact/">Contact</a>
        <a href="{BASE_URL}/">App Library</a>
      </nav>
    </div>
  </footer>
</body>
</html>
"""


def render_category_page(category: str, apps: list[dict[str, str]]) -> str:
    info = CATEGORY_INFO[category]
    featured = apps[:6]
    related = "\n".join(pill_link(topic_url(slug), TOPIC_INFO[slug]["title"]) for slug in info["related_topics"])
    cards = "\n".join(card_markup(app) for app in apps)
    featured_cards = "\n".join(card_markup(app) for app in featured)
    main_html = f"""    <section class="section">
      <h2>Featured picks in {html.escape(info['title'])}</h2>
      <p>Start with the higher-interest tools below, then browse the full category list if you need a narrower utility.</p>
      <div class="grid">
{featured_cards}
      </div>
    </section>
    <section class="section">
      <h2>Related topic hubs</h2>
      <p>These hubs collect nearby tools by job to be done instead of by internal category.</p>
      <div class="pill-row">
{related}
      </div>
    </section>
    <section class="section">
      <h2>All {html.escape(info['title'])} apps</h2>
      <p>{len(apps)} apps currently live in this category.</p>
      <div class="grid">
{cards}
      </div>
    </section>"""
    canonical = category_url(category)
    image = app_url(featured[0]["slug"]) + "share.jpg" if featured else None
    return page_shell(
        title=info["title"],
        description=info["description"],
        canonical=canonical,
        body_class="category-page",
        eyebrow="Category",
        heading=info["title"],
        intro=info["intro"],
        bullets=info["bullets"],
        main_html=main_html,
        image=image,
    )


def render_topic_page(slug: str, app_lookup: dict[str, dict[str, str]]) -> str:
    info = TOPIC_INFO[slug]
    apps = [app_lookup[item] for item in info["apps"] if item in app_lookup]
    category_links = []
    seen = set()
    for app in apps:
      category = app["category"]
      if category not in seen:
          seen.add(category)
          category_links.append(pill_link(category_url(category), category))
    cards = "\n".join(card_markup(app) for app in apps)
    main_html = f"""    <section class="section">
      <h2>Best tools for this workflow</h2>
      <p>These pages solve the most common jobs inside this topic, from quick checks to copy-ready output.</p>
      <div class="grid">
{cards}
      </div>
    </section>
    <section class="section">
      <h2>Browse the related categories</h2>
      <p>If you want the wider library around this topic, these category pages are the next stop.</p>
      <div class="pill-row">
{''.join(category_links)}
      </div>
    </section>"""
    canonical = topic_url(slug)
    image = app_url(apps[0]["slug"]) + "share.jpg" if apps else None
    return page_shell(
        title=info["title"],
        description=info["description"],
        canonical=canonical,
        body_class="topic-page",
        eyebrow="Topic Hub",
        heading=info["title"],
        intro=info["intro"],
        bullets=info["bullets"],
        main_html=main_html,
        image=image,
    )


def render_simple_page(*, slug: str, title: str, description: str, eyebrow: str, intro: str, bullets: list[str], sections: list[tuple[str, str]]) -> str:
    main_chunks = []
    for heading, content in sections:
        main_chunks.append(
            f"""    <section class="section">
      <h2>{html.escape(heading)}</h2>
      <p>{content}</p>
    </section>"""
        )
    return page_shell(
        title=title,
        description=description,
        canonical=f"{BASE_URL}/{slug}/",
        body_class="trust-page",
        eyebrow=eyebrow,
        heading=title,
        intro=intro,
        bullets=bullets,
        main_html="\n".join(main_chunks),
        jsonld_type="WebPage",
    )


def render_overview_page(*, slug: str, title: str, description: str, eyebrow: str, intro: str, bullets: list[str], cards: list[tuple[str, str, str]]) -> str:
    cards_html = "\n".join(
        f"""<a class="card" href="{href}">
  <div class="card-meta">{html.escape(meta)}</div>
  <h3>{html.escape(card_title)}</h3>
  <p>{html.escape(card_description)}</p>
</a>"""
        for href, meta, card_title, card_description in cards
    )
    main_html = f"""    <section class="section">
      <h2>Browse all {html.escape(title.lower())}</h2>
      <p>Pick the lane that best matches the job you are trying to finish.</p>
      <div class="grid">
{cards_html}
      </div>
    </section>"""
    return page_shell(
        title=title,
        description=description,
        canonical=f"{BASE_URL}/{slug}/",
        body_class="overview-page",
        eyebrow=eyebrow,
        heading=title,
        intro=intro,
        bullets=bullets,
        main_html=main_html,
        jsonld_type="CollectionPage",
    )


def write_page(path: Path, html_text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")
    print(f"WROTE {path.relative_to(ROOT)}")


def main() -> None:
    apps = app_cards_from_homepage()
    app_lookup = {app["slug"]: app for app in apps}

    apps_by_category: dict[str, list[dict[str, str]]] = {name: [] for name in CATEGORY_INFO}
    for app in apps:
        apps_by_category[app["category"]].append(app)

    for category, items in apps_by_category.items():
        items.sort(key=lambda app: app["title"].lower())
        path = ROOT / "categories" / CATEGORY_INFO[category]["slug"] / "index.html"
        write_page(path, render_category_page(category, items))

    category_cards = [
        (
            category_url(name),
            "Category",
            info["title"],
            info["description"],
        )
        for name, info in CATEGORY_INFO.items()
    ]
    write_page(
        ROOT / "categories" / "index.html",
        render_overview_page(
            slug="categories",
            title="Categories",
            description="Browse South Fork Apps by category, including everyday tools, text tools, developer utilities, design helpers, planning apps, and fun tools.",
            eyebrow="Browse",
            intro="South Fork Apps groups the library into broad lanes so you can jump into the right part of the toolset faster.",
            bullets=[
                "Each category page collects a full slice of the library.",
                "Useful when you know the kind of tool you need but not the exact app.",
                "A better entry point than searching blind through the full catalog.",
            ],
            cards=category_cards,
        ),
    )

    for slug in TOPIC_INFO:
        path = ROOT / "topics" / slug / "index.html"
        write_page(path, render_topic_page(slug, app_lookup))

    topic_cards = [
        (
            topic_url(slug),
            "Topic Hub",
            info["title"],
            info["description"],
        )
        for slug, info in TOPIC_INFO.items()
    ]
    write_page(
        ROOT / "topics" / "index.html",
        render_overview_page(
            slug="topics",
            title="Topics",
            description="Browse South Fork Apps by workflow topics such as text tools, developer tools, calculators, CSS and color helpers, generators, and time tools.",
            eyebrow="Browse",
            intro="Topic hubs group apps by the job you are trying to finish, not just by the internal category they happen to live in.",
            bullets=[
                "Good when your task spans more than one category.",
                "Helps you compare nearby tools that solve the same kind of problem.",
                "Adds stronger static paths into the library for both users and search engines.",
            ],
            cards=topic_cards,
        ),
    )

    write_page(
        ROOT / "about" / "index.html",
        render_simple_page(
            slug="about",
            title="About South Fork Apps",
            description="About South Fork Apps, the browser-based library of practical tools built by Tucker Chastain.",
            eyebrow="About",
            intro="South Fork Apps is a growing library of browser-based tools built for practical jobs: writing cleanup, developer chores, quick calculators, design checks, and the odd weird utility that ends up being genuinely useful.",
            bullets=[
                "Built by Tucker Chastain and published as a public tool library.",
                "Focused on small jobs that should not require a signup or heavy app.",
                "Organized around practical use, not trend-chasing feature lists.",
            ],
            sections=[
                ("What the site is for", "Most pages on South Fork Apps exist to solve one concrete problem fast. The goal is not to keep you browsing forever. The goal is to help you finish the task and move on."),
                ("How tools get added", "New apps usually start as repeat annoyances, missing utilities, or workflow chores that deserve a faster browser-first answer. The collection spans text, code, design, planning, and everyday use cases because real work is messy and does not stay in one lane."),
                ("Where to follow updates", 'Field Notes at <a href="https://blog.southforkapps.com" target="_blank" rel="noopener">blog.southforkapps.com</a> is the best place to track new releases, updates, and related thinking around the library.'),
            ],
        ),
    )

    write_page(
        ROOT / "privacy" / "index.html",
        render_simple_page(
            slug="privacy",
            title="Privacy",
            description="Privacy information for South Fork Apps and how browser-based tools on the site handle data.",
            eyebrow="Privacy",
            intro="South Fork Apps is designed to keep tool use lightweight. Many tools run entirely in the browser, and the site does not require user accounts for the public app library.",
            bullets=[
                "No user account is required to use the public tools.",
                "Many tools process input directly in the browser.",
                "Some pages may use third-party services such as hosting or advertising infrastructure.",
            ],
            sections=[
                ("Tool inputs", "Many South Fork Apps tools process what you type directly on the page. Some specialized tools may call a third-party service to complete a task. When that happens, the tool should make that dependency clear in its interface."),
                ("Site infrastructure", "Like most public websites, South Fork Apps may rely on standard hosting, CDN, security, and ad infrastructure that can log normal request data such as IP address, browser details, referral data, and performance diagnostics."),
                ("Practical rule of thumb", "If you are working with sensitive personal, financial, medical, legal, or company-confidential information, do not paste it into any public web tool unless you understand exactly how that specific tool works and what services it depends on."),
            ],
        ),
    )

    write_page(
        ROOT / "contact" / "index.html",
        render_simple_page(
            slug="contact",
            title="Contact",
            description="How to report issues, suggest apps, or follow South Fork Apps updates.",
            eyebrow="Contact",
            intro="If a tool breaks, misses an obvious feature, or there is a practical app you want added to South Fork Apps, use one of the channels below.",
            bullets=[
                "Best for bug reports, feature requests, and new app ideas.",
                "Use public channels where possible so the request has context.",
                "Field Notes is the easiest way to follow what changes next.",
            ],
            sections=[
                ("GitHub", 'The public repository lives at <a href="https://github.com/tchastain26/south-fork-apps" target="_blank" rel="noopener">github.com/tchastain26/south-fork-apps</a>. That is the best place for concrete bug reports and implementation-level feedback.'),
                ("Field Notes", 'Project updates and writing around the library live at <a href="https://blog.southforkapps.com" target="_blank" rel="noopener">blog.southforkapps.com</a>.'),
                ("Broader web presence", 'For the person behind the project, visit <a href="https://tuckerchastain.com" target="_blank" rel="noopener">tuckerchastain.com</a>.'),
            ],
        ),
    )


if __name__ == "__main__":
    main()
