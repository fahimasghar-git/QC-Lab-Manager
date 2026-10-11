// QC Lab Manager PWA Service Worker
// Version placeholder dynamically replaced by Django service_worker view
const CACHE_NAME = 'qc-lims-cache-{{APP_VERSION}}';

const CORE_ASSETS = [
  '/',
  '/static/manifest.json',
  '/static/images/icons/icon-144x144.png',
  '/static/images/icons/icon-192x192.png',
  '/static/images/icons/icon-512x512.png',
  '/static/images/icons/apple-touch-icon.png'
];

// 1. Install Event: Pre-cache essential static assets
self.addEventListener('install', (event) => {
  console.log(`[PWA SW] Installing worker version: ${CACHE_NAME}`);
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CORE_ASSETS).catch((err) => {
        console.warn('[PWA SW] Pre-caching partial issue (non-fatal):', err);
      });
    })
  );
  // Do NOT automatically call self.skipWaiting() here so the update prompt can be shown to the user!
});

// 2. Activate Event: Clean up outdated caches
self.addEventListener('activate', (event) => {
  console.log(`[PWA SW] Activating worker version: ${CACHE_NAME}`);
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME && name.startsWith('qc-lims-cache-')) {
            console.log('[PWA SW] Purging old cache:', name);
            return caches.delete(name);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. Message Event: Listen for user request to apply update immediately
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('[PWA SW] Received SKIP_WAITING signal from user. Activating update...');
    self.skipWaiting();
  }
});

// 4. Fetch Event: Network-first for dynamic lab records, stale-while-revalidate for static files
self.addEventListener('fetch', (event) => {
  // Only intercept GET requests
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Skip chrome-extension or external cross-origin requests
  if (!url.protocol.startsWith('http')) return;

  // HTML page navigations & API requests: ALWAYS Network-first so fresh LIMS data is prioritized
  if (event.request.mode === 'navigate' || event.request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Cache successful navigation responses for offline fallback
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(() => {
          // If offline, attempt cached version or fallback to root
          return caches.match(event.request).then((cached) => {
            return cached || caches.match('/');
          });
        })
    );
    return;
  }

  // Static assets (css, js, images, fonts): Stale-while-revalidate
  if (url.pathname.startsWith('/static/') || url.pathname.includes('font') || url.pathname.includes('cdn')) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        const fetchPromise = fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return networkResponse;
        }).catch(() => cachedResponse);

        return cachedResponse || fetchPromise;
      })
    );
  }
});
