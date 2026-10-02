/* Scoped, atomic offline shell. A new version waits for an explicit reload. */
const PREFIX = 'poop-tracker-';
const CACHE = 'poop-tracker-v3-2026.10.02-review2';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './favicon.svg', './apple-touch-icon.png'];
const scope = new URL('./', self.location.href);
const shellURL = new URL('./index.html', scope).href;

self.addEventListener('install', event => {
  // Reject partial installs. Keep the last working worker if any asset fails.
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS.map(asset => new Request(new URL(asset, scope), {cache:'reload'})))));
});
self.addEventListener('message', event => {
  if (event.data?.type === 'ACTIVATE_UPDATE') self.skipWaiting();
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(
    keys.filter(key => key.startsWith(PREFIX) && key !== CACHE).map(key => caches.delete(key))
  )).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== scope.origin || !url.pathname.startsWith(scope.pathname)) return;
  if (req.mode === 'navigate') {
    // Match only this app's entry page, including query strings. An active worker
    // serves its matching shell until the waiting update is accepted.
    if (url.pathname !== scope.pathname && url.pathname !== new URL(shellURL).pathname) return;
    event.respondWith(caches.open(CACHE).then(async cache => (await cache.match(shellURL)) || fetch(req)));
    return;
  }
  if (!ASSETS.some(asset => new URL(asset, scope).pathname === url.pathname)) return;
  event.respondWith(caches.open(CACHE).then(async cache => (await cache.match(req, {ignoreSearch:true})) || fetch(req)));
});
