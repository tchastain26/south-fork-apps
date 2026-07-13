/* Dog Poop Tracker service worker.
   Network-first for the page itself (so updates land), cache-first for assets.
   Bump CACHE on every deploy that changes index.html. */
const CACHE = 'poop-tracker-v3-1';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './favicon.svg', './apple-touch-icon.png'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(cache =>
      Promise.allSettled(ASSETS.map(a => cache.add(a)))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return; // never intercept cross-origin (fonts, etc.)

  if (req.mode === 'navigate' || url.pathname.endsWith('/index.html')) {
    event.respondWith(
      fetch(req)
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE).then(cache => cache.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then(hit => hit || caches.match('./index.html')))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(cache => cache.put(req, copy));
      return res;
    }))
  );
});
