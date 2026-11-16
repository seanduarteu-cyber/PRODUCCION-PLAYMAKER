// Planificación · «Devolver a una etapa»: un pedido terminado o en curso vuelve a una etapa anterior para completar lo que falta
// Base simulada con estado (lee, cambia, agrega y borra filas como Supabase) para revisar lo que queda guardado.
const { chromium, contexto } = require('./comun_movil');
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const d = n => { const x = new Date(); x.setDate(x.getDate() + n); return x.toISOString().slice(0, 10); };
const ts = n => d(n) + 'T15:00:00.000Z';
const dh = n => { while ([0, 6].includes(new Date(d(n) + 'T12:00:00Z').getUTCDay())) n++; return d(n); };   // día hábil (lun-vie)
const ETS = { ARMADO: 1, CORTE: 2, REVISION: 3, PLOTEO: 4, SUBL: 5, CONFEC: 6, ESTAMP: 7, ENTREGA: 8 };
const base = (id, cot, extra) => ({ id, cot, cliente: 'Club ' + cot, prendas: 30, desglose: { 'FUT-HOMUC01|1 · MC': 30 }, moldes: [], fecha_ingreso_ficha: d(-20),
  fecha_entrega_cliente: d(-3), fecha_termino_interno: d(-8), tipo: 'normal', requiere_estampado: false, requiere_sublimacion: true, observaciones: null,
  estado_general: 'en_produccion', responsable_ficha: 'Sean Duarte', resumido_at: null, terminado_at: null, created_at: ts(-20), ...extra });
const DB = {
  prod: {
    planificacion: [
      base(20, 'COT-3700', { estado_general: 'entregado' }),                                         // terminado, con su detalle
      base(21, 'COT-3701', { estado_general: 'entregado', resumido_at: ts(-5), terminado_at: ts(-100), fecha_entrega_cliente: d(-101) }),   // detalle borrado
      base(22, 'COT-3702', { fecha_entrega_cliente: dh(12), fecha_termino_interno: d(7) })             // en curso, en Confección
    ],
    planificacion_etapas: [], planificacion_log: []
  },
  fichas: { fichas_tallas: [{ ref: 'COT-3700', cliente: 'Club COT-3700', estado: 'confirmado', montaje_aprobado: true, entrega_cliente: d(-3), entrega_interna: d(-8), items: [], specs: {} }] }
};
let eid = 1;
const sinEstampado = Object.keys(ETS).filter(k => k !== 'ESTAMP');
sinEstampado.forEach(k => DB.prod.planificacion_etapas.push({ id: eid++, planificacion_id: 20, etapa: k, orden: ETS[k], estado: 'terminado', fecha_inicio_plan: d(-18),
  fecha_limite: d(-4), fecha_inicio_real: ts(-15), fecha_termino_real: k === 'ENTREGA' ? ts(-2) : ts(-6), responsable: 'Pedro', observaciones: null }));
sinEstampado.forEach(k => DB.prod.planificacion_etapas.push({ id: eid++, planificacion_id: 22, etapa: k, orden: ETS[k], estado: ETS[k] < 6 ? 'terminado' : ETS[k] === 6 ? 'en_proceso' : 'pendiente',
  fecha_inicio_plan: d(-5), fecha_limite: d(5), fecha_inicio_real: ETS[k] <= 6 ? ts(-4) : null, fecha_termino_real: ETS[k] < 6 ? ts(-2) : null, responsable: ETS[k] <= 6 ? 'Pedro' : null, observaciones: null }));

