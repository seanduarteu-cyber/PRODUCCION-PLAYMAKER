// Panel de fichas: cambiar el molde de un diseño ya cargado sin perder las personas (nombres, números y tallas),
// los montajes ni la ficha técnica; el despiece pasa al molde nuevo conservando las telas. Bases simuladas.
const { chromium, contexto } = require('./comun_movil');
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const hoy = new Date().toISOString().slice(0, 10), ahora = new Date().toISOString();
const moldes = require('./datos_moldes_catalogo.json').map(m => Object.assign({}, m));
const piezas = { 2: ['Delantero', 'Espalda', 'Manga'], 21: ['Delantero', 'Espalda', 'Manga raglán', 'Cuello v'], 22: ['Delantero', 'Espalda', 'Manga raglán', 'Cuello v'] };
moldes.forEach(m => { if (piezas[m.numero]) m.piezas = piezas[m.numero].map(p => ({ pieza: p, cant: 1, tela: '' })); });

// COT-3700: camiseta «Jugadores» con el molde 02 (FUTHOMU01) por error, y short; tres personas con nombre, número y tallas
const ficha = { id: 1, ref: 'COT-3700', proyecto: 'Uniformes damas', cliente: 'Club Prueba', vendedor: 'Sean Duarte', entrega: hoy, entrega_interna: hoy, entrega_cliente: hoy,
  estado: 'confirmado', created_at: ahora,
  items: [{ prenda: 'camiseta', cant: 3 }, { prenda: 'short', cant: 3 }],
  specs: { camiseta: { nombre: 'Jugadores', deporte: 'Fútbol', tela: 'Nacional', moldes: { Masculino: 'FUTHOMU01|2' }, unidades: { Masculino: 3 },
      despiece: { molde: '02 · FUTHOMU01', piezas: [{ pieza: 'Delantero', cant: 1, tela: 'Dry fit azul', detalle: 'Sublimada' }, { pieza: 'Espalda', cant: 1, tela: 'Dry fit azul', detalle: 'Sublimada' },
        { pieza: 'Manga', cant: 2, tela: 'Dry fit blanco', detalle: '' }] } },
    short: { moldes: { Masculino: 'BK-SH|46' }, unidades: { Masculino: 3 }, tela: 'Nacional' } },
  imagenes: [{ url: 'https://x.test/cam.jpg', prendas: ['camiseta'], prenda: 'camiseta', moldes: ['FUTHOMU01|2'], vista: 'Completo', path: 'a/1.jpg' },
    { url: 'https://x.test/sho.jpg', prendas: ['short'], prenda: 'short', vista: 'Completo', path: 'a/2.jpg' }] };
const personas = [['p1', 'Ana Pérez', 'ANA', '7', 'S'], ['p2', 'Bea Soto', 'BEA', '9', 'M'], ['p3', 'Caro Díaz', 'CARO', '10', 'L']].map(x =>
  ({ id: x[0], ref: 'COT-3700', nombre: x[1], estampado: x[2], numero: x[3], calce: 'Masculino', manga: 'Corta', arquero: false, obs: '', tallas: { camiseta: x[4], short: x[4] }, disenos: {}, created_at: ahora }));
// COT-3701: el molde ya se cambió en la ficha técnica (22) pero el despiece sigue siendo del 02
const ficha2 = Object.assign({}, ficha, { id: 2, ref: 'COT-3701', estado: 'abierto', items: [{ prenda: 'camiseta', cant: 3 }], imagenes: [],
  specs: { camiseta: Object.assign({}, ficha.specs.camiseta, { moldes: { Masculino: 'FUTHOMV02|22' } }) } });
const porRef = filas => u => { const m = (u.searchParams.get('ref') || '').replace(/^eq\./, ''); return m ? filas.filter(f => f.ref === m) : filas; };
const datos = { tablas: { fichas_tallas: porRef([ficha, ficha2]), fichas_detalle: porRef(personas), fichas_avisos: [], moldes, catalogo_tecnico: [], pedidos: [] } };

