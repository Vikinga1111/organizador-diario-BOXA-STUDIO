const CACHE = 'boxa-horario-v2';

// Detect base URL from scope path
const BASE_URL = (function(){
  const path = self.location.pathname;
  const match = path.match(/^(\/[^\/]+\/)/);
  return match ? match[1] : '/';
})();

const ASSETS = [
  BASE_URL,
  BASE_URL + 'index.html',
  BASE_URL + 'manifest.json',
  BASE_URL + 'icons/icon-192.png',
  BASE_URL + 'icons/icon-512.png',
  'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // Never intercept Supabase or external API calls
  const url = e.request.url;
  if (url.includes('supabase.co') || url.includes('googleapis.com') || e.request.method !== 'GET') {
    return;
  }
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request).then(res => {
      const clone = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, clone));
      return res;
    }))
  );
});