// filtros de PostgREST que usa Planificación
function calza(fila, k, v) {
  const val = fila[k], txt = val == null ? null : String(val);
  if (v.startsWith('eq.')) return txt === decodeURIComponent(v.slice(3));
  if (v.startsWith('neq.')) return txt !== decodeURIComponent(v.slice(4));
  if (v.startsWith('is.null')) return val == null;
  if (v.startsWith('not.is.null')) return val != null;
  if (v.startsWith('in.(')) return v.slice(4, -1).split(',').map(x => decodeURIComponent(x).replace(/^"|"$/g, '')).includes(txt);
  for (const [op, f] of [['lte.', (a, b) => a <= b], ['gte.', (a, b) => a >= b], ['lt.', (a, b) => a < b], ['gt.', (a, b) => a > b]])
    if (v.startsWith(op)) return txt != null && f(txt, decodeURIComponent(v.slice(op.length)));
  return true;
}
function filtrar(filas, u) {
  const filtros = [...u.searchParams.entries()].filter(([k]) => !['select', 'order', 'limit', 'offset', 'or', 'and'].includes(k));
  let out = filas.filter(f => filtros.every(([k, v]) => calza(f, k, v)));
  const ord = u.searchParams.get('order');
  if (ord) { const [c, dir] = ord.split(',')[0].split('.'); out = out.slice().sort((a, b) => String(a[c] ?? '').localeCompare(String(b[c] ?? '')) * (dir === 'desc' ? -1 : 1)); }
  if (+u.searchParams.get('offset') > 0) out = [];
  return out;
}
const escrituras = [];
async function rutaBase(r, tablas) {
  const req = r.request(), u = new URL(req.url());
  if (/\/rpc\//.test(u.pathname)) return r.fallback();
  const t = u.pathname.split('/').pop(), m = req.method();
  if (!tablas[t]) { if (m === 'GET') return r.fulfill({ contentType: 'application/json', body: '[]' }); return r.fulfill({ status: 201, body: '' }); }
  if (m === 'GET') return r.fulfill({ contentType: 'application/json', body: JSON.stringify(filtrar(tablas[t], u)) });
  const body = req.postData() ? JSON.parse(req.postData()) : null;
  escrituras.push({ t, m, q: u.search, body });
  if (m === 'POST') {
    const nuevas = (Array.isArray(body) ? body : [body]).map(x => ({ created_at: new Date().toISOString(), ...x }));
    nuevas.forEach(x => { x.id = Math.max(0, ...tablas[t].map(y => y.id || 0)) + 1; tablas[t].push(x); });
    return /return=representation/.test(req.headers()['prefer'] || '') ? r.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(nuevas) }) : r.fulfill({ status: 201, body: '' });
  }
  if (m === 'PATCH') { filtrar(tablas[t], u).forEach(f => Object.assign(f, body)); return r.fulfill({ status: 204, body: '' }); }
  if (m === 'DELETE') { const fuera = new Set(filtrar(tablas[t], u)); tablas[t] = tablas[t].filter(f => !fuera.has(f)); return r.fulfill({ status: 204, body: '' }); }
  return r.fulfill({ status: 405, body: '' });
}
const etapa = (pid, k) => DB.prod.planificacion_etapas.find(e => e.planificacion_id === pid && e.etapa === k);
const pedido = id => DB.prod.planificacion.find(p => p.id === id);

