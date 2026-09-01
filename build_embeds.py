#!/usr/bin/env python3
"""Generate embeddable versions of selected tools at /embed/<slug>/.

Why this exists: the site's own search traffic is negligible, but the tools
themselves are worth hosting on other people's pages. Every embed places a real
anchor to southforkapps.com in the host's own HTML, which is the one SEO
deficiency the site cannot fix from the inside.

Three rules the generator enforces, each for a concrete reason:
  * noindex on every embed. They duplicate the tool pages, and ads_update.py
    already refuses to place ads on a noindex page, which is what keeps us on
    the right side of the AdSense policy against serving ads inside a frame on
    a site we do not control.
  * only stateless tools. Anything storing personal data, reading location, or
    taking an API key is excluded by the allowlist below, not by accident.
  * the attribution anchor lives in the SNIPPET, not in the iframe. A link
    inside a frame passes no authority to the host page; Google treats framed
    content as a separate document.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOLS = ROOT / "tools"
OUT = ROOT / "embed"
BASE_URL = "https://southforkapps.com"

# Deliberate allowlist. Finance first: those pages already pull 9.6% of the
# site's impressions from 5% of the catalog, and mortgage brokers, lenders and
# advisers are exactly the people who put a calculator on their own site.
EMBEDDABLE = [
    ("mortgage-calculator",   "Mortgage Calculator"),
    ("loan-calculator",       "Loan Calculator"),
    ("loan-comparison",       "Loan Comparison"),
    ("compound-interest",     "Compound Interest Calculator"),
    ("debt-snowball",         "Debt Snowball Calculator"),
    ("savings-goal-planner",  "Savings Goal Planner"),
    ("roi-calculator",        "ROI Calculator"),
    ("break-even-calculator", "Break-Even Calculator"),
    ("inflation-calculator",  "Inflation Calculator"),
    ("rule-of-72",            "Rule of 72"),
    ("percentage-calculator", "Percentage Calculator"),
    ("tip-calculator",        "Tip Calculator"),
    ("unit-converter",        "Unit Converter"),
    ("aspect-ratio-calculator", "Aspect Ratio Calculator"),
    ("pace-calculator",       "Pace Calculator"),
]

DEFAULT_HEIGHT = 620

RESIZER = """
<script>
// Tell the host page how tall we are, so the snippet's listener can size the
// frame. Hosts that strip the listener still get the fixed fallback height.
(function () {
  var last = 0;
  function post() {
    var h = Math.ceil(document.documentElement.scrollHeight);
    if (h && h !== last) {
      last = h;
      parent.postMessage({ sfaEmbed: true, slug: SFA_SLUG, height: h }, "*");
    }
  }
  window.addEventListener("load", post);
  if (window.ResizeObserver) new ResizeObserver(post).observe(document.documentElement);
  setInterval(post, 1000);
})();
</script>
"""


def strip_marked(text: str, marker: str) -> str:
    return re.sub(
        rf"\n?(?:<!--|/\*)\s*{re.escape(marker)}_START\s*(?:-->|\*/).*?(?:<!--|/\*)\s*{re.escape(marker)}_END\s*(?:-->|\*/)\n?",
        "\n", text, flags=re.S,
    )


def build_one(slug: str, title: str) -> str | None:
    src = TOOLS / slug / "index.html"
    if not src.exists():
        return None
    s = src.read_text(encoding="utf-8")
    for m in ("SFA_FEATURE", "SFA_RELATED", "SFA_ADS", "SFA_JSONLD", "SFA_BREADCRUMB", "SFA_SOCIAL", "SFA_DISCOVERY"):
        s = strip_marked(s, m)

    styles = "\n".join(m.group(0) for m in re.finditer(r"(?is)<style[^>]*>.*?</style>", s))
    fonts = "\n".join(m.group(0) for m in re.finditer(r'<link[^>]+fonts\.googleapis\.com[^>]*>', s))

    body_m = re.search(r"(?is)<main\b[^>]*>(.*?)</main>", s)
    if body_m:
        tool = body_m.group(1)
    else:
        # Some tools have no <main>: they open with <nav> or <header> and then
        # put the interface straight in <body>. Take everything after that
        # chrome, minus the footer and any trailing scripts.
        b = s[s.index("<body"):]
        b = b[b.index(">") + 1:]
        for close in ("</nav>", "</header>"):
            i = b.lower().find(close)
            if i != -1:
                b = b[i + len(close):]
        b = re.sub(r"(?is)<footer\b.*?</footer>", "", b)
        b = re.sub(r"(?is)<script.*?</script>", "", b)
        b = re.sub(r"(?is)</body>.*", "", b)
        tool = b.strip()
        if not tool:
            return None

    body_all = s[s.index("<body"):]
    scripts = "\n".join(
        m.group(0) for m in re.finditer(r"(?is)<script(?![^>]*\bsrc=)(?![^>]*ld\+json)[^>]*>.*?</script>", body_all)
    )
    ext = "\n".join(
        m.group(0) for m in re.finditer(r'(?is)<script[^>]*\bsrc="https://(?:cdnjs|cdn\.jsdelivr)[^"]*"[^>]*></script>', s)
    )

    tool_url = f"{BASE_URL}/tools/{slug}/"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} (embed) | South Fork Apps</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{tool_url}">
{fonts}
{styles}
<style>
  body{{margin:0;padding:0;background:#111412;}}
  main{{padding:1rem;}}
  .sfa-embed-credit{{
    display:flex;justify-content:flex-end;padding:.5rem 1rem 1rem;
    font:500 .72rem/1.4 'Plus Jakarta Sans',system-ui,sans-serif;
  }}
  .sfa-embed-credit a{{color:#7ddb84;text-decoration:none;opacity:.85;}}
  .sfa-embed-credit a:hover{{opacity:1;text-decoration:underline;}}
</style>
</head>
<body>
<main>{tool}</main>
<div class="sfa-embed-credit">
  <a href="{tool_url}?utm_source=embed" target="_blank" rel="noopener">{html.escape(title)} by South Fork Apps</a>
</div>
{ext}
{scripts}
<script>var SFA_SLUG = {slug!r};</script>
{RESIZER}
</body>
</html>
"""



