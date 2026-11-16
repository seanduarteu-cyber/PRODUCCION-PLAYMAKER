// Costeo de prendas en Planificación: registro del corte (kg por tela y merma) y del ploteo (metros) al terminar,
// pestaña «Costeo» (tela, insumos por consumo, confección, ploteo y sublimación, gasto general de los 3 meses
// anteriores según Ventas, margen y precio sugerido), consumo de insumos por molde y clasificación de gastos.
// Bases simuladas (Producción, Fichas y Ventas), con estado.
const { chromium, contexto } = require('./comun_movil');
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const ahora = new Date().toISOString();
const moldes = require('./datos_moldes_catalogo.json').map(m => Object.assign({}, m));
moldes.forEach(m => {
  if (m.numero === 18) m.piezas = [{ pieza: 'Delantero', cant: 1, consumo: 0.5 }, { pieza: 'Espalda', cant: 1, consumo: 0.5 }, { pieza: 'Manga', cant: 2, consumo: 0.3 }];
  if (m.numero === 46) m.piezas = [{ pieza: 'Delantero', cant: 1, consumo: 0.4 }, { pieza: 'Trasero', cant: 1, consumo: 0.4 }];
});
// Producción
const proys = [
  { id: 1, cot: 'COT-4000', cliente: 'Club Costeo', prendas: 10, desglose: { '18 · FUTHOMU02': 8, '46 · BK-SH': 2, 'VINILO': true }, fecha_ingreso_ficha: '2026-11-05',
    fecha_entrega_cliente: '2026-12-10', fecha_termino_interno: '2026-12-05', tipo: 'normal', requiere_estampado: false, requiere_sublimacion: true, estado_general: 'en_produccion', created_at: ahora },
  { id: 2, cot: 'COT-4001', cliente: 'Club Estimado', prendas: 8, desglose: { '18 · FUTHOMU02': 8 }, fecha_ingreso_ficha: '2026-11-06',
    fecha_entrega_cliente: '2026-12-12', fecha_termino_interno: '2026-12-07', tipo: 'normal', requiere_estampado: false, requiere_sublimacion: true, estado_general: 'en_produccion', created_at: ahora }];
const ETS = ['ARMADO', 'CORTE', 'REVISION', 'PLOTEO', 'SUBL', 'CONFEC', 'ENTREGA'];
let eid = 1; const etapas = [];
proys.forEach(p => ETS.forEach(k => etapas.push({ id: eid++, planificacion_id: p.id, etapa: k, estado: k === 'CORTE' ? 'en_proceso' : k === 'ARMADO' ? 'terminado' : 'pendiente',
  fecha_limite: '2026-12-01', fecha_inicio_real: k === 'CORTE' || k === 'ARMADO' ? ahora : null, fecha_termino_real: k === 'ARMADO' ? ahora : null })));
const asignaciones = [{ id: 1, planificacion_id: 1, cot: 'COT-4000', etapa: 'CORTE', ejecutante_id: 1, ejecutante: 'Pedro Corte', tipo_prenda: '18 · FUTHOMU02', cantidad: 10, created_at: ahora },
  { id: 2, planificacion_id: 1, cot: 'COT-4000', etapa: 'CONFEC', ejecutante_id: 2, ejecutante: 'Taller Las Rosas', tipo_prenda: '18 · FUTHOMU02', cantidad: 8, precio_unit: 3000, created_at: ahora },
  { id: 3, planificacion_id: 1, cot: 'COT-4000', etapa: 'CONFEC', ejecutante_id: 2, ejecutante: 'Taller Las Rosas', tipo_prenda: '46 · BK-SH', cantidad: 2, precio_unit: 2000, created_at: ahora },
  { id: 4, planificacion_id: 2, cot: 'COT-4001', etapa: 'CORTE', ejecutante_id: 1, ejecutante: 'Pedro Corte', tipo_prenda: '18 · FUTHOMU02', cantidad: 8, created_at: ahora }];
const insumos = [
  { id: 1, nombre: 'Pro', categoria: 'Tela', unidad: 'kg', precio: 9000, rendimiento: 3, stock: 50, activo: true },
  { id: 2, nombre: 'Nacional', categoria: 'Tela', unidad: 'm', precio: 2500, rendimiento: 4, stock: 200, activo: true },
  { id: 3, nombre: 'Elástico', categoria: 'Elástico', unidad: 'm', precio: 300, stock: 100, activo: true },
  { id: 4, nombre: 'Etiqueta', categoria: 'Etiqueta', unidad: 'unid', precio: 50, stock: 1000, activo: true },
  { id: 5, nombre: 'Bolsa', categoria: 'Embalaje', unidad: 'unid', precio: 80, stock: 1000, activo: true },
  { id: 6, nombre: 'Papel sublimación', categoria: 'Papel', unidad: 'm', precio: 400, stock: 500, activo: true },
  { id: 7, nombre: 'Tinta', categoria: 'Tinta', unidad: 'litro', precio: 20000, stock: 10, activo: true },
  { id: 8, nombre: 'Papel protección', categoria: 'Papel', unidad: 'm', precio: 150, stock: 500, activo: true }];