(async () => {
  const b = await chromium.launch();
  const ctx = await contexto(b, datos, { viewport: { width: 1280, height: 900 }, isMobile: false, hasTouch: false, userAgent: undefined });
  const envios = [];
  await ctx.route(/supabase\.co\/rest\/v1\/fichas_(tallas|detalle)/, r => {
    const q = r.request(); if (q.method() === 'GET') return r.fallback();
    envios.push({ m: q.method(), u: decodeURIComponent(q.url()), d: q.postData() ? JSON.parse(q.postData()) : null });
    return r.fulfill({ contentType: 'application/json', body: '[]' });
  });
  const p = await ctx.newPage(); const errores = []; p.on('pageerror', e => errores.push(e.message)); p.on('dialog', d => d.accept());
  const texto = sel => p.innerText(sel || '#app').catch(() => p.innerText('body'));

  await p.goto('https://panel-fichas-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(1200);
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3700'); await p.waitForTimeout(1500);
  await p.click('[data-ir="editar"]'); await p.waitForTimeout(900);

  // 1 · cada molde tiene «Cambiar molde»; el catálogo se abre en modo cambio, solo con camisetas
  ok((await p.$$('[data-cambiar-molde]')).length === 2, 'cada molde de la ficha tiene su botón «Cambiar molde»');
  await p.click('[data-linea="0"] [data-cambiar-molde]'); await p.waitForTimeout(500);
  const cat = await texto('#cat-mol');
  ok(/Cambiar el molde de «Jugadores»/.test(cat) && /Molde actual: N° 02 · FUTHOMU01/.test(cat) && /se conservan las personas/.test(cat), 'el catálogo dice qué molde se cambia y que se conservan las personas');
  const subs = await p.$$eval('#cat-mol .cat-fila .lm-sub', ss => ss.map(s => s.textContent));
  ok(subs.length > 5 && subs.every(s => /^Camiseta/.test(s)), 'solo ofrece moldes de camiseta (' + subs.length + ')');
  ok(await p.$eval('#cat-mol .cat-fila button[disabled]', x => x.textContent) === 'Molde actual', 'el molde actual aparece marcado y no se puede elegir');
  ok(!(await p.$('#cat-mol [data-add-molde]')), 'en modo cambio no se agregan diseños nuevos');

  // 2 · elegir otro molde del mismo calce, deshacer, y elegir el correcto (femenino)
  await p.selectOption('#cat-mol [data-cf="calce"]', ''); await p.waitForTimeout(400);
  await p.click('[data-usar-molde="22"]'); await p.waitForTimeout(400);
  { const t0 = await texto('[data-linea="0"]'); ok(/Molde cambiado · antes:\s+N° 02 · FUTHOMU01/.test(t0) && /FUTHOMV02/.test(t0), 'la línea muestra el molde nuevo y el anterior: ' + t0.replace(/\s+/g, ' ')); }
  ok(!(await p.$('[data-linea="0"] [data-mover-calce]')), 'mismo calce: no pregunta por las personas');
  await p.click('[data-deshacer-molde="0"]'); await p.waitForTimeout(300);
  ok(!/Molde cambiado/.test(await texto('[data-linea="0"]')) && /FUTHOMU01/.test(await texto('[data-linea="0"]')), '«Deshacer» vuelve al molde anterior');
  await p.click('[data-linea="0"] [data-cambiar-molde]'); await p.waitForTimeout(400);
  await p.selectOption('#cat-mol [data-cf="calce"]', 'Femenino'); await p.waitForTimeout(400);
  await p.click('[data-usar-molde="21"]'); await p.waitForTimeout(400);
  const l0 = await texto('[data-linea="0"]');
  ok(/3 personas de este diseño están cargadas como masculino y el molde nuevo es femenino/.test(l0), 'avisa que las 3 personas están en el calce anterior');
  ok(await p.$eval('[data-linea="0"] [data-mover-calce][value="1"]', x => x.checked), 'por defecto se pasan al calce del molde nuevo');
  ok(/También llevan «Short o calza», que no tiene molde femenino/.test(l0), 'avisa que esas personas también llevan un short sin molde femenino: ' + l0.replace(/\s+/g, ' '));
  ok(/3 cargadas por el cliente/.test(l0), 'la línea cuenta a las personas que pasan');

  // 3 · guardar: mismo diseño (camiseta), sin borrar ni volver a cargar personas
  envios.length = 0;
  await p.click('#btn-guardar-items'); await p.waitForTimeout(1500);
  const pt = envios.find(e => e.m === 'PATCH' && /fichas_tallas/.test(e.u) && e.d && e.d.specs) || {}, sp = ((pt.d || {}).specs || {}).camiseta || {};
  ok(pt.d && pt.d.items.map(i => i.prenda + ':' + i.cant).join() === 'camiseta:3,short:3', 'los diseños son los mismos (camiseta y short), con sus cantidades');
  ok(JSON.stringify(sp.moldes) === '{"Femenino":"FUTMUJV02|21"}' && JSON.stringify(sp.unidades) === '{"Femenino":3}', 'la camiseta queda con el molde 21 femenino: ' + JSON.stringify(sp.moldes));
  ok(sp.nombre === 'Jugadores' && sp.tela === 'Nacional', 'se conservan el nombre del diseño y la tela principal');
  const dp = sp.despiece || {};
  ok(dp.molde === '21 · FUTMUJV02' && (dp.piezas || []).map(q => q.pieza).join() === 'Delantero,Espalda,Manga raglán,Cuello v', 'despiece del molde nuevo: ' + (dp.piezas || []).map(q => q.pieza).join());
  ok(dp.piezas && dp.piezas[0].tela === 'Dry fit azul' && dp.piezas[0].detalle === 'Sublimada' && dp.piezas[1].tela === 'Dry fit azul' && !dp.piezas[2].tela, 'conserva la tela y el proceso de las piezas que se llaman igual');
  ok(sp.moldeCambiado && sp.moldeCambiado.antes === 'N° 02 · FUTHOMU01' && sp.moldeCambiado.ahora === 'N° 21 · FUTMUJV02', 'queda marcado para revisar en la ficha técnica');
  const pc = envios.find(e => e.m === 'PATCH' && /fichas_detalle/.test(e.u)) || {};
  ok(/id=in\.\("p1","p2","p3"\)/.test(pc.u || '') && JSON.stringify(pc.d) === '{"calce":"Femenino"}', 'las 3 personas pasan a femenino en un solo envío (solo cambia el calce)');
  ok(!envios.some(e => /fichas_detalle/.test(e.u) && e.m !== 'PATCH'), 'no se borra ni se vuelve a crear ninguna persona');
  const pi = envios.find(e => e.m === 'PATCH' && e.d && e.d.imagenes) || {};
  ok(pi.d && JSON.stringify(pi.d.imagenes[0].moldes) === '["FUTMUJV02|21"]' && pi.d.imagenes.length === 2, 'el montaje de la camiseta queda con el molde nuevo y no se borra ninguno');

  // 4 · se abre la ficha técnica en ese diseño, con el aviso para revisar
  ok(await p.$('[data-mc="camiseta"]') && await p.$eval('details[data-sec="p-camiseta"]', d => d.open), 'se abre la ficha técnica en «Jugadores» con el aviso de molde cambiado');
  ok(/antes N° 02 · FUTHOMU01, ahora N° 21 · FUTMUJV02/.test(await texto('[data-mc="camiseta"]')), 'el aviso dice el molde anterior y el nuevo');
  ok(!(await p.$('[data-dp-otro="camiseta"]')), 'el despiece ya es del molde nuevo (sin aviso de piezas de otro molde)');
  envios.length = 0;
  await p.check('[data-mc-ok="camiseta"]'); await p.click('#btn-guardar-tec'); await p.waitForTimeout(1200);
  const pt2 = envios.find(e => e.m === 'PATCH' && e.d && e.d.specs) || {};
  ok(pt2.d && !pt2.d.specs.camiseta.moldeCambiado && pt2.d.specs.camiseta.despiece.molde === '21 · FUTMUJV02', 'al marcar «Ya lo revisé» y guardar, el aviso se quita');

  // 5 · ficha técnica con piezas de otro molde: se cargan las del nuevo conservando telas
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3701'); await p.waitForTimeout(1500);
  await p.click('[data-ir="tecnica"]'); await p.waitForTimeout(900);
  await p.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = true; }));
  ok(/Estas piezas son del molde 02 · FUTHOMU01, pero el molde ahora es 22 · FUTHOMV02/.test(await texto('[data-dp-otro="camiseta"]')), 'avisa que el despiece es de otro molde');
  await p.click('[data-dp-nuevo="camiseta"]'); await p.waitForTimeout(400);
  await p.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = true; }));
  const filas = await p.$$eval('.dp-tabla tbody tr', tr => tr.map(t => t.querySelector('input[data-k="pieza"]').value + '=' + (t.querySelector('.cbx-btn') || {}).textContent));
  ok(!(await p.$('[data-dp-otro="camiseta"]')) && filas.length === 4 && /^Delantero=Dry fit azul/.test(filas[0]), 'piezas del molde 22 con la tela de antes: ' + filas.join(' · '));

  // 6 · al crear una ficha también se puede cambiar el molde de una línea
  await p.goto('https://panel-fichas-playmaker.netlify.app/'); await p.waitForTimeout(1200);
  await p.click('[data-ir="crear"]'); await p.waitForTimeout(700);
  await p.click('#btn-catalogo'); await p.waitForTimeout(300);
  await p.click('[data-add-molde="2"]'); await p.waitForTimeout(300);
  await p.click('[data-linea="0"] [data-cambiar-molde]'); await p.waitForTimeout(300);
  await p.click('[data-usar-molde="22"]'); await p.waitForTimeout(300);
  ok((await p.$$('[data-linea]')).length === 1 && /FUTHOMV02/.test(await texto('[data-linea="0"]')) && await p.$('#cat-mol [data-add-molde]'), 'al crear: la línea cambia de molde y el catálogo sigue abierto para agregar');

  ok(!errores.length, 'panel sin errores JS ' + errores.join(' | '));
  await b.close();
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