GALLERY_CSS = """
:root{--bg:#111412;--surface:#1d201e;--surface2:#191c1a;--border:#3f493e;--accent:#7ddb84;--text:#e1e3df;--muted:#aab5ac;}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--text);font-family:'Plus Jakarta Sans',system-ui,sans-serif;line-height:1.6;}
a{color:var(--accent);}
.nav{position:sticky;top:0;z-index:10;background:rgba(11,18,14,.85);backdrop-filter:blur(14px);border-bottom:1px solid rgba(63,73,62,.5);}
.nav-in{max-width:1080px;margin:0 auto;padding:1rem;display:flex;gap:1rem;align-items:center;}
.brand{font-weight:800;color:var(--accent);text-decoration:none;}
.wrap{max-width:1080px;margin:0 auto;padding:2rem 1rem 4rem;}
h1{font-size:clamp(1.9rem,4vw,2.9rem);line-height:1.1;margin:.2rem 0 .6rem;}
.lede{color:var(--muted);max-width:62ch;}
h2{margin:2.5rem 0 .6rem;font-size:1.3rem;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,220px),1fr));gap:.6rem;margin:1rem 0 0;}
.pick{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:.7rem .85rem;color:var(--text);
  font:600 .9rem/1.3 inherit;text-align:left;cursor:pointer;transition:border-color .15s,background .15s;}
.pick:hover{border-color:var(--accent);}
.pick[aria-pressed="true"]{border-color:var(--accent);background:rgba(125,219,132,.12);color:var(--accent);}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1rem;margin-top:1rem;}
.row{display:flex;gap:1rem;flex-wrap:wrap;align-items:center;margin-bottom:.8rem;}
label{font-size:.82rem;color:var(--muted);display:flex;gap:.4rem;align-items:center;}
input[type=number]{width:90px;background:var(--surface2);border:1px solid var(--border);color:var(--text);
  border-radius:8px;padding:.35rem .5rem;font:inherit;}
pre{background:#0c0f0d;border:1px solid var(--border);border-radius:10px;padding:1rem;overflow-x:auto;
  font:500 .8rem/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;color:#cfe6d2;white-space:pre;margin:0;}
.copy{margin-top:.7rem;background:var(--accent);color:#04210a;border:none;border-radius:9px;
  padding:.6rem 1.1rem;font:800 .85rem inherit;cursor:pointer;}
.copy:hover{filter:brightness(1.08);}
iframe.preview{width:100%;border:1px solid var(--border);border-radius:12px;background:var(--bg);}
.note{color:var(--muted);font-size:.85rem;}
ul{color:var(--muted);}
@media (max-width:640px){.wrap{padding:1.2rem 1rem 3rem;}}
"""


