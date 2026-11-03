// Sitio del cliente: camisetas sin nombre ni número (solo talla), en adulto e infantil, y el error completo si la base rechaza
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const HTML = fs.readFileSync(path.resolve(__dirname, '../sistemas/ingreso-fichas/index.html'));
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
async function correr({ calce, lista, baseRechaza }) {
  const ficha = { id: 1, ref: 'COT-7000', cliente: 'CLUB PRUEBA', proyecto: 'Uniformes', estado: 'abierto', acceso: 'ABC', items: [{ prenda: 'camiseta', cant: 5 }],
    specs: { camiseta: { deporte: 'Fútbol', moldes: { [calce]: calce === 'Infantil' ? 'FUT-NIN|40' : 'FUT-HOMUC01|1' }, unidades: { [calce]: 5 } } }, created_at: new Date().toISOString() };
  const detalle = [], patchSpecs = [];
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await ctx.route('**/*', async r => {
    const req = r.request(), u = new URL(req.url());
    if (u.host === 'ingreso-fichas-playmaker.netlify.app') return r.fulfill({ body: HTML, contentType: 'text/html' });
    if (u.host === 'jvgifibnoigpicwklasw.supabase.co') {
      if (/rpc\/ficha_cliente/.test(u.pathname)) return r.fulfill({ contentType: 'application/json', body: JSON.stringify(ficha) });
      if (/fichas_detalle/.test(u.pathname)) {
        if (req.method() === 'POST') {
          const filas = [].concat(JSON.parse(req.postData()));
          if (baseRechaza && filas.some(x => !x.nombre && !x.numero && !x.estampado))
            return r.fulfill({ status: 400, contentType: 'application/json', body: JSON.stringify({ code: '23514', details: null, hint: null, message: 'new row for relation "fichas_detalle" violates check constraint "fichas_detalle_identifica"' }) });
          filas.forEach(x => { const i = detalle.findIndex(d => d.id === x.id); if (i >= 0) detalle[i] = x; else detalle.push({ ...x, created_at: new Date().toISOString() }); });
          return r.fulfill({ status: 201, body: '' });
        }
        return r.fulfill({ contentType: 'application/json', body: JSON.stringify(detalle) });
      }
      if (/fichas_tallas/.test(u.pathname) && req.method() === 'PATCH') { const bd = JSON.parse(req.postData()); if (bd.specs) { patchSpecs.push(bd.specs); ficha.specs = bd.specs; } return r.fulfill({ status: 204, body: '' }); }
      if (/fichas_tallas/.test(u.pathname)) return r.fulfill({ contentType: 'application/json', body: JSON.stringify([ficha]) });
      return r.fulfill({ contentType: 'application/json', body: '[]' });
    }
    if (/fonts/.test(u.host)) return r.fulfill({ body: '' });
    return r.abort();
  });
  const p = await ctx.newPage(); const errores = []; p.on('pageerror', e => errores.push(e.message)); p.on('dialog', d => d.accept());
  await p.goto('https://ingreso-fichas-playmaker.netlify.app/?f=ABC'); await p.waitForTimeout(800);
  await p.click('[data-ir="pedido"]'); await p.waitForTimeout(800);
  await p.click('[data-paso]'); await p.waitForTimeout(400);
  const pregunta = await p.isVisible('[data-chip="lote_numero"]');
  const etiqueta = pregunta ? await p.evaluate(() => [...document.querySelectorAll('.campo label')].map(l => l.textContent).find(t => /número/.test(t))) : '';
  await p.click('[data-chip="lote_estampar"][data-val="no"]');
  await p.fill('#lote-texto', lista.join('\n'));
  // sin responder lo del número: lo pide
  await p.click('#btn-leer'); await p.waitForTimeout(200);
  const pideResponder = /Responde si las camisetas llevan número/.test(await p.textContent('.aviso.error').catch(() => ''));
  await p.click('[data-chip="lote_numero"][data-val="no"]');
  await p.fill('#lote-texto', lista.join('\n'));
  await p.click('#btn-leer'); await p.waitForTimeout(300);
  const contador = await p.textContent('#contador').catch(() => '');
  const bajada = await p.textContent('.bajada').catch(() => '');
  await p.click('#btn-guardar-lote'); await p.waitForTimeout(400);
  if (await p.$('#btn-guardar-arq')) { await p.click('#btn-guardar-arq'); await p.waitForTimeout(800); }
  const error = await p.textContent('.aviso.error').catch(() => '');
  await p.screenshot({ path: 'movil/cliente_sin_numero_' + calce + (baseRechaza ? '_rechazo' : '') + '.png', fullPage: true });
  await b.close();
  return { pregunta, etiqueta, pideResponder, contador, bajada, detalle, patchSpecs, error, errores };
}
(async () => {
  let r = await correr({ calce: 'Masculino', lista: ['L', 'XL', 'Sin nombre: M', 'S', 'XL'], baseRechaza: false });
  ok(r.pregunta && r.etiqueta === '¿Las camisetas llevan número?', 'pregunta «¿Las camisetas llevan número?»');
  ok(r.pideResponder, 'si no se responde, lo pide');
  ok(/5 personas/.test(r.contador) && !/sin talla|sin número/.test(r.contador), 'lista de 5 solo con talla, sin faltantes: «' + r.contador.trim() + '»');
  ok(/Las camisetas no llevan número: basta con la talla/.test(r.bajada), 'explica que basta con la talla');
  ok(r.detalle.length === 5 && r.detalle.every(d => !d.nombre && !d.numero && d.tallas.camiseta) && r.detalle.map(d => d.tallas.camiseta).join() === 'L,XL,M,S,XL', 'se guardan 5 camisetas solo con talla (' + r.detalle.map(d => d.tallas.camiseta).join() + ')');
  ok(r.patchSpecs.length === 1 && r.patchSpecs[0].camiseta.numero === 'no', 'la ficha queda marcada «camisetas sin número»');
  ok(r.errores.length === 0 && !r.error, 'sin errores ' + r.errores.join('|') + r.error);
  r = await correr({ calce: 'Infantil', lista: ['10', '12', '14', '8', '10'], baseRechaza: false });
  ok(r.detalle.length === 5 && r.detalle.map(d => d.tallas.camiseta).join() === '10,12,14,8,10' && r.detalle.every(d => !d.numero), 'infantil: «10» se toma como talla, no como número (' + r.detalle.map(d => d.tallas.camiseta + '/' + (d.numero || '-')).join() + ')');
  r = await correr({ calce: 'Masculino', lista: ['L', 'XL'], baseRechaza: true });
  ok(/fichas_detalle_identifica/.test(r.error), 'si la base aún no tiene el SQL 16A, el error se ve completo (con el nombre de la regla)');
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
