# Tailwind Static Build Plan

Created: 2026.08.25
Source: 2026.07.06 security review, South Fork Apps finding #2 ("Replace Tailwind Play CDN with built static CSS").
Status: PLAN ONLY. Nothing in this file has been executed.

## Why this matters

`index.html` line 23 loads the Tailwind **Play CDN**:

    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>

Three problems, in order of how much they actually matter:

1. **Third-party script on every homepage load.** It is a remote, versionless script with full DOM access. If `cdn.tailwindcss.com` is ever compromised or hijacked, it executes on southforkapps.com. This is the security finding.
2. **It forces `'unsafe-inline'` and a CDN allowance in the CSP.** The new `_headers` CSP has to whitelist `https://cdn.tailwindcss.com` in `script-src`. Removing the CDN removes one whitelisted origin and is a prerequisite for ever making the CSP enforcing rather than report-only.
3. **Performance.** The Play CDN ships a full JIT compiler to the browser and generates CSS at runtime, on every visit. Tailwind's own docs say it is not for production.

## Scope (smaller than it looks)

Only **one** file uses Tailwind: `index.html`. The 250 app pages in `South Fork Apps Collection/` do not.

Measured 2026.08.25:
- 197 unique classes in `index.html`
- 47 custom colors in the `tailwind.config` block (a Material-style dark palette from the original Google Stitch mock)
- 2 plugins: `forms`, `container-queries`
- `darkMode: "class"`

Estimated built CSS: roughly 10-20 KB before gzip. That is small enough to inline into `<style>` and skip a separate request entirely.

## Steps

1. Create `tailwind/` in the repo root with `package.json`, `tailwind.config.js`, and `src.css`.
2. Move the inline `tailwind.config` object (currently `<script id="tailwind-config">`, 2,298 chars) into `tailwind.config.js` verbatim. Set `content: ["../index.html"]`.
3. `src.css` is the standard three lines: `@tailwind base; @tailwind components; @tailwind utilities;`
4. Install `tailwindcss`, `@tailwindcss/forms`, `@tailwindcss/container-queries` as devDependencies. Register both plugins in the config.
5. Build minified: `npx tailwindcss -i src.css -o ../assets/tailwind.css --minify`
6. In `index.html`: delete the CDN `<script>` (line 23) and the `<script id="tailwind-config">` block; add `<link rel="stylesheet" href="/assets/tailwind.css">`.
7. Diff the rendered homepage against the current live one before and after. The dark palette and the asymmetric card grid are the two things most likely to regress.
8. Once verified, drop `https://cdn.tailwindcss.com` from `script-src` in `_headers`.

## Risks

- **Dynamically generated class names.** The homepage builds app cards in JS. Tailwind's content scanner only sees classes that appear as complete literal strings. Any class assembled at runtime (`"bg-" + color`) will be purged and silently break. Grep the card-rendering JS for string concatenation into `class` before building, and use a `safelist` for anything found.
- **`build_hub_pages.py` and `seo_update.py` rewrite `index.html`.** Confirm neither script re-injects the CDN tag, or the change will be reverted on the next build.
- **Adds a build step to a site that currently has none for CSS.** The `tailwind/` folder and `node_modules` must be gitignored, and `assets/tailwind.css` must be committed as a build artifact.

## Recommendation

Do this as its own focused session, not bolted onto other work. It is a contained change (one file, one build step) but step 7 needs real visual comparison, and the failure mode in the first risk above is silent.
