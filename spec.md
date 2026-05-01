# South Fork Apps — Weekend Run Spec

## Goal

Build 10 new single-file web apps for the South Fork Apps collection. Each app should be genuinely useful, polished, and ready to add to southforkapps.com.

## Output Location

Each app goes in its own folder:
```
/77_South Fork Apps/South Fork Apps Collection/[app-name]/
```

Two files per app:
- `index.html` — the app
- `[App Name] Notes.md` — companion doc

## HTML Requirements

Every index.html must:

1. Be a single self-contained file (inline CSS + JS, no external dependencies)
2. Use this exact color theme:
   - Background: `#111412`
   - Accent / primary color: `#7ddb84`
   - Text: `#e8e8e8`
   - Secondary surface: `#1a1f1b`
   - Border: `#2a2f2b`
3. Load Plus Jakarta Sans from Google Fonts:
   ```html
   <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
   ```
4. Include this nav bar at the top of `<body>`:
   ```html
   <nav class="nav">
     <a href="https://southforkapps.com" class="nav-back">← South Fork Apps</a>
     <span class="nav-title">[App Name]</span>
   </nav>
   ```
5. Nav CSS (use exactly):
   ```css
   .nav {
     display: flex;
     align-items: center;
     gap: 1rem;
     padding: 0.75rem 1.5rem;
     background: #1a1f1b;
     border-bottom: 1px solid #2a2f2b;
     font-family: 'Plus Jakarta Sans', sans-serif;
   }
   .nav-back {
     color: #7ddb84;
     text-decoration: none;
     font-size: 0.875rem;
     font-weight: 500;
   }
   .nav-back:hover { text-decoration: underline; }
   .nav-title {
     color: #e8e8e8;
     font-size: 0.875rem;
     font-weight: 600;
   }
   ```
6. Be mobile-friendly (responsive, relative units, simple flex/grid layout)
7. Version badge in the footer: `v1.0`

## Notes.md Format

```
# [App Name] Notes

Created: 2026.04.19
Status: Done

## What It Does

[One-paragraph description]

## How to Use

[Brief usage instructions]

## Changelog

- 2026.04.19 — Initial build (weekend run)
```

## Verification

After building each app, confirm:
- [ ] Folder exists at correct path
- [ ] index.html opens without errors
- [ ] Nav bar present with correct link and app name
- [ ] Theme colors applied (#111412 bg, #7ddb84 accent)
- [ ] Notes.md exists with correct format
- [ ] App is functional (core feature works)

Run `tests/validate.sh [app-folder-name]` after each app.

## Out of Scope

- Do NOT add the app to southforkapps.com index.html (Tucker does that manually)
- Do NOT use frameworks (React, Vue, etc.)
- Do NOT use external CDN libraries unless the app genuinely cannot work without one (note it if so)
- Do NOT create more than 10 apps (stick to todo.md list)
- Do NOT modify any existing app files
