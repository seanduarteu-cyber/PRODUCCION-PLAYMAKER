// Ventas: tiempo hasta ver los pedidos, con 300 pedidos que traen un comprobante de ~100 KB, en una conexión de 10 Mbps
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const COMP = 'A'.repeat(133000);   // ~100 KB de imagen en base64
const hoy = new Date().toISOString().slice(0, 10);
const DBS = Array.from({ length: 300 }, (_, i) => ({ id: i + 1, cot: 'COT-' + (5000 + i), cliente: 'Cliente ' + i, fecha: hoy, estado: 'Pagado', vendedor: 'Sean Duarte', total: 1e6, neto: 840336, saldo: 0,
  docs: [], observaciones: '[]', abonos: [{ monto: 1e6, fecha: hoy, metodo: 'Transferencia electrónica', comp64: COMP, compMime: 'image/jpeg', compName: 'c.jpg' }] }));
const liv = p => ({ ...p, abonos: p.abonos.map((a, i) => { const c = { ...a }; delete c.comp64; return { ...c, tiene_comp: true, _i: i }; }) });
const BPS = 10e6 / 8, LAT = 150;   // 10 Mbps, 150 ms
async function medir(archivo) {
  const b = await chromium.launch(); const ctx = await b.newContext({ serviceWorkers: 'block' }); let bytes = 0;
  // la red es una sola: las respuestas se reparten el ancho de banda (cola simple)
  let libre = Date.now();
  const enviar = async (r, body, ct) => { bytes += body.length; const ini = Math.max(Date.now() + LAT, libre); libre = ini + body.length / BPS * 1000;
    await new Promise(ok => setTimeout(ok, libre - Date.now())); return r.fulfill({ body, contentType: ct || 'application/json' }); };
  await ctx.route('**/*', async r => {
    const req = r.request(), u = new URL(req.url());
    if (u.host === 'ventas-playmaker.netlify.app') return r.fulfill({ body: fs.readFileSync(archivo), contentType: 'text/html' });
    if (u.host === 'ygcsqrylpibhofvetdyh.supabase.co') return enviar(r, JSON.stringify({ usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'] }));
    if (u.host === 'nnisdusdujcpkrbjqnhe.supabase.co') {
      if (u.pathname.endsWith('/rpc/pedidos_livianos')) { const { p_offset, p_cant } = JSON.parse(req.postData()); return enviar(r, JSON.stringify(DBS.slice(p_offset, p_offset + p_cant).map(liv))); }
      if (u.pathname.endsWith('/pedidos')) { const [a, z] = (req.headers()['range'] || '0-99').split('-').map(Number); return enviar(r, JSON.stringify(DBS.slice(a, z + 1))); }
      return enviar(r, '[]');
    }
    if (/xlsx/.test(u.pathname)) return enviar(r, 'x'.repeat(300000), 'text/javascript');   // ~300 KB comprimido
    if (/fonts/.test(u.host)) return r.fulfill({ body: '' });
    return r.abort();
  });
  const p = await ctx.newPage(); const t0 = Date.now();
  await p.goto('https://ventas-playmaker.netlify.app/#pmk_acceso=tok1');
  await p.waitForFunction(() => typeof DB !== 'undefined' && DB.length >= 300 && document.querySelector('#tabla-pedidos tr'), null, { timeout: 180000, polling: 100 });
  const t = Date.now() - t0; await b.close(); return { t, mb: (bytes / 1e6).toFixed(1) };
}
(async () => {
  const a = await medir(path.join(__dirname, 'antes/ventas.html'));
  console.log('Ventas antes :', (a.t / 1000).toFixed(1), 's ·', a.mb, 'MB');
  const d = await medir(path.resolve(__dirname, '../sistemas/ventas/index.html'));
  console.log('Ventas ahora :', (d.t / 1000).toFixed(1), 's ·', d.mb, 'MB');
})();
