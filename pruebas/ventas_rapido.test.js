// Ventas liviano: carga sin comprobantes, «Ver» los trae, y ningún guardado pierde un comprobante
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const HTML = fs.readFileSync(path.resolve(__dirname, '../sistemas/ventas/index.html'));
const PNG = fs.readFileSync(path.resolve(__dirname, '../sistemas/produccion/icon-192.png')).toString('base64');
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const hoy = new Date().toISOString().slice(0, 10);
function base() {
  return Array.from({ length: 450 }, (_, i) => ({ id: i + 1, cot: 'COT-' + (5000 + i), cliente: 'Cliente ' + i, fecha: hoy, estado: 'Abono parcial', vendedor: 'Sean Duarte', canal: 'Directo',
    tipo_venta: 'Uniformes', cantidad: 10, total: 1000000, neto: 840336, saldo: 300000, descuento_pct: 0, docs: [], observaciones: '[]', created_at: new Date().toISOString(),
    abonos: [{ monto: 500000, fecha: hoy, metodo: 'Transferencia electrónica', comp64: PNG, compMime: 'image/png', compName: 'transf_' + i + '.png' },
             { monto: 200000, fecha: hoy, metodo: 'Depósito bancario' }] }));
}
const liviano = p => ({ ...p, abonos: (p.abonos || []).map((a, i) => { const c = { ...a }; delete c.comp64; return { ...c, tiene_comp: !!a.comp64, _i: i }; }) });
async function correr(conRpc) {
  let DBS = base(); const upserts = [], pedidosLeidos = []; let rpcLlamadas = 0, xlsxPedido = false, bytes = 0;
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 800 }, serviceWorkers: 'block' });
  await ctx.route('**/*', async r => {
    const req = r.request(), u = new URL(req.url());
    const responder = (obj, st) => { const body = JSON.stringify(obj); bytes += body.length; return r.fulfill({ status: st || 200, contentType: 'application/json', body }); };
    if (u.host === 'ventas-playmaker.netlify.app') return r.fulfill({ body: HTML, contentType: 'text/html' });
    if (u.host === 'ygcsqrylpibhofvetdyh.supabase.co') return responder(/plan_sesion/.test(u.pathname) ? { usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'] } : []);
    if (u.host === 'nnisdusdujcpkrbjqnhe.supabase.co') {
      if (u.pathname.endsWith('/rpc/pedidos_livianos')) { rpcLlamadas++; if (!conRpc) return responder({ code: 'PGRST202', message: 'not found' }, 404);
        const { p_offset, p_cant } = JSON.parse(req.postData()); return responder(DBS.slice(p_offset, p_offset + p_cant).map(liviano)); }
      if (u.pathname.endsWith('/pedidos')) {
        if (req.method() === 'POST') { const body = JSON.parse(req.postData()); upserts.push(body); const i = DBS.findIndex(x => x.id === body.id); if (i >= 0) DBS[i] = { ...DBS[i], ...body }; return r.fulfill({ status: 201, body: '' }); }
        const m = u.search.match(/id=eq\.(\d+)/);
        if (m) { pedidosLeidos.push(+m[1]); return responder(DBS.filter(x => x.id === +m[1]).map(x => ({ abonos: x.abonos }))); }
        const rango = req.headers()['range'] || '0-99'; const [a, z] = rango.split('-').map(Number); return responder(DBS.slice(a, z + 1));
      }
      return responder([]);
    }
    if (/xlsx/.test(u.pathname)) { xlsxPedido = true; return r.fulfill({ contentType: 'text/javascript', body: 'window.XLSX={utils:{json_to_sheet:()=>({}),book_new:()=>({}),book_append_sheet(){}},writeFile(){window.__xlsxOk=true}};' }); }
    if (/fonts/.test(u.host)) return r.fulfill({ body: '' });
    return r.abort();
  });
  const p = await ctx.newPage(); const errores = []; p.on('pageerror', e => errores.push(e.message)); p.on('dialog', d => d.accept());
  const t0 = Date.now();
  await p.goto('https://ventas-playmaker.netlify.app/#pmk_acceso=tok1');
  await p.waitForFunction(() => typeof DB !== 'undefined' && DB.length >= 450, null, { timeout: 30000 });
  const modo = conRpc ? '[liviano]' : '[sin SQL 15A]';
  console.log(modo, 'cargado en', Date.now() - t0, 'ms ·', Math.round(bytes / 1024), 'KB recibidos');
  ok(!xlsxPedido, modo + ' la librería de Excel no se descarga al abrir');
  const enMemoria = await p.evaluate(() => ({ n: DB.length, conComp: DB.filter(r => r.abonos.some(a => a.comp64)).length, liv: PEDIDOS_LIVIANOS }));
  if (conRpc) ok(enMemoria.n === 450 && enMemoria.conComp === 0 && enMemoria.liv, '[liviano] 450 pedidos sin comprobantes en memoria (' + JSON.stringify(enMemoria) + ')');
  else ok(enMemoria.n === 450 && enMemoria.conComp === 450 && !enMemoria.liv, '[sin SQL 15A] carga completa como antes (' + JSON.stringify(enMemoria) + ')');
  // «Ver» el comprobante desde el detalle
  await p.evaluate(() => verDetalle(7)); await p.waitForTimeout(300);
  await p.click('#modal-body table a'); await p.waitForTimeout(600);
  ok(await p.evaluate(() => { const i = document.querySelector('.comp-visor img'); return !!(i && i.naturalWidth); }), modo + ' «Ver» muestra la transferencia');
  if (conRpc) ok(pedidosLeidos.includes(7), '[liviano] el comprobante se trajo al tocar «Ver»');
  await p.click('.comp-visor button'); await p.evaluate(() => closeModal());
  // guardar un cambio del pedido (observación) sin haber visto el comprobante: debe guardarse con el comprobante
  const leidosAntes = pedidosLeidos.length;
  await p.evaluate(async () => { const r = DB.find(x => x.id === 12); r.observaciones = JSON.stringify([{ autor: 'Sean', texto: 'nota', fecha: new Date().toISOString() }]); await saveEdits(r); });
  let up = upserts.filter(x => x.id === 12).pop();
  ok(up && up.abonos[0].comp64 === base()[11].abonos[0].comp64 && up.abonos[0].compName === 'transf_11.png', modo + ' guardar una nota mantiene el comprobante');
  ok(up && up.abonos.every(a => !('tiene_comp' in a) && !('_i' in a) && !('_pid' in a)), modo + ' lo guardado no lleva marcas internas');
  if (conRpc) ok(pedidosLeidos.length === leidosAntes + 1, '[liviano] antes de guardar se trajeron los comprobantes');
  // eliminar el abono 2 (sin comprobante): el 1 conserva su comprobante
  await p.evaluate(async () => { await eliminarAbono(20, 1, 'detalle'); });
  up = upserts.filter(x => x.id === 20).pop();
  ok(up && up.abonos.length === 1 && up.abonos[0].comp64 === PNG, modo + ' eliminar un abono no borra el comprobante del otro');
  // eliminar el abono 1 (con comprobante) en otro pedido: queda el 2 y no se envía comprobante
  await p.evaluate(async () => { await eliminarAbono(21, 0, 'detalle'); });
  up = upserts.filter(x => x.id === 21).pop();
  ok(up && up.abonos.length === 1 && !up.abonos[0].comp64 && up.abonos[0].monto === 200000, modo + ' eliminar el abono con comprobante lo quita solo a él');
  // otro guardado del mismo pedido después: no vuelve a leer y conserva todo
  await p.evaluate(async () => { const r = DB.find(x => x.id === 20); r.observaciones = '[]'; await saveEdits(r); });
  up = upserts.filter(x => x.id === 20).pop();
  ok(up && up.abonos.length === 1 && up.abonos[0].comp64 === PNG, modo + ' segundo guardado del mismo pedido conserva el comprobante');
  // si el comprobante cambió en la base desde otro equipo: no se guarda (no se pisa)
  if (conRpc) {
    const i = DBS.findIndex(x => x.id === 30); DBS[i] = { ...DBS[i], abonos: [{ ...DBS[i].abonos[0], compName: 'otro.png', monto: 999 }, DBS[i].abonos[1]] };
    const n = upserts.length;
    const res = await p.evaluate(async () => { const r = DB.find(x => x.id === 30); try { await saveEdits(r); return 'guardado'; } catch (e) { return e.message; } });
    ok(upserts.length === n && /cambió desde otro equipo/.test(res), '[liviano] si el comprobante cambió en otro equipo, no se pisa: «' + res.slice(0, 60) + '…»');
  }
  // registrar un abono nuevo con comprobante: los anteriores conservan el suyo
  await p.evaluate(() => abrirAbono(40)); await p.waitForTimeout(200);
  await p.fill('#abono-monto', '100000');
  await p.evaluate(b64 => { comprobante64 = b64; comprobanteMime = 'image/png'; comprobanteName = 'nuevo.png'; }, PNG);
  await p.evaluate(async () => { await guardarAbono(); }); await p.waitForTimeout(300);
  up = upserts.filter(x => x.id === 40).pop();
  ok(up && up.abonos.length === 3 && up.abonos[0].comp64 === PNG && up.abonos[0].compName === 'transf_39.png' && up.abonos[2].compName === 'nuevo.png' && up.abonos[2].comp64 === PNG, modo + ' abono nuevo con comprobante: se guardan los tres, con sus comprobantes');
  // corregir el monto del abono 2 (sin comprobante) desde «Editar»
  await p.evaluate(() => { closeAbonoModal && closeAbonoModal(); editarAbono(41, 1, 'detalle'); }); await p.waitForTimeout(300);
  const campoMonto = await p.$('#abono-monto');
  if (campoMonto) { await campoMonto.fill('250000'); await p.evaluate(async () => { await guardarEdicionAbono(); }); await p.waitForTimeout(300);
    up = upserts.filter(x => x.id === 41).pop();
    ok(up && up.abonos[1].monto === 250000 && up.abonos[0].comp64 === PNG, modo + ' corregir un abono conserva el comprobante del otro'); }
  else ok(false, modo + ' no se encontró el formulario de corrección');
  // limpieza diaria (gerencia): el respaldo lleva los comprobantes y el pedido queda sin ellos
  const resp = [];
  await p.route('**/respaldo_comprobantes_2026', r2 => { resp.push(JSON.parse(r2.request().postData())); r2.fulfill({ status: 201, body: '' }); });
  { const i50 = DBS.findIndex(x => x.id === 50); DBS[i50] = { ...DBS[i50], abonos: DBS[i50].abonos.map(a => ({ ...a, fecha: '2026-01-10' })) }; }
  await p.evaluate(() => { const r = DB.find(x => x.id === 50); r.estado = 'Pagado'; r.saldo = 0; r.abonos.forEach(a => a.fecha = '2026-01-10'); sessionStorage.setItem('pmk_rol', 'gerencia'); localStorage.removeItem('pmk_ultima_limpieza'); DB = DB.filter(x => x.id === 50 || x.estado !== 'Pagado'); });
  await p.evaluate(async () => { await limpiezaAutomaticaDiaria(); });
  up = upserts.filter(x => x.id === 50).pop();
  ok(resp.length === 1 && resp[0].abonos[0].comp64 === PNG && !('_i' in resp[0].abonos[0]), modo + ' limpieza: el respaldo lleva el comprobante');
  ok(up && up.abonos.every(a => !a.comp64), modo + ' limpieza: el pedido queda sin comprobantes');
  // Excel: la librería llega al exportar
  await p.evaluate(() => descargarExcel()); await p.waitForTimeout(400);
  ok(xlsxPedido && await p.evaluate(() => window.__xlsxOk === true), modo + ' «Descargar Excel» carga la librería y exporta');
  ok(errores.length === 0, modo + ' sin errores de JavaScript ' + errores.join(' | '));
  await b.close();
}
function PNG_ESPERADO_20() { return PNG; }
(async () => {
  // la función de la página no conoce PNG_ESPERADO_20: se compara aquí
  await correr(true); await correr(false);
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