let costeo = [], cid = 1;
let bom = [{ id: 1, molde: '*', insumo_id: 4, cantidad: 1 }, { id: 2, molde: '*', insumo_id: 5, cantidad: 1 }, { id: 3, molde: '46', insumo_id: 3, cantidad: 0.9 }], bid = 4;
let movs = [{ id: 1, insumo_id: 1, tipo: 'consumo', cantidad: -2.7, planificacion_id: 1, cot: 'COT-4000', nota: 'Consumo del pedido al ingresar a producción' }], mid = 2;
let config = [{ clave: 'costeo_valores', valor: JSON.stringify({ papel: '6', tinta: '7', tintaM: 0.01, prot: '8', protF: 1, margen: 30 }) }];
// Fichas
const ficha = { id: 1, ref: 'COT-4000', proyecto: 'Uniformes', cliente: 'Club Costeo', estado: 'abierto', created_at: ahora, items: [{ prenda: 'camiseta', cant: 8 }, { prenda: 'short', cant: 2 }],
  specs: { camiseta: { tela: 'Pro', moldes: { Masculino: 'FUTHOMU02|18' }, despiece: { molde: '18 · FUTHOMU02', piezas: [{ pieza: 'Delantero', tela: 'Pro' }, { pieza: 'Espalda', tela: 'Pro' }, { pieza: 'Manga', tela: 'Nacional' }] } },
    short: { tela: 'Nacional', moldes: { Masculino: 'BK-SH|46' } } }, imagenes: [] };
const dets = Array.from({ length: 8 }, (_, i) => ({ id: 'p' + i, ref: 'COT-4000', calce: 'Masculino', manga: 'Corta', tallas: Object.assign({ camiseta: ['S', 'M'][i % 2] }, i < 2 ? { short: 'M' } : {}), created_at: ahora }));
// COT-4001: sin corte registrado, la tela se estima con el consumo teórico de su ficha (8 m de Pro y 2,4 m de Nacional)
const ficha2 = Object.assign({}, ficha, { id: 2, ref: 'COT-4001', items: [{ prenda: 'camiseta', cant: 8 }], specs: { camiseta: ficha.specs.camiseta } });
const dets2 = Array.from({ length: 8 }, (_, i) => ({ id: 'q' + i, ref: 'COT-4001', calce: 'Masculino', manga: 'Corta', tallas: { camiseta: 'M' }, created_at: ahora }));
// Ventas: ventas netas de agosto a octubre (3.000.000) y gastos; noviembre usa esos 3 meses
const ventasPed = [{ id: 1, cot: '4000', fecha: '2026-11-03', neto: 300000, total: 357000, cliente: 'Club Costeo', cantidad: 10 },
  { id: 2, cot: '3900', fecha: '2026-08-10', neto: 1000000 }, { id: 3, cot: '3901', fecha: '2026-09-10', neto: 1000000 }, { id: 4, cot: '3902', fecha: '2026-10-10', neto: 1000000 }];
const gastos = [{ id: 1, fecha: '2026-08-05', monto: 300000, categoria: 'REMUNERACIONES', proveedor: '' }, { id: 2, fecha: '2026-09-05', monto: 150000, categoria: 'ARRIENDO', proveedor: 'Inmobiliaria' },
  { id: 3, fecha: '2026-10-05', monto: 500000, categoria: 'TELAS', proveedor: 'Textil' }, { id: 4, fecha: '2026-10-06', monto: 200000, categoria: 'HONORARIOS', proveedor: 'Taller Juan Pérez' },
  { id: 5, fecha: '2026-10-07', monto: 100000, categoria: 'HONORARIOS', proveedor: 'Antonia Hermosilla' }, { id: 6, fecha: '2026-10-08', monto: 80000, categoria: 'IMPUESTO SII', proveedor: 'SII' }];