(async () => {
  const b = await chromium.launch(); const errores = [];
  const ctx = await contexto(b, { tablas: {} }, { viewport: { width: 1366, height: 860 }, isMobile: false, hasTouch: false, deviceScaleFactor: 1, userAgent: undefined });
  await ctx.route(/ygcsqrylpibhofvetdyh\.supabase\.co\/rest\/v1\//, r => rutaBase(r, DB.prod));
  await ctx.route(/jvgifibnoigpicwklasw\.supabase\.co\/rest\/v1\//, r => rutaBase(r, DB.fichas));
  const p = await ctx.newPage(); p.on('pageerror', e => errores.push(e.message));
  const dialogos = []; p.on('dialog', x => { dialogos.push(x.message()); x.accept(); });
  await p.goto('https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(2500);
  const nueva = await p.evaluate(() => ajustarAdelante(moverDia(F.hoy(), 10)));

  // 1 · Terminados → Ver proyecto → Reabrir
  ok(await p.evaluate(() => PROY.map(x => x.cot).join()) === 'COT-3702', 'al inicio solo COT-3702 está en producción');
  await p.evaluate(async () => { TAB = 'area'; AREA_SEL = 'TERMINADOS'; renderTabs(); await renderArea(); }); await p.waitForTimeout(800);
  await p.evaluate(() => verTerminado(20)); await p.waitForTimeout(800);
  ok(await p.isVisible('#modal >> text=Reabrir: devolver a una etapa'), 'Terminados: el proyecto terminado tiene «Reabrir: devolver a una etapa»');
  await p.click('#modal >> text=Reabrir: devolver a una etapa'); await p.waitForTimeout(800);
  ok(/Hoy: Terminado el/.test(await p.textContent('#modal')), 'el formulario dice cómo está hoy (Terminado el …)');
  ok(await p.inputValue('#re-fecha') === '', 'la entrega comprometida ya pasó: la fecha viene vacía para poner la nueva');
  const opciones = await p.$$eval('#re-dest option', o => o.map(x => x.textContent));
  ok(opciones.length === 9 && /Confección \(hoy terminada\)/.test(opciones.join('|')) && /Desde el inicio/.test(opciones.join('|')), 'ofrece cada etapa de su flujo y «Desde el inicio»: ' + opciones.slice(1).join(' | '));
  await p.selectOption('#re-dest', 'CONFEC'); await p.waitForTimeout(200);
  const marcadas = await p.$$eval('#re-etapas input', i => i.filter(x => x.checked).map(x => x.dataset.k + (x.disabled ? '*' : '')).join());
  ok(marcadas === 'CONFEC,ENTREGA*', 'Confección y lo que viene después (Listo para entrega, fijo) se rehacen: ' + marcadas);
  ok(/Quedan terminadas: Armado de mesa, Corte, Revisión de mesa, Ploteo, Sublimación/.test(await p.textContent('#re-res')), 'dice qué queda terminado');
  // validaciones
  await p.click('#re-ok'); await p.waitForTimeout(200);
  ok(/Escribe qué falta/.test(await p.textContent('#re-err')), 'sin «qué falta» no se guarda');
  await p.fill('#re-falta', '8 camisetas talla M');
  await p.click('#re-ok'); await p.waitForTimeout(200);
  ok(/fecha de entrega/.test(await p.textContent('#re-err')), 'sin fecha nueva no se guarda');
  await p.fill('#re-fecha', d(-1)); await p.click('#re-ok'); await p.waitForTimeout(200);
  ok(/ya pasó/.test(await p.textContent('#re-err')), 'con una fecha pasada no se guarda');
  ok(!escrituras.length, 'las validaciones no escriben nada en la base');
  // Corte también (va en paralelo): se puede sumar a mano
  await p.check('#re-etapas input[data-k="CORTE"]'); await p.waitForTimeout(200);
  const marcadas2 = await p.$$eval('#re-etapas input', i => i.filter(x => x.checked).map(x => x.dataset.k + (x.disabled ? '*' : '')).join());
  ok(marcadas2 === 'CORTE,SUBL*,CONFEC,ENTREGA*', 'al marcar Corte se suman Sublimación (depende de Corte), Confección y Listo para entrega: ' + marcadas2);
  await p.uncheck('#re-etapas input[data-k="CORTE"]'); await p.waitForTimeout(200);
  await p.fill('#re-fecha', nueva);
  await p.click('#re-ok'); await p.waitForTimeout(2500);
  ok(/vuelve a Confección/.test(dialogos.join('|')), 'pide confirmar: «vuelve a Confección»');
  const p20 = pedido(20);
  ok(p20.estado_general === 'en_produccion', 'COT-3700 vuelve a «en producción» (' + p20.estado_general + ')');
  ok(p20.fecha_entrega_cliente === nueva && p20.fecha_termino_interno < nueva, 'guarda la nueva entrega ' + nueva + ' y su término interno ' + p20.fecha_termino_interno);
  ok(etapa(20, 'CONFEC').estado === 'pendiente' && etapa(20, 'CONFEC').fecha_termino_real === null && etapa(20, 'ENTREGA').estado === 'pendiente', 'Confección y Listo para entrega quedan pendientes, sin fechas reales');
  ok(etapa(20, 'SUBL').estado === 'terminado' && etapa(20, 'SUBL').fecha_termino_real === ts(-6) && etapa(20, 'CORTE').estado === 'terminado', 'Sublimación y Corte siguen terminados con su fecha original');
  ok(etapa(20, 'CONFEC').fecha_limite >= d(0) && etapa(20, 'CONFEC').fecha_limite <= nueva, 'Confección queda replanificada hacia la nueva entrega (límite ' + etapa(20, 'CONFEC').fecha_limite + ')');
  const lg = DB.prod.planificacion_log.find(x => x.planificacion_id === 20 && x.accion === 'reingreso');
  const dma = s => s.slice(8, 10) + '-' + s.slice(5, 7) + '-' + s.slice(0, 4);
  ok(lg && lg.etapa === 'CONFEC' && lg.valor_anterior === `Terminado el ${dma(d(-2))} · entrega comprometida ${dma(d(-3))}` && lg.observacion === 'Falta: 8 camisetas talla M',
    'historial: ' + (lg ? `${lg.valor_anterior} → ${lg.valor_nuevo} · ${lg.observacion} · ${lg.usuario}` : 'sin registro'));
  ok(DB.prod.planificacion_log.some(x => x.planificacion_id === 20 && x.accion === 'cambio_fecha_entrega' && /también se actualizó en la ficha/.test(x.observacion)), 'historial: cambio de fecha, también en la ficha');
  const fi = DB.fichas.fichas_tallas[0];
  ok(fi.entrega_cliente === nueva && fi.entrega_interna === null, 'la ficha en Fichas toma la nueva fecha (y su entrega interna vencida se borra)');
  // se ve como reingreso
  ok(await p.evaluate(() => PROY.some(x => x.id === 20)), 'COT-3700 aparece en Proyectos');
  ok(/Reingreso.*vuelve a Confección.*falta 8 camisetas talla M/.test(await p.textContent('#modal')), 'el detalle muestra «Reingreso … vuelve a Confección: falta 8 camisetas talla M»');
  await p.evaluate(() => cerrarModal());
  await p.evaluate(async () => { TAB = 'area'; AREA_SEL = 'CONFEC'; renderTabs(); await renderArea(); }); await p.waitForTimeout(600);
  ok(/↺ Reingreso: falta 8 camisetas talla M/.test(await p.textContent('#view-area')), 'Confección ve el pedido con «↺ Reingreso: falta 8 camisetas talla M»');
  await p.screenshot({ path: 'movil/reingreso_area.png', fullPage: false });
  await p.evaluate(() => { TAB = 'proyectos'; renderTabs(); renderVista(); }); await p.waitForTimeout(500);
  ok(/↺ Reingreso/.test(await p.textContent('#view-proyectos')), 'Proyectos marca el pedido con «↺ Reingreso»');

  // 2 · pedido en curso (Confección) vuelve a Armado de mesa: Corte (en paralelo) queda como estaba
  escrituras.length = 0;
  await p.evaluate(() => verProyecto(22)); await p.waitForTimeout(500);
  await p.click('#modal >> text=Devolver a una etapa'); await p.waitForTimeout(800);
  ok(await p.inputValue('#re-fecha') === dh(12), 'pedido en curso: propone su misma fecha de entrega');
  ok(await p.isVisible('#modal >> text=Devolver a Diseño o Ingreso'), 'ofrece el camino a «Devolver a Diseño o Ingreso»');
  await p.selectOption('#re-dest', 'ARMADO'); await p.waitForTimeout(200);
  const m3 = await p.$$eval('#re-etapas input', i => i.filter(x => x.checked).map(x => x.dataset.k + (x.disabled ? '*' : '')).join());
  ok(m3 === 'ARMADO,REVISION*,PLOTEO*,SUBL*,CONFEC*,ENTREGA*', 'Armado de mesa arrastra todo menos Corte: ' + m3);
  await p.fill('#re-falta', 'error de diseño en el escudo'); await p.click('#re-ok'); await p.waitForTimeout(2000);
  if (await p.isVisible('#re-err .aviso')) console.log('      aviso:', await p.textContent('#re-err'));
  ok(['ARMADO', 'REVISION', 'PLOTEO', 'SUBL', 'CONFEC', 'ENTREGA'].every(k => etapa(22, k).estado === 'pendiente') && etapa(22, 'CORTE').estado === 'terminado', 'Armado a Listo para entrega pendientes; Corte sigue terminado');
  ok(etapa(22, 'CONFEC').fecha_inicio_real === null && etapa(22, 'CONFEC').responsable === null, 'Confección (estaba en proceso) queda sin inicio ni responsable');
  ok(!escrituras.some(w => w.t === 'fichas_tallas') && pedido(22).fecha_entrega_cliente === dh(12), 'misma fecha: no cambia la fecha ni la ficha');
  const lg22 = DB.prod.planificacion_log.find(x => x.planificacion_id === 22 && x.accion === 'reingreso');
  ok(lg22 && lg22.valor_anterior === 'Confección', 'historial del pedido en curso: desde «Confección» (' + (lg22 && lg22.valor_anterior) + ')');
  await p.evaluate(() => cerrarModal());

  // 3 · terminado con el detalle ya borrado (90 días): se vuelven a crear sus etapas
  escrituras.length = 0;
  await p.evaluate(async () => { TAB = 'area'; AREA_SEL = 'TERMINADOS'; renderTabs(); await renderArea(); verTerminado(21); }); await p.waitForTimeout(900);
  await p.click('#modal >> text=Reabrir: devolver a una etapa'); await p.waitForTimeout(800);
  ok(/sus etapas se vuelven a crear/.test(await p.textContent('#modal')), 'avisa que el detalle se borró y que las etapas se vuelven a crear');
  await p.selectOption('#re-dest', 'SUBL'); await p.fill('#re-falta', 'reimprimir 4 camisetas'); await p.fill('#re-fecha', nueva);
  await p.click('#re-ok'); await p.waitForTimeout(2000);
  const e21 = DB.prod.planificacion_etapas.filter(e => e.planificacion_id === 21).map(e => e.etapa + ':' + e.estado).join();
  ok(e21 === 'ARMADO:terminado,CORTE:terminado,REVISION:terminado,PLOTEO:terminado,SUBL:pendiente,CONFEC:pendiente,ENTREGA:pendiente', 'etapas creadas: las anteriores terminadas, Sublimación y las siguientes pendientes · ' + e21);
  ok(pedido(21).estado_general === 'en_produccion' && pedido(21).resumido_at === null && pedido(21).terminado_at === null, 'vuelve a producción y deja de estar marcado como resumido');
  const lg21 = DB.prod.planificacion_log.find(x => x.planificacion_id === 21 && x.accion === 'reingreso');
  ok(lg21 && lg21.valor_anterior === `Terminado el ${dma(d(-100))} · entrega comprometida ${dma(d(-101))}`, 'historial: primera fecha de término desde el resumen (' + (lg21 && lg21.valor_anterior) + ')');
  await p.evaluate(() => cerrarModal());

  // 4 · Gerencia: al terminarse de nuevo, el cumplimiento usa la primera fecha de término y la entrega de entonces
  Object.assign(pedido(20), { estado_general: 'entregado' });
  Object.assign(etapa(20, 'ENTREGA'), { estado: 'terminado', fecha_termino_real: ts(9) });
  await p.evaluate(async () => { ENTREGADOS = null; TAB = 'gerencia'; renderTabs(); await renderGerencia(); }); await p.waitForTimeout(800);
  const fila = await p.$$eval('#view-gerencia tr', t => t.map(r => r.textContent).find(x => /COT-3700/.test(x)) || '');
  const corta = s => s.slice(8, 10) + '/' + s.slice(5, 7);
  const dt = await p.evaluate(([a, b]) => diffHabiles(a, b), [d(-3), d(-2)]), res = dt > 0 ? dt + ' días tarde' : 'A tiempo';
  ok(/reabierto/.test(fila) && fila.includes(corta(d(-3))) && fila.includes(corta(d(-2))) && fila.includes(res), 'Gerencia: COT-3700 «reabierto», comprometida ' + corta(d(-3)) + ', entregada ' + corta(d(-2)) + ' (la primera vez) · ' + fila.replace(/\s+/g, ' '));
  ok(errores.length === 0, 'sin errores de JavaScript ' + errores.join(' | '));
  await b.close(); console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
