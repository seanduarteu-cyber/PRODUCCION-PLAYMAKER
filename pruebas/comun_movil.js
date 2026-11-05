// Utilidades para revisar los sistemas en tamaño celular: sitios servidos con su dirección real y bases simuladas
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const BASE = path.resolve(__dirname, '../sistemas');
const SITIOS = { 'planificacion-playmaker.netlify.app': 'produccion', 'panel-fichas-playmaker.netlify.app': 'panel-fichas', 'ventas-playmaker.netlify.app': 'ventas' };
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.webmanifest': 'application/manifest+json' };
const USUARIO = { usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'], ejecutante_id: null };
async function contexto(b, datos, opciones) {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, serviceWorkers: 'block',
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1', ...(opciones || {}) });
  await ctx.route('**/*', async r => {
    const req = r.request(), u = new URL(req.url());
    if (SITIOS[u.host]) {
      const f = path.join(BASE, SITIOS[u.host], decodeURIComponent(u.pathname).replace(/^\//, '') || 'index.html');
      return fs.existsSync(f) && fs.statSync(f).isFile() ? r.fulfill({ body: fs.readFileSync(f), contentType: TIPOS[path.extname(f)] || 'application/octet-stream' }) : r.fulfill({ status: 404, body: 'no' });
    }
    if (/supabase\.co$/.test(u.host)) {
      const m = u.pathname.match(/\/rpc\/(\w+)/);
      if (m) {
        if (m[1] === 'plan_sesion' || m[1] === 'plan_login') return r.fulfill({ contentType: 'application/json', body: JSON.stringify({ ...USUARIO, token: 'tok1' }) });
        return r.fulfill({ contentType: 'application/json', body: JSON.stringify(datos.rpc && datos.rpc[m[1]] !== undefined ? datos.rpc[m[1]] : null) });
      }
      const tabla = u.pathname.split('/').pop();
      const rango = req.headers()['range'];
      if (req.method() !== 'GET') return r.fulfill({ contentType: 'application/json', body: '[]' });
      let filas = (datos.tablas && datos.tablas[tabla]) || [];
      if (typeof filas === 'function') filas = filas(u);
      if (rango && !rango.startsWith('0-')) filas = [];
      return r.fulfill({ contentType: 'application/json', body: JSON.stringify(filas) });
    }
    if (/fonts\.(googleapis|gstatic)/.test(u.host)) return r.fulfill({ status: 200, body: '' });
    if (/cdnjs\.cloudflare\.com/.test(u.host)) {
      const loc = { 'xlsx.full.min.js': '/opt/node22/lib/node_modules/xlsx/dist/xlsx.full.min.js' };
      return r.fulfill({ status: 200, contentType: 'text/javascript', body: '' });
    }
    return r.abort();
  });
  return ctx;
}
// Qué queda fuera de alcance: desborde de la página y elementos recortados por un contenedor sin desplazamiento
function revisar(p) {
  return p.evaluate(() => {
    const W = document.documentElement.clientWidth, out = { anchoPagina: document.documentElement.scrollWidth, ancho: W, cortados: [], fuera: [] };
    const nombre = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '') + ' «' + (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30) + '»';
    const visible = el => { for (let x = el; x; x = x.parentElement) { const s = getComputedStyle(x); if (s.display === 'none' || s.visibility === 'hidden') return false; } return true; };
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height || !visible(el)) continue;
      let p = el.parentElement, recorta = null;
      while (p && p !== document.documentElement) {
        const s = getComputedStyle(p);
        if (/auto|scroll/.test(s.overflowX)) break;
        if (/hidden|clip/.test(s.overflowX)) { recorta = p; break; }
        p = p.parentElement;
      }
      if (recorta) { const q = recorta.getBoundingClientRect(); if (r.right > q.right + 2 && r.left < q.right - 2 && el.children.length === 0) out.cortados.push(nombre(el) + ' en ' + nombre(recorta).slice(0, 40)); }
      if (r.right > W + 2 && el.children.length === 0 && !recorta) {
        let sc = false; for (let x = el.parentElement; x; x = x.parentElement) { if (/auto|scroll/.test(getComputedStyle(x).overflowX) && x !== document.documentElement && x !== document.body) { sc = true; break; } }
        if (!sc) out.fuera.push(nombre(el));
      }
    }
    out.cortados = [...new Set(out.cortados)].slice(0, 12); out.fuera = [...new Set(out.fuera)].slice(0, 12);
    return out;
  });
}
module.exports = { chromium, contexto, revisar, fs, path, BASE };