def build_gallery(built: list[tuple[str, str]]) -> str:
    opts = "\n".join(
        f'      <button class="pick" type="button" data-slug="{s}" data-title="{html.escape(t, quote=True)}">{html.escape(t)}</button>'
        for s, t in built
    )
    first_slug, first_title = built[0]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Embed a Free Calculator on Your Site | South Fork Apps</title>
<meta name="description" content="Put a working calculator on your own website for free. Pick a tool, copy one line of HTML, done. No account, no script, no tracking of your visitors.">
<link rel="canonical" href="{BASE_URL}/embed/">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{{CSS}}</style>
</head>
<body>
<nav class="nav"><div class="nav-in"><a class="brand" href="{BASE_URL}/">South Fork Apps</a><span class="note">Embeds</span></div></nav>
<div class="wrap">
  <h1>Put a working calculator on your site</h1>
  <p class="lede">Pick a tool, copy the snippet, paste it into your page. It runs in your visitor's browser,
  needs no account or API key, and collects nothing about the people who use it.</p>

  <h2>1. Pick a tool</h2>
  <div class="grid" id="picker">
{opts}
  </div>

  <h2>2. Copy the snippet</h2>
  <div class="panel">
    <div class="row">
      <label>Height <input type="number" id="h" value="{DEFAULT_HEIGHT}" min="240" max="2000" step="20"></label>
      <label><input type="checkbox" id="auto" checked> Auto-resize to fit content</label>
    </div>
    <pre id="snippet"></pre>
    <button class="copy" id="copyBtn" type="button">Copy snippet</button>
    <p class="note" id="copied" style="display:none">Copied.</p>
  </div>

  <h2>3. Check it looks right</h2>
  <iframe class="preview" id="preview" title="Embed preview" height="{DEFAULT_HEIGHT}"></iframe>

  <h2>Why put a calculator on your page</h2>
  <p class="lede">A visitor who works out their own number stays on the page and leaves with an answer
  instead of a vague impression. For a broker, adviser, agent or contractor that is the difference
  between a page someone reads and a page someone uses.</p>
  <p class="lede">It also gives people a reason to link to you. A page with a working tool on it gets
  referenced by other sites far more often than a page that only describes the same thing in prose.</p>

  <h2>How it works</h2>
  <ul>
    <li>The snippet is one iframe pointing at a page on this site. There is no library to install,
        no build step, and nothing to keep updated.</li>
    <li>The calculation runs entirely in your visitor&#x27;s browser. Nothing they type is transmitted,
        logged or stored, by us or by anyone else, so the widget adds no privacy obligations to your site.</li>
    <li>No cookies are set, and the embed carries no advertising of any kind.</li>
    <li>The optional resize script lets the frame grow to fit its contents so you never get an inner
        scrollbar. Leave it out and the fixed height still works.</li>
    <li>The tools available here are the stateless ones. Anything that stores personal data, reads
        location, or needs an API key is deliberately not offered as an embed.</li>
  </ul>

  <h2>Common questions</h2>
  <h3 style="font-size:1.02rem;margin:1.2rem 0 .2rem">Does it slow my page down?</h3>
  <p class="note">The iframe loads lazily, so it does not block your page rendering and is only fetched
  when the visitor scrolls near it.</p>
  <h3 style="font-size:1.02rem;margin:1.2rem 0 .2rem">Will it match my design?</h3>
  <p class="note">The embeds use this site&#x27;s dark theme as-is. If you need it in your own colours and
  typography, that is what a branded build is for.</p>
  <h3 style="font-size:1.02rem;margin:1.2rem 0 .2rem">What happens if you change the tool?</h3>
  <p class="note">Your embed picks up improvements automatically, because it points at the live page
  rather than a copy. The inputs and outputs of these calculators are stable; the maths behind a
  mortgage payment is not going to change.</p>
  <h3 style="font-size:1.02rem;margin:1.2rem 0 .2rem">Can I remove the attribution?</h3>
  <p class="note">Not on the free embed. A branded build has no attribution, along with your own name,
  colours and figures.</p>

  <h2>The terms, in plain words</h2>
  <ul>
    <li>Free to use on any site, commercial or not.</li>
    <li>Keep the attribution line. It is the only thing asked in return, and it is what pays for the tools staying free.</li>
    <li>Nothing about your visitors is collected, stored or sent anywhere. The calculation happens in their browser.</li>
    <li>Want it in your own colours, with your own name, pricing or rates, and no attribution?
        <a href="{BASE_URL}/tools/detailing-quote-widget/">See how a branded build works</a>.</li>
  </ul>
