// Costeo de prendas en Planificación: registro del corte (kg por tela y merma) y del ploteo (metros) al terminar,
// pestaña «Costeo» (tela, insumos por consumo, confección, ploteo y sublimación, gasto general de los 3 meses
// anteriores según la clasificación de Ventas, en neto), margen y precio sugerido, y consumo de insumos por molde.
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
  { id: 8, nombre: 'Papel protección', categoria: 'Papel', unidad: 'm', precio: 150, stock: 500, activo: true },
  { id: 9, nombre: 'Dry fit', categoria: 'Tela', unidad: 'm', precio: null, rendimiento: null, stock: 0, activo: true }];
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
// Ventas: ventas netas de agosto a octubre (3.000.000, sin la anulada) y gastos ya clasificados (v_gastos_neto, SQL 21B);
// el pedido se cerró en noviembre: usa agosto, septiembre y octubre
const ventasPed = [{ id: 1, cot: '4000', fecha: '2026-11-03', neto: 300000, total: 357000, cliente: 'Club Costeo', cantidad: 10 },
  { id: 2, cot: '3900', fecha: '2026-08-10', neto: 1000000 }, { id: 3, cot: '3901', fecha: '2026-09-10', neto: 1000000 }, { id: 4, cot: '3902', fecha: '2026-10-10', neto: 1000000 },
  { id: 5, cot: '3903', fecha: '2026-10-20', neto: 500000, estado: 'Anulada' }];
const gn = (id, periodo, cuenta_codigo, nivel, estado, monto_bruto, monto_neto, iva_recuperable) => ({ gasto_id: id, periodo, cuenta_codigo, nivel, estado, monto_bruto, monto_neto, origen_iva: 'cuenta', iva_recuperable: !!iva_recuperable });
const vGastosNeto = [gn(1, '2026-08-01', '3.01', '3', 'clasificado', 300000, 300000),          // sueldos de producción
  gn(2, '2026-09-01', '3.07', '3', 'clasificado', 150000, 150000),                                // arriendo: 80/10/10
  gn(3, '2026-10-01', '2.01', '2', 'clasificado', 595000, 500000, true),                          // tela: costo directo, no entra
  gn(4, '2026-10-01', '2.09', '2', 'clasificado', 100000, 100000),                                // comisión: costo directo, no entra
  gn(5, '2026-10-01', '5.02', '5', 'clasificado', 119000, 100000, true),                          // software con factura afecta: en neto
  gn(6, '2026-10-01', 'F.01', 'F', 'clasificado', 80000, 80000),                                  // pago de IVA: fuera
  gn(7, '2026-10-01', null, null, 'revision', 40000, 40000),                                       // en revisión: el % es provisorio
  gn(8, '2026-03-01', '3.01', '3', 'clasificado', 999999, 999999)];                                // antes de abril: no se usa
const planCuentas = [{ codigo: '3.01', nivel: '3', prorrateo: null }, { codigo: '3.07', nivel: '3', prorrateo: 'local' }, { codigo: '5.02', nivel: '5', prorrateo: null }];
const gestionParametros = [{ clave: 'inicio_analisis', valor: '2026-04-01' }, { clave: 'prorrateo_local', valor: { produccion: 80, ventas: 10, administracion: 10 } }];

