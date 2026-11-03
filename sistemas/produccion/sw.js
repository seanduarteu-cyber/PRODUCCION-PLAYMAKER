/* Playmaker · Producción — permite instalar el sistema como aplicación en el celular.
   La página se pide siempre a internet primero (así cada publicación en Netlify llega de inmediato);
   solo si no hay conexión se muestra la última versión guardada. Los datos (Supabase) nunca se guardan aquí. */
const CACHE = 'pmk-produccion-v1';
const BASE = ['./', 'sistemas.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'apple-touch-icon.png'];
self.addEventListener('install', e => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then(c => c.addAll(BASE)).catch(() => {})); });
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;            // Supabase y otros servicios: siempre directo
  if (req.mode === 'navigate') {
    // la aplicación se guarda como './'; otras páginas (sistemas.html), con su propia dirección
    const clave = /\/(index\.html)?$/.test(url.pathname) ? './' : url.pathname;
    e.respondWith(fetch(req).then(r => { const copia = r.clone(); caches.open(CACHE).then(c => c.put(clave, copia)); return r; })
      .catch(() => caches.match(clave).then(r => r || caches.match('./'))));
    return;
  }
  e.respondWith(caches.match(req).then(r => r || fetch(req)));
});
