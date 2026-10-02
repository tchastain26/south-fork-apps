# Dog Poop Tracker

A lightweight, local-first yard tracker. Set up a simple map or capture four GPS corners, mark a spot, correct its position, and mark it cleaned.

## Source and hosting

- Source: `tools/dog-poop-tracker/` in the `tchastain26/south-fork-apps` Git repository.
- Mac mini checkout: `~/Sites/south-fork-apps`.
- Live URL: https://southforkapps.com/tools/dog-poop-tracker/
- Hosting: Cloudflare Pages, Git integration on `main`.
- The former Netlify deployment and vault source paths are obsolete.
- Static HTML/CSS/JavaScript plus `sw.js` and `manifest.webmanifest`. No framework or backend.

## 2026.10.02 v2.1 release

Tucker approved the v2.1 release on 2026.10.02. Developed and tested on `codex/dog-poop-tracker-review`, based on `27644cf`. Production deployment uses the existing Cloudflare Pages integration on `main`.

- Added simple yard setup without location permission, a numbered map, phone action bar, readable labels, explicit cleanup, Undo, and keyboard placement/correction.
- Preserved the filtered GPS engine, quadrilateral mapping, hold-still corner capture, grid snapping, corrections, and v2-to-v3 migration. The legacy storage key stays intact.
- Limited tracking samples to six seconds; kept the device accuracy as the uncertainty floor; rejected duplicate timestamps and degenerate geometry. Known corner error is included in uncapped uncertainty ellipses. Unknown legacy accuracy is labeled rather than invented.
- Validated backups before replacement. Import preserves a recovery copy. Storage failures and cross-tab conflicts are visible. Corrupt stored data stays untouched and can be exported.
- Scoped service-worker cleanup to this app, made shell installation atomic, bypassed stale HTTP cache on install, and added explicit update activation. New workers wait for Save & reload. Production verification found Cloudflare's canonical index.html redirect; navigation now serves the non-redirected directory response, and installation repairs the briefly released worker's cache without forcing activation. The browser server reproduces that redirect and tests recovery. A narrow `_headers` exception keeps the tracker service worker out of the site's one-year immutable JavaScript cache; refresh this URL in Cloudflare when releasing the exception.
- Location collection starts when requested or when opening an already calibrated yard, and pauses while hidden. The app does not upload yard locations. Browser storage and exported backups are plaintext. The shared South Fork origin and external Google Fonts remain existing architectural constraints.

## Checks

With Node 20 or newer and the repository dependencies installed:

```sh
npm run test:dog-poop-tracker
bash tests/validate.sh dog-poop-tracker
```

The unit suite covers geometry, filtering, migration and backup validation. The browser suite starts its own loopback server and isolated Chromium/WebKit contexts with synthetic GPS. It covers daily use, corner capture, backup handling, storage failure, responsive themes, offline use, update activation and failed-install recovery. Screenshots and results are written to the ignored `artifacts/dog-poop-tracker/` directory. Install browser binaries with the Playwright CLI if needed.

Real iPhone GPS, sunlight readability, VoiceOver, lock/resume, Home Screen installation, and actual yard cleanup still require a field check. A local Mac loopback URL is not an iPhone HTTPS test route.

## Release note

Bump the service-worker cache name whenever the application shell changes. Keep the existing storage keys. Never deploy a release before approval; pushing `main` deploys the site.
