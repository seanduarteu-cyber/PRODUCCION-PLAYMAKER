// Tiempo de arranque con 200 ms de demora por consulta: versión anterior vs nueva
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, 'plan_movil.js'), 'utf8');
const datosPlan = new Function('require', src.slice(src.indexOf('const d ='), src.indexOf('(async')) + 'return datos;')(require);
const datosFichas = require('./datos_fichas');
const ESPERA = 200;
async function medir(html, host, datos, listo, url) {
  const b = await chromium.launch(); const ctx = await b.newContext({ serviceWorkers: 'block' });
  let consultas = 0;
  await ctx.route('**/*', async r => {
    const u = new URL(r.request().url());
    if (u.host === host) return r.fulfill({ body: html, contentType: 'text/html' });
    if (/supabase\.co$/.test(u.host)) {
      consultas++; await new Promise(ok => setTimeout(ok, ESPERA));
      if (/rpc\/plan_sesion/.test(u.pathname)) return r.fulfill({ contentType: 'application/json', body: JSON.stringify({ usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'], token: 'tok1' }) });
      if (/\/rpc\//.test(u.pathname)) return r.fulfill({ contentType: 'application/json', body: 'null' });
      let filas = (datos.tablas || {})[u.pathname.split('/').pop()] || [];
      if (typeof filas === 'function') filas = filas(u);
      const rango = r.request().headers()['range']; if (rango && !rango.startsWith('0-')) filas = [];
      return r.fulfill({ contentType: 'application/json', body: JSON.stringify(filas) });
    }
    if (/fonts/.test(u.host)) return r.fulfill({ body: '' });
    return r.abort();
  });
  const p = await ctx.newPage(); const t0 = Date.now();
  await p.goto(url); await p.waitForFunction(listo, null, { timeout: 60000, polling: 50 });
  const t = Date.now() - t0; await b.close(); return { t, consultas };
}
(async () => {
  const listoPlan = () => typeof PROY !== 'undefined' && PROY.length && PROY[0].et && Object.keys(PROY[0].et).length && document.querySelector('#vista *, main *');
  const listoFichas = () => /COT-3610/.test(document.body.innerText);
  for (const [n, host, antes, ahora, datos, listo, url] of [
    ['Fichas (ficha)', 'panel-fichas-playmaker.netlify.app', 'antes/fichas.html', '../sistemas/panel-fichas/index.html', datosFichas, () => /personas/i.test(document.body.innerText) && /22/.test(document.body.innerText), 'https://panel-fichas-playmaker.netlify.app/?ref=COT-3610#pmk_acceso=tok1'],
    ['Planificación', 'planificacion-playmaker.netlify.app', 'antes/produccion.html', '../sistemas/produccion/index.html', datosPlan, listoPlan, 'https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'],
    ['Fichas (lista)', 'panel-fichas-playmaker.netlify.app', 'antes/fichas.html', '../sistemas/panel-fichas/index.html', datosFichas, listoFichas, 'https://panel-fichas-playmaker.netlify.app/#pmk_acceso=tok1']]) {
    const a = await medir(fs.readFileSync(path.join(__dirname, antes)), host, datos, listo, url);
    const d = await medir(fs.readFileSync(path.join(__dirname, ahora)), host, datos, listo, url);
    console.log(n.padEnd(16), 'antes', a.t, 'ms (' + a.consultas + ' consultas) → ahora', d.t, 'ms (' + d.consultas + ' consultas)');
  }
})();
