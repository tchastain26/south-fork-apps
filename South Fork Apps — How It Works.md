# South Fork Apps — How It Works

Last updated: 2026.04.15

## The Short Version

The `77_South Fork Apps` folder **is** the Git repo. Everything here gets pushed to GitHub and auto-deployed to Cloudflare Pages. To add a new app: build it, add a card to the directory, commit, push. Done.

---

## Folder Layout

```
77_South Fork Apps/
├── index.html                        ← The southforkapps.com landing page (the directory)
├── README.md                         ← GitHub-facing repo description
├── South Fork Apps Collection/       ← Each app lives in its own subfolder here
│   ├── hex-code-color-generator/
│   │   └── index.html
│   └── temperature-converter/
│       └── index.html
└── .git/                             ← Git repo (do not touch)
```

---

## How Deployment Works

1. This folder is a Git repo connected to: `https://github.com/tchastain26/south-fork-apps`
2. Cloudflare Pages watches the `main` branch
3. Every push to `main` auto-deploys the whole folder to southforkapps.com
4. No build step. No CI. Static files only.

**Domain chain:** Hover (registrar) → Cloudflare nameservers → Cloudflare Pages → southforkapps.com

**Blog:** blog.southforkapps.com is a CNAME in Cloudflare pointing to Micro.blog. Managed separately.

---

## App URLs

Apps in `South Fork Apps Collection` are served as subpaths. A folder named `hex-code-color-generator` is live at:

```
southforkapps.com/South Fork Apps Collection/hex-code-color-generator/
```

Note the space in the folder name gets URL-encoded, which is ugly. If this is a problem, rename the subfolder to something without spaces (e.g. `apps/`). For now it works.

---

## Adding a New App

### Step 1 — Build the app

Create a folder under `South Fork Apps Collection/`:

```
South Fork Apps Collection/
└── your-app-name/
    └── index.html
```

Single `index.html` with inline CSS and JS. No build tools, no frameworks. See the skill file at `/90_Robot/Skills/south-fork-app.md` for the full build template.

### Step 2 — Add it to the directory

Open `index.html` at the root of `77_South Fork Apps`. Find the apps section (look for the Dog Poop Tracker card). Duplicate a card and update:
- App name
- Description
- Link — point it to the Cloudflare Pages subpath or an external URL if hosted elsewhere (e.g. Netlify)

### Step 3 — Commit and push

From Terminal, navigate to `77_South Fork Apps` and run:

```bash
cd "/Users/tuckerchastain/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tucker Chastain/77_South Fork Apps"
git add .
git commit -m "Add [App Name]"
git push origin main
```

Cloudflare deploys within a minute or two. Check southforkapps.com to confirm.

---

## Current Apps

| App | Location | Hosted At |
|---|---|---|
| Dog Poop Tracker | South Fork Apps Collection/dog-poop-tracker/ | dogpooptracker.netlify.app |
| Hex Code Color Generator | South Fork Apps Collection/hex-code-color-generator/ | hex-color-picker-26.netlify.app |
| Temperature Converter | South Fork Apps Collection/temperature-converter/ | temperature-converter-26.netlify.app |

---

## Key Accounts

| Service | Purpose | Login |
|---|---|---|
| GitHub | Source repo | github.com/tchastain26 |
| Cloudflare | DNS + Pages hosting | cloudflare.com |
| Hover | Domain registrar for southforkapps.com | hover.com |
| Micro.blog | blog.southforkapps.com | micro.blog |

---

## Notes

- The vault copy in `77_South Fork Apps` and the GitHub repo are the same thing. Changes made here need to be committed and pushed — they don't sync automatically.
- Never delete files from this folder via Obsidian without also handling it in Git.
- The `.git` folder and `.gitignore` are hidden — ignore them.
- App notes/docs for Cog live in the vault at `/90_Robot/Skills/south-fork-app.md`, not in this folder.