const datos = { tablas: { planificacion: u => /select=cot&/.test(u.search) ? proys.map(p => ({ cot: p.cot })) : proys,
  plan_usuarios: [{ usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'], activo: true }],
  plan_ejecutantes: [{ id: 1, nombre: 'Pedro Corte', area: 'Corte', activo: true }, { id: 2, nombre: 'Taller Las Rosas', area: 'Confección', activo: true }],
  plan_tarifas: [{ tipo: '18 · FUTHOMU02', precio: 3000 }, { tipo: '46 · BK-SH', precio: 2000 }],
  plan_insumos_stock: insumos, plan_insumos: insumos, moldes, fichas_tallas: [ficha, ficha2], fichas_detalle: dets.concat(dets2), catalogo_tecnico: [], pedidos: ventasPed, gastos } };

(async () => {
  const b = await chromium.launch();
  const ctx = await contexto(b, datos, { viewport: { width: 1366, height: 860 }, isMobile: false, hasTouch: false, userAgent: undefined, deviceScaleFactor: 1 });
  const envios = [];
  const filtro = (u, filas) => { let r = filas; for (const [k, v] of u.searchParams) {
    if (['select', 'order', 'limit', 'offset', 'on_conflict'].includes(k)) continue;
    const m = v.match(/^(eq|in)\.(.*)$/); if (!m) continue;
    const vals = m[1] === 'eq' ? [m[2]] : m[2].replace(/^\(|\)$/g, '').split(',').map(x => x.replace(/^"|"$/g, ''));
    r = r.filter(x => vals.includes(String(x[k]))); } return r; };
  const tablaViva = { plan_costeo: () => costeo, plan_insumos_molde: () => bom, plan_insumos_mov: () => movs, plan_config: () => config, planificacion_etapas: () => etapas, plan_asignaciones: () => asignaciones };
  await ctx.route(/ygcsqrylpibhofvetdyh\.supabase\.co\/rest\/v1\/(plan_costeo|plan_insumos_molde|plan_insumos_mov|plan_config|planificacion_etapas|plan_asignaciones)/, r => {
    const q = r.request(), u = new URL(q.url()), t = u.pathname.split('/').pop(), filas = tablaViva[t]();
    const d = q.postData() ? JSON.parse(q.postData()) : null;
    if (q.method() !== 'GET') envios.push({ m: q.method(), t, u: decodeURIComponent(u.search), d });
    if (q.method() === 'GET') return r.fulfill({ contentType: 'application/json', body: JSON.stringify(filtro(u, filas)) });
    if (q.method() === 'DELETE') { const quitar = filtro(u, filas); quitar.forEach(x => filas.splice(filas.indexOf(x), 1)); return r.fulfill({ contentType: 'application/json', body: '[]' }); }
    if (q.method() === 'PATCH') { filtro(u, filas).forEach(x => Object.assign(x, d)); return r.fulfill({ contentType: 'application/json', body: '[]' }); }
    const claves = (u.searchParams.get('on_conflict') || '').split(',').filter(Boolean);
    [].concat(d).forEach(x => { const ya = claves.length && filas.find(y => claves.every(k => String(y[k] ?? '') === String(x[k] ?? '')));
      if (ya) Object.assign(ya, x); else if (t === 'plan_config') { const c = filas.find(y => y.clave === x.clave); if (c) Object.assign(c, x); else filas.push(x); }
      else filas.push(Object.assign({ id: t === 'plan_costeo' ? cid++ : t === 'plan_insumos_molde' ? bid++ : mid++ }, x)); });
    return r.fulfill({ contentType: 'application/json', body: '[]' });
  });
  const p = await ctx.newPage(); const errores = []; p.on('pageerror', e => errores.push(e.message)); p.on('dialog', x => x.accept());
  await p.goto('https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(3000);
  const tabs = await p.evaluate(() => tabsPara());
  ok(tabs.includes('costeo'), 'administración ve la pestaña «Costeo»: ' + tabs.join(','));

  // 1 · Corte: al terminar pide los kilos de cada tela del despiece
  await p.evaluate(() => { AREA_SEL = 'CORTE'; irTab('area'); }); await p.waitForTimeout(800);
  ok(/Registrar kilos/.test(await p.innerText('#view-area')), 'la tarjeta de Corte tiene «Registrar kilos»');
  await p.evaluate(() => accionEtapa(1, 'CORTE', 'terminar')); await p.waitForTimeout(1200);
  const modal = await p.innerText('#modal');
  ok(/Corte · COT-4000/.test(modal) && /Pro/.test(modal) && /Nacional/.test(modal), 'al terminar se abre el registro con las telas de la ficha (Pro y Nacional)');
  ok(/8 m · 2,67 kg/.test(modal) && /Terminar sin registrar/.test(modal), 'muestra el consumo teórico (8 m ≈ 2,67 kg de Pro) y permite terminar sin registrar');
  ok(!etapas.find(e => e.planificacion_id === 1 && e.etapa === 'CORTE').fecha_termino_real, 'el corte aún no se termina');
  const idx = await p.$$eval('#rc-telas tr', trs => trs.slice(1).map(t => t.querySelector('b').textContent));
  const iPro = idx.indexOf('Pro'), iNac = idx.indexOf('Nacional');
  await p.fill('#rc-c-' + iPro, '3'); await p.fill('#rc-m-' + iPro, '0.5'); await p.fill('#rc-c-' + iNac, '1.2'); await p.fill('#rc-m-' + iNac, '0.3'); await p.fill('#rc-prendas', '10');
  ok(await p.textContent('#rc-p-' + iPro) === '14,3%', '% de merma de Pro al escribir: ' + await p.textContent('#rc-p-' + iPro));
  envios.length = 0;
  await p.click('#modal .btn.pri'); await p.waitForTimeout(1800);
  const cProA = costeo.find(x => x.etapa === 'CORTE' && x.tela === 'Pro'), cNac = costeo.find(x => x.etapa === 'CORTE' && x.tela === 'Nacional');
  ok(cProA && +cProA.kg_cortado === 3 && +cProA.kg_merma === 0.5 && cProA.prendas === 10 && cNac && +cNac.kg_cortado === 1.2, 'quedan los kilos de cada tela y las prendas cortadas');
  const real = movs.filter(m => m.planificacion_id === 1 && m.tipo === 'consumo');
  ok(real.length === 2 && real.find(m => m.insumo_id === 1).cantidad === -3.5 && real.find(m => m.insumo_id === 2).cantidad === -6 && !real.some(m => /al ingresar/.test(m.nota)),
    'el stock de tela queda con el consumo real (Pro −3,5 kg; Nacional −6 m = 1,5 kg × 4 m/kg) en vez del teórico');
  ok(etapas.find(e => e.planificacion_id === 1 && e.etapa === 'CORTE').estado === 'terminado', 'y el corte se termina');

  // 2 · Ploteo: metros ploteados → papel, tinta y protección
  await p.evaluate(() => abrirRegistroCosteo(1, 'PLOTEO')); await p.waitForTimeout(600);
  await p.fill('#rc-metros', '20'); await p.click('#modal .btn.pri'); await p.waitForTimeout(1200);
  const mp = movs.filter(m => m.planificacion_id === 1 && /Ploteo/.test(m.nota || '')).map(m => m.insumo_id + ':' + m.cantidad).sort().join(' ');
  ok(costeo.some(x => x.etapa === 'PLOTEO' && +x.metros === 20) && mp === '6:-20 7:-0.2 8:-20', 'ploteo: 20 m, y se descuentan papel 20 m, tinta 0,2 l y protección 20 m (' + mp + ')');

  // 3 · pestaña Costeo
  await p.evaluate(() => irTab('costeo')); await p.waitForTimeout(1800);
  const fila = await p.$$eval('#cs-tabla tr', trs => trs.map(t => t.innerText.replace(/\s+/g, ' ')));
  const f1 = fila.find(t => /COT-4000/.test(t)) || '', f2 = fila.find(t => /COT-4001/.test(t)) || '';
  // tela 31.500 + 15.000 · insumos 1.840 · confección 28.000 · ploteo 15.000 · directo 91.340 · GG 18,3% de 300.000 = 55.000 · total 146.340
  ok(/\$46\.500/.test(f1) && /\$1\.840/.test(f1) && /\$28\.000/.test(f1) && /\$15\.000/.test(f1), 'COT-4000: tela 46.500, insumos 1.840, confección 28.000, ploteo y subl. 15.000: ' + f1);
  ok(/\$55\.000 18,3%/.test(f1) && /\$146\.340/.test(f1) && /\$14\.634/.test(f1) && /\$300\.000/.test(f1) && /51,2%/.test(f1), 'gasto general 18,3% (55.000), total 146.340, 14.634 por prenda, margen 51,2%');
  ok(/\$30\.000 estimada/.test(f2), 'COT-4001: tela estimada con el consumo teórico (8 m × $3.000 + 2,4 m × $2.500 = $30.000)');
  ok(/estimada/.test(f2) && /falta: registro del corte/.test(f2), 'COT-4001 sin corte: tela estimada y avisa qué falta: ' + f2.slice(0, 160));
  await p.evaluate(() => verCosteo(1)); await p.waitForTimeout(800);
  const det = await p.innerText('#modal');
  ok(/Pro\s+teórico 8 m\s+3 kg\s+0,5 kg\s+14,3%\s+\$9\.000\s+\$31\.500/.test(det), 'detalle: Pro 3 kg + 0,5 merma (14,3%) a $9.000/kg = $31.500');
  ok(/gastos ÷ ventas de agosto 2026, septiembre 2026, octubre 2026, sobre la venta neta/.test(det), 'detalle: el gasto general dice con qué meses se calculó');
  const tipos = await p.$$eval('#modal table', ts => [...ts[ts.length - 1].querySelectorAll('tr')].slice(1).map(r => r.innerText.replace(/\s+/g, ' ')));
  ok(/^18 · FUTHOMU02 .* 8 \$5\.063 \$130 \$3\.000/.test(tipos[0] || '') && /^46 · BK-SH .* 2 \$3\.000 \$400 \$2\.000/.test(tipos[1] || ''),
    'por molde: la camiseta lleva $5.063 de tela, $130 de insumos y $3.000 de confección; el short $3.000, $400 y $2.000: ' + tipos.join(' / '));
  ok(/\$18\.760$/.test(tipos[0] || ''), 'precio sugerido de la camiseta = directo ÷ (1 − 18,3% − 30%): ' + (tipos[0] || ''));
  await p.evaluate(() => cerrarModal());

  // 4 · gasto general: % de cada mes y clasificación (honorarios de talleres fuera; Antonia Hermosilla dentro)
  await p.evaluate(() => { COSTEO_MODO = 'gg'; renderCosteo(); }); await p.waitForTimeout(1200);
  const gg = await p.innerText('#view-costeo');
  ok(/noviembre 2026\s+agosto 2026, septiembre 2026, octubre 2026\s+\$3\.000\.000\s+\$550\.000\s+18,3%/.test(gg), 'noviembre: $550.000 de gastos generales ÷ $3.000.000 de ventas = 18,3%');
  ok(/HONORARIOS/.test(gg) && /Antonia Hermosilla/.test(gg), 'honorarios como costo directo, con la excepción de Antonia Hermosilla');
  await p.evaluate(() => { const c = CATS_GG.indexOf('IMPUESTO SII'); clasificarGasto(c, 'general'); }); await p.waitForTimeout(800);
  const cfg = JSON.parse((config.find(c => c.clave === 'costeo_gastos') || {}).valor || '{}');
  ok(cfg.cat && cfg.cat['IMPUESTO SII'] === 'general' && /21%/.test(await p.innerText('#view-costeo')), 'cambiar la clasificación se guarda y recalcula el % (630.000 ÷ 3.000.000 = 21%)');
  await p.evaluate(() => { const c = CATS_GG.indexOf('IMPUESTO SII'); clasificarGasto(c, 'fuera'); }); await p.waitForTimeout(600);

  // 5 · consumo de insumos por molde
  await p.evaluate(() => { COSTEO_MODO = 'consumo'; BOM_SEL = '18'; renderCosteo(); }); await p.waitForTimeout(900);
  await p.selectOption('#bom-ins', '3'); await p.fill('#bom-cant', '0.5'); await p.click('button:text-is("Agregar")'); await p.waitForTimeout(900);
  ok(bom.some(x => x.molde === '18' && x.insumo_id === 3 && x.cantidad === 0.5), 'agrega elástico 0,5 m por prenda al molde 18');
  ok(/Total por prenda de este molde \(con lo común\): \$280/.test(await p.innerText('#view-costeo')), 'total por prenda del molde 18 con lo común: 150 + 130 = $280');
  await p.evaluate(() => document.querySelector('#view-costeo details').open = true);
  await p.check('[data-bom-copia][value="17"]'); await p.click('text=Copiar a los marcados'); await p.waitForTimeout(900);
  ok(bom.some(x => x.molde === '17' && x.insumo_id === 3 && x.cantidad === 0.5), 'se copia al molde 17');

  // 6 · valores
  await p.evaluate(() => { COSTEO_MODO = 'valores'; renderCosteo(); }); await p.waitForTimeout(700);
  await p.fill('#cv-margen', '40'); await p.click('text=Guardar valores'); await p.waitForTimeout(700);
  ok(JSON.parse(config.find(c => c.clave === 'costeo_valores').valor).margen === 40, 'el margen para el precio sugerido se guarda');

  ok(!errores.length, 'sin errores JS ' + errores.join(' | '));
  await b.close();
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