</div>
<script>
const BASE = {BASE_URL!r};
const picker = document.getElementById('picker');
const snippetEl = document.getElementById('snippet');
const preview = document.getElementById('preview');
const hEl = document.getElementById('h');
const autoEl = document.getElementById('auto');
let slug = {first_slug!r}, title = {first_title!r};

function snippet() {{
  const h = parseInt(hEl.value, 10) || {DEFAULT_HEIGHT};
  const frame = `<iframe src="${{BASE}}/embed/${{slug}}/" title="${{title}}" width="100%" height="${{h}}" `
    + `style="border:1px solid #3f493e;border-radius:12px;max-width:100%" loading="lazy"></iframe>`;
  // The attribution anchor sits in YOUR page, not inside the frame. A link
  // inside an iframe is a separate document and passes nothing to the host.
  const credit = `<p style="font:500 13px system-ui,sans-serif;margin:.5rem 0 0">`
    + `<a href="${{BASE}}/tools/${{slug}}/">${{title}}</a> by <a href="${{BASE}}/">South Fork Apps</a></p>`;
  const resizer = autoEl.checked ? `\n\\x3Cscript>addEventListener("message",function(e){{`
    + `if(e.data&&e.data.sfaEmbed&&e.data.slug==="${{slug}}"){{`
    + `var f=document.querySelector('iframe[src*="/embed/${{slug}}/"]');`
    + `if(f)f.height=e.data.height;}}}});<\/script>` : '';
  return frame + "\\n" + credit + resizer;
}}

function render() {{
  snippetEl.textContent = snippet();
  preview.src = BASE + '/embed/' + slug + '/';
  preview.height = parseInt(hEl.value, 10) || {DEFAULT_HEIGHT};
  for (const b of picker.querySelectorAll('.pick'))
    b.setAttribute('aria-pressed', String(b.dataset.slug === slug));
}}

picker.addEventListener('click', e => {{
  const b = e.target.closest('.pick');
  if (!b) return;
  slug = b.dataset.slug; title = b.dataset.title; render();
}});
hEl.addEventListener('input', render);
autoEl.addEventListener('change', render);
document.getElementById('copyBtn').addEventListener('click', async () => {{
  try {{ await navigator.clipboard.writeText(snippet()); }} catch (err) {{}}
  const n = document.getElementById('copied');
  n.style.display = 'block'; setTimeout(() => n.style.display = 'none', 1800);
}});
addEventListener('message', e => {{
  if (e.data && e.data.sfaEmbed && e.data.slug === slug && autoEl.checked) preview.height = e.data.height;
}});
render();
</script>
</body>
</html>
""".replace("{CSS}", GALLERY_CSS)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    built = []
    for slug, title in EMBEDDABLE:
        page = build_one(slug, title)
        if not page:
            print(f"SKIP {slug}: no <main> or missing source")
            continue
        d = OUT / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page, encoding="utf-8")
        built.append((slug, title))
        print(f"BUILT /embed/{slug}/")
    (OUT / "index.html").write_text(build_gallery(built), encoding="utf-8")
    print("BUILT /embed/ (gallery and snippet builder)")
    print(f"\n{len(built)} embeds generated")


if __name__ == "__main__":
    main()
