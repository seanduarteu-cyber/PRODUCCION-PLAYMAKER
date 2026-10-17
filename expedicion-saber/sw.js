/* Service worker de Expedición Saber: permite jugar sin conexión después de la primera visita.
   Estrategia «red primero»: con internet siempre se usa la versión más nueva y se guarda una copia;
   sin internet se usa la copia guardada. */
const CACHE = 'expedicion-saber-v1';
const BASE = ['./', './index.html', './manifest.webmanifest', './js/motor.js', './js/avatar_bloques.js', './js/avatar_heroes.js',
  './js/avatar_plataformas.js', './js/ui.js', './js/retos.js', './mundos/mundos.json', './contenido/indice.json',
  './iconos/icono-192.png', './iconos/icono-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(BASE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then(r => { const copia = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copia)); return r; })
      .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
  );
});