const datos = { tablas: { planificacion: u => /select=cot&/.test(u.search) ? proys.map(p => ({ cot: p.cot })) : proys,
  plan_usuarios: [{ usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'], activo: true }],
  plan_ejecutantes: [{ id: 1, nombre: 'Pedro Corte', area: 'Corte', activo: true }, { id: 2, nombre: 'Taller Las Rosas', area: 'Confección', activo: true }],
  plan_tarifas: [{ tipo: '18 · FUTHOMU02', precio: 3000 }, { tipo: '46 · BK-SH', precio: 2000 }],
  plan_insumos_stock: insumos, plan_insumos: insumos, moldes, fichas_tallas: [ficha, ficha2], fichas_detalle: dets.concat(dets2), catalogo_tecnico: [], pedidos: ventasPed,
  v_gastos_neto: vGastosNeto, plan_cuentas: planCuentas, gestion_parametros: gestionParametros } };

(async () => {
  const b = await chromium.launch();
  const ctx = await contexto(b, datos, { viewport: { width: 1366, height: 860 }, isMobile: false, hasTouch: false, userAgent: undefined, deviceScaleFactor: 1 });
  const envios = [];
  const filtro = (u, filas) => { let r = filas; for (const [k, v] of u.searchParams) {
    if (['select', 'order', 'limit', 'offset', 'on_conflict'].includes(k)) continue;
    const m = v.match(/^(eq|in)\.(.*)$/); if (!m) continue;
    const vals = m[1] === 'eq' ? [m[2]] : m[2].replace(/^\(|\)$/g, '').split(',').map(x => x.replace(/^"|"$/g, ''));
    r = r.filter(x => vals.includes(String(x[k]))); } return r; };
  const tablaViva = { plan_costeo: () => costeo, plan_insumos_molde: () => bom, plan_insumos_mov: () => movs, plan_config: () => config, planificacion_etapas: () => etapas, plan_asignaciones: () => asignaciones, plan_insumos: () => insumos };
  await ctx.route(/ygcsqrylpibhofvetdyh\.supabase\.co\/rest\/v1\/(plan_costeo|plan_insumos_molde|plan_insumos_mov|plan_config|planificacion_etapas|plan_asignaciones|plan_insumos(?=\?|$))/, r => {
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
  // sin el SQL 23A (precios por proveedor): Precios sigue con un precio por producto
  await ctx.route(/ygcsqrylpibhofvetdyh\.supabase\.co\/rest\/v1\/(plan_insumo_precios|plan_proveedores_estado)/, r => r.fulfill({ status: 404, contentType: 'application/json', body: '{"code":"PGRST205"}' }));
  const p = await ctx.newPage(); const errores = []; p.on('pageerror', e => errores.push(e.message)); p.on('dialog', x => x.accept());
  await p.goto('https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(3000);
  const tabs = await p.evaluate(() => tabsPara());
  ok(tabs.includes('costeo'), 'administración ve la pestaña «Costeo»: ' + tabs.join(','));

  // 1 · Corte: al terminar pide los kilos de cada molde por separado (camisetas y shorts), por cada tela
  await p.evaluate(() => { AREA_SEL = 'CORTE'; irTab('area'); }); await p.waitForTimeout(800);
  ok(/Registrar kilos/.test(await p.innerText('#view-area')), 'la tarjeta de Corte tiene «Registrar kilos»');
  await p.evaluate(() => accionEtapa(1, 'CORTE', 'terminar')); await p.waitForTimeout(1200);
  const modal = await p.innerText('#modal');
  ok(/Corte · COT-4000/.test(modal) && /18 · FUTHOMU02/.test(modal) && /46 · BK-SH/.test(modal) && /Terminar sin registrar/.test(modal), 'al terminar se abre el registro con cada molde del pedido por separado');
  const telasM = await p.$$eval('#rc-moldes > div', ds => ds.map(d => [...d.querySelectorAll('tbody tr, table tr')].slice(1).map(t => (t.querySelector('b') || {}).textContent)));
  ok(telasM[0].join() === 'Pro,Nacional' && telasM[1].join() === 'Nacional', 'la camiseta trae Pro y Nacional; el short, Nacional (de la ficha): ' + JSON.stringify(telasM));
  ok(/8 m · 2,67 kg/.test(modal) && /1,6 m · 0,4 kg/.test(modal), 'teórico de cada molde: camiseta 8 m de Pro (2,67 kg); short 1,6 m de Nacional (0,4 kg)');
  ok(!etapas.find(e => e.planificacion_id === 1 && e.etapa === 'CORTE').fecha_termino_real, 'el corte aún no se termina');
  await p.fill('#rc-c-0-0', '2.5'); await p.fill('#rc-m-0-0', '0.4'); await p.fill('#rc-c-0-1', '0.8'); await p.fill('#rc-m-0-1', '0.2'); await p.fill('#rc-u-0', '8');
  await p.fill('#rc-c-1-0', '0.5'); await p.fill('#rc-m-1-0', '0.1'); await p.fill('#rc-u-1', '2');
  ok(await p.textContent('#rc-p-0-0') === '13,8%' && await p.textContent('#rc-p-1-0') === '16,7%', '% de merma de cada fila al escribir');
  await p.click('#modal .btn.pri'); await p.waitForTimeout(1800);
  const cr = (m, t) => costeo.find(x => x.etapa === 'CORTE' && x.molde === m && x.tela === t);
  ok(cr('18 · FUTHOMU02', 'Pro') && +cr('18 · FUTHOMU02', 'Pro').kg_cortado === 2.5 && cr('18 · FUTHOMU02', 'Pro').prendas === 8 && +cr('18 · FUTHOMU02', 'Nacional').kg_merma === 0.2 &&
    +cr('46 · BK-SH', 'Nacional').kg_cortado === 0.5 && cr('46 · BK-SH', 'Nacional').prendas === 2 && costeo.filter(x => x.etapa === 'CORTE').length === 3, 'quedan los kilos de cada molde y tela, y las prendas cortadas de cada molde');
  ok(String(cr('18 · FUTHOMU02', 'Pro').piezas) === 'Delantero,Espalda' && String(cr('18 · FUTHOMU02', 'Nacional').piezas) === 'Manga' && String(cr('46 · BK-SH', 'Nacional').piezas) === 'Delantero,Trasero',
    'cada tela del corte queda con sus piezas, tomadas de la ficha (camiseta: Pro delantero y espalda, Nacional mangas)');
  const real = movs.filter(m => m.planificacion_id === 1 && m.tipo === 'consumo');
  ok(real.length === 2 && real.find(m => m.insumo_id === 1).cantidad === -2.9 && real.find(m => m.insumo_id === 2).cantidad === -6.4 && !real.some(m => /al ingresar/.test(m.nota)),
    'el stock de tela queda con el consumo real de todos los moldes (Pro −2,9 kg; Nacional −6,4 m = 1,6 kg × 4 m/kg)');
  ok(etapas.find(e => e.planificacion_id === 1 && e.etapa === 'CORTE').estado === 'terminado', 'y el corte se termina');

  // 2 · Ploteo: metros de cada molde → papel, tinta y protección
  await p.evaluate(() => abrirRegistroCosteo(1, 'PLOTEO')); await p.waitForTimeout(600);
  await p.fill('#rc-pm-0', '16'); await p.fill('#rc-pm-1', '4'); await p.click('#modal .btn.pri'); await p.waitForTimeout(1200);
  const mp = movs.filter(m => m.planificacion_id === 1 && /Ploteo/.test(m.nota || '')).map(m => m.insumo_id + ':' + m.cantidad).sort().join(' ');
  ok(costeo.some(x => x.etapa === 'PLOTEO' && x.molde === '18 · FUTHOMU02' && +x.metros === 16) && costeo.some(x => x.etapa === 'PLOTEO' && x.molde === '46 · BK-SH' && +x.metros === 4) &&
    mp === '6:-20 7:-0.2 8:-20', 'ploteo: 16 m de camisetas y 4 m de shorts; se descuentan papel 20 m, tinta 0,2 l y protección 20 m (' + mp + ')');

  // 3 · pestaña Costeo: cada pedido con el costo total de cada molde
  await p.evaluate(() => irTab('costeo')); await p.waitForTimeout(1800);
  const filas = await p.$$eval('#cs-tabla tr', trs => trs.map(t => t.className + '|' + t.innerText.replace(/\s+/g, ' ')));
  const iP = filas.findIndex(t => /COT-4000/.test(t)), cam = filas[iP + 1] || '', sho = filas[iP + 2] || '', ped = filas[iP] || '';
  // camiseta: tela 36.100 · insumos 1.040 · confección 24.000 · ploteo 12.000 · directo 73.140 · GG 46.270 → 119.410 (14.926 c/u)
  // short: tela 6.000 · insumos 800 · confección 4.000 · ploteo 3.000 · directo 13.800 · GG 8.730 → 22.530 (11.265 c/u)
  ok(/^cs-molde\|18 · FUTHOMU02 .*Camiseta.* 8 \$36\.100 \$1\.040 \$24\.000 \$12\.000 \$46\.270 \$119\.410 \$14\.926/.test(cam), 'camisetas: costo total del molde $119.410, $14.926 por prenda: ' + cam);
  ok(/^cs-molde\|46 · BK-SH .*Short.* 2 \$6\.000 \$800 \$4\.000 \$3\.000 \$8\.730 \$22\.530 \$11\.265/.test(sho), 'shorts: costo total del molde $22.530, $11.265 por prenda: ' + sho);
  ok(/^cs-ped\|COT-4000 .* 10 \$42\.100 \$1\.840 \$28\.000 \$15\.000 \$55\.000 \$141\.940 \$300\.000 52,7%/.test(ped), 'pedido: suma de sus moldes ($141.940), venta $300.000, margen 52,7%: ' + ped);
  const f2 = filas.slice(filas.findIndex(t => /COT-4001/.test(t))).join(' / ');
  ok(/\$30\.000 estimada/.test(f2) && /falta: registro del corte/.test(f2), 'COT-4001 sin corte: tela estimada con el consumo teórico ($30.000) y avisa qué falta');
  await p.evaluate(() => verCosteo(1)); await p.waitForTimeout(800);
  const det = await p.innerText('#modal');
  ok(/18 · FUTHOMU02 · Camiseta — 8 prendas \(8 cortadas\)/.test(det) && /46 · BK-SH · Short.* — 2 prendas \(2 cortadas\)/.test(det), 'detalle: una sección por molde con sus prendas cortadas');
  ok(/Pro\s+teórico 8 m\s+2,5 kg\s+0,4 kg\s+13,8%\s+\$9\.000\s+\$26\.100/.test(det), 'detalle camiseta: Pro 2,5 kg + 0,4 merma a $9.000/kg = $26.100');
  ok(/Costo total del molde\s+\$119\.410\s+Costo por prenda\s+\$14\.926\s+Precio sugerido por prenda\s+costo directo[^\n]*\s+\$17\.695/.test(det), 'detalle: costo total del molde, por prenda y precio sugerido (directo ÷ (1 − 18,3% − 30%))');
  ok(/gasto general ÷ ventas netas de agosto 2026, septiembre 2026, octubre 2026, sobre la venta neta · provisorio/.test(det), 'detalle: el gasto general dice con qué meses se calculó y que es provisorio');
  // otro costo de un molde
  await p.evaluate(() => abrirOtroCosto(1)); await p.waitForTimeout(400);
  await p.fill('#oc-con', 'Bordado escudo'); await p.fill('#oc-monto', '8000'); await p.selectOption('#oc-molde', '18 · FUTHOMU02'); await p.click('#modal .btn.pri'); await p.waitForTimeout(900);
  ok(costeo.some(x => x.etapa === 'OTRO' && x.molde === '18 · FUTHOMU02' && x.tela === 'Bordado escudo' && x.monto === 8000) && /Bordado escudo\s+otro costo\s+\$8\.000/.test(await p.innerText('#modal')), 'otro costo asignado a las camisetas');
  await p.evaluate(() => cerrarModal());
  // resumen por molde en el período
  await p.evaluate(() => { COSTEO_MODO = 'moldes'; renderCosteo(); }); await p.waitForTimeout(900);
  const pm = await p.$$eval('#cs-moldes tr', trs => trs.slice(1).map(t => t.innerText.replace(/\s+/g, ' ')));
  ok(pm.length === 2 && /^18 · FUTHOMU02 .* 2 16 /.test(pm[0]) && /^46 · BK-SH .* 1 2 /.test(pm[1]), 'por molde: la camiseta en 2 pedidos (16 prendas) y el short en 1: ' + pm.join(' / '));

  // 4 · gasto general desde la clasificación de Ventas, en neto: cada mes y el % de los 3 meses anteriores
  await p.evaluate(() => { COSTEO_MODO = 'gg'; renderCosteo(); }); await p.waitForTimeout(1200);
  const ggP = (await p.innerText('#gg-pedidos')).replace(/\s+/g, ' '), ggM = await p.$$eval('#gg-meses tr', trs => trs.slice(1).map(t => t.innerText.replace(/\s+/g, ' ')));
  ok(/noviembre 2026 agosto 2026, septiembre 2026, octubre 2026 \$3\.000\.000 \$550\.000 18,3% provisorio/.test(ggP), 'pedidos de noviembre: $550.000 de gasto general ÷ $3.000.000 de ventas netas = 18,3%, provisorio: ' + ggP.slice(0, 200));
  const fM = m => ggM.find(x => x.startsWith(m)) || '';
  ok(/^octubre 2026 \$1\.000\.000 \$0 \$0 \$100\.000 \$100\.000 10% \$40\.000 1 gasto$/.test(fM('octubre')), 'octubre: sin la venta anulada; tela, comisión e IVA no entran; software en neto; $40.000 en revisión: ' + fM('octubre'));
  ok(/^septiembre 2026 \$1\.000\.000 \$120\.000 \$15\.000 \$15\.000 \$150\.000 15% —$/.test(fM('septiembre')), 'septiembre: arriendo repartido 80/10/10: ' + fM('septiembre'));
  ok(/^agosto 2026 \$1\.000\.000 \$300\.000 \$0 \$0 \$300\.000 30% —$/.test(fM('agosto')), 'agosto: sueldos de producción: ' + fM('agosto'));
  ok(!ggM.some(x => /marzo/.test(x)) && /\$19\.000 de IVA se descontaron según el IVA habitual de la cuenta/.test(await p.innerText('#view-costeo')), 'marzo no aparece (el análisis parte en abril) y avisa el IVA descontado por supuesto');
  // sin el SQL 21B en Ventas: avisa en vez de calcular con otra cosa
  await ctx.route(/nnisdusdujcpkrbjqnhe\.supabase\.co\/rest\/v1\/v_gastos_neto/, r => r.fulfill({ status: 404, contentType: 'application/json', body: '{"code":"PGRST205"}' }));
  await p.evaluate(() => { GG_DATOS = null; renderCosteo(); }); await p.waitForTimeout(900);
  ok(/Falta correr el SQL 21B/.test(await p.innerText('#view-costeo')), 'sin SQL 21B: avisa que falta');
  await ctx.unroute(/nnisdusdujcpkrbjqnhe\.supabase\.co\/rest\/v1\/v_gastos_neto/);
  await p.evaluate(() => { GG_DATOS = null; COSTEO_DATOS = null; }); 

  // 5 · consumo de insumos por molde
  await p.evaluate(() => { COSTEO_MODO = 'consumo'; BOM_SEL = '18'; renderCosteo(); }); await p.waitForTimeout(900);
  await p.selectOption('#bom-ins', '3'); await p.fill('#bom-cant', '0.5'); await p.click('button:text-is("Agregar")'); await p.waitForTimeout(900);
  ok(bom.some(x => x.molde === '18' && x.insumo_id === 3 && x.cantidad === 0.5), 'agrega elástico 0,5 m por prenda al molde 18');
  ok(/Total por prenda de este molde \(con lo común\): \$280/.test(await p.innerText('#view-costeo')), 'total por prenda del molde 18 con lo común: 150 + 130 = $280');
  await p.evaluate(() => document.querySelector('#view-costeo details').open = true);
  await p.check('[data-bom-copia][value="17"]'); await p.click('text=Copiar a los marcados'); await p.waitForTimeout(900);
  ok(bom.some(x => x.molde === '17' && x.insumo_id === 3 && x.cantidad === 0.5), 'se copia al molde 17');

  // 6 · precios: todas las telas por kg y todos los insumos en una sola lista
  await p.evaluate(() => { COSTEO_MODO = 'precios'; renderCosteo(); }); await p.waitForTimeout(900);
  ok(/Falta correr el SQL 23A/.test(await p.innerText('#view-costeo')), 'sin el SQL 23A: avisa y sigue con un precio por producto');
  ok(await p.inputValue('#pr-kg-1') === '9000' && await p.inputValue('#pr-kg-2') === '10000' && /\$2\.500\/m/.test(await p.textContent('#pr-eq-2')),
    'telas por kg: Pro $9.000/kg; Nacional (se lleva en metros) $10.000/kg = $2.500/m con 4 m/kg');
  { const tx = (await p.innerText('#view-costeo')).replace(/\s+/g, ' '); ok(/2 de 3 Telas con precio/.test(tx) && /6 de 6 Insumos con precio/.test(tx), 'resumen: 2 de 3 telas y 6 de 6 insumos con precio'); }
  await p.fill('#pr-kg-2', '12000'); await p.dispatchEvent('#pr-kg-2', 'change'); await p.waitForTimeout(700);
  ok(insumos.find(i => i.id === 2).precio === 3000 && /Guardado/.test(await p.textContent('#pr-st-2')) && /\$3\.000\/m/.test(await p.textContent('#pr-eq-2')), 'Nacional a $12.000/kg queda guardado como $3.000 por metro (12.000 ÷ 4 m/kg)');
  await p.fill('#pr-kg-9', '8000'); await p.dispatchEvent('#pr-kg-9', 'change'); await p.waitForTimeout(500);
  ok(!(insumos.find(i => i.id === 9).precio > 0) && /rendimiento/.test(await p.textContent('#pr-st-9')), 'tela en metros sin rendimiento: pide el rendimiento antes de guardar');
  await p.fill('#pr-rd-9', '5'); await p.dispatchEvent('#pr-rd-9', 'change'); await p.waitForTimeout(700);
  ok(insumos.find(i => i.id === 9).precio === 1600 && insumos.find(i => i.id === 9).rendimiento === 5, 'con 5 m/kg se guarda: $8.000/kg = $1.600/m');
  await p.fill('#pr-u-3', '350'); await p.dispatchEvent('#pr-u-3', 'change'); await p.waitForTimeout(700);
  ok(insumos.find(i => i.id === 3).precio === 350 && movs.some(m => m.insumo_id === 3 && m.tipo === 'edicion' && /\$300 → \$350 por m/.test(m.nota)), 'insumo: elástico a $350/m, y queda en el historial del insumo');
  await p.evaluate(() => { PRECIOS_SIN = true; renderCosteo(); }); await p.waitForTimeout(700);
  ok(await p.$$eval('#pr-telas tr[data-ins], #pr-ins tr[data-ins]', t => t.length) === 0, '«Solo sin precio»: ya no queda ninguno sin precio');
  await p.evaluate(() => { PRECIOS_SIN = false; });

  // 7 · valores
  await p.evaluate(() => { COSTEO_MODO = 'valores'; renderCosteo(); }); await p.waitForTimeout(700);
  await p.fill('#cv-margen', '40'); await p.click('#view-costeo .acciones .btn.pri'); await p.waitForTimeout(700);
  ok(JSON.parse(config.find(c => c.clave === 'costeo_valores').valor).margen === 40, 'el margen para el precio sugerido se guarda');

  ok(!errores.length, 'sin errores JS ' + errores.join(' | '));
  await b.close();
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
