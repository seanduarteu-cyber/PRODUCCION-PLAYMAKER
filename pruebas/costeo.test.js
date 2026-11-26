// Costeo de prendas en Planificación: registro del corte (kg por tela y merma) y del ploteo (metros) al terminar,
// pestaña «Costeo» (tela, insumos por consumo, confección, ploteo y sublimación, gasto general de los 3 meses
// anteriores según la clasificación de Ventas, en neto), margen contra la venta (sin precio sugerido), y consumo de insumos por molde.
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
const fichasF = [ficha, ficha2];   // Fichas › fichas_tallas (las secciones 11 y 12 agregan fichas de otros meses)
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
const planCuentas = [{ codigo: '3.01', nivel: '3', prorrateo: null, nombre: 'Sueldos de producción' }, { codigo: '3.07', nivel: '3', prorrateo: 'local' }, { codigo: '5.02', nivel: '5', prorrateo: null },
  { codigo: '3.02', nivel: '3', prorrateo: null, nombre: 'Sueldos de diseño' }, { codigo: '3.03', nivel: '3', prorrateo: 'sueldos' }, { codigo: '4.01', nivel: '4', prorrateo: null }];
const gastosV = [];   // Ventas › gastos: a quién se pagó cada remuneración (se llena en la sección 11)
const gestionParametros = [{ clave: 'inicio_analisis', valor: '2026-04-01' }, { clave: 'prorrateo_local', valor: { produccion: 80, ventas: 10, administracion: 10 } }];

// planificacion filtra por fecha de ingreso como la base (gte / lte), para probar el período de Costeo
const porFecha = u => { const f = u.searchParams.getAll('fecha_ingreso_ficha'), g = (f.find(x => /^gte\./.test(x)) || '').slice(4), l = (f.find(x => /^lte\./.test(x)) || '').slice(4);
  return proys.filter(p => (!g || p.fecha_ingreso_ficha >= g) && (!l || p.fecha_ingreso_ficha <= l)); };
const datos = { tablas: { planificacion: u => /select=cot&/.test(u.search) ? proys.map(p => ({ cot: p.cot })) : porFecha(u),
  plan_usuarios: [{ usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'], activo: true }],
  plan_ejecutantes: [{ id: 1, nombre: 'Pedro Corte', area: 'Corte', activo: true }, { id: 2, nombre: 'Taller Las Rosas', area: 'Confección', activo: true }],
  plan_tarifas: [{ tipo: '18 · FUTHOMU02', precio: 3000 }, { tipo: '46 · BK-SH', precio: 2000 }],
  plan_insumos_stock: insumos, plan_insumos: insumos, moldes, fichas_tallas: fichasF, fichas_detalle: dets.concat(dets2), catalogo_tecnico: [], pedidos: ventasPed,
  v_gastos_neto: vGastosNeto, plan_cuentas: planCuentas, gestion_parametros: gestionParametros, gastos: gastosV } };

(async () => {
  const b = await chromium.launch();
  const ctx = await contexto(b, datos, { viewport: { width: 1366, height: 860 }, isMobile: false, hasTouch: false, userAgent: undefined, deviceScaleFactor: 1 });
  const envios = [];
  const filtro = (u, filas) => { let r = filas; for (const [k, v] of u.searchParams) {
    if (['select', 'order', 'limit', 'offset', 'on_conflict'].includes(k)) continue;
    const lk = v.match(/^like\.(.*)$/);   // like: el * es cualquier cosa (ej.: molde=like.17 · *)
    if (lk) { const re = new RegExp('^' + lk[1].split('*').map(x => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('.*') + '$'); r = r.filter(x => re.test(String(x[k] ?? ''))); continue; }
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
  ok(/^cs-molde\|18 · FUTHOMU02 .*Camiseta.* 8 \$36\.100 \$1\.040 \$24\.000 \$0 \$12\.000 \$46\.270 \$119\.410 \$14\.926/.test(cam), 'camisetas: costo total del molde $119.410, $14.926 por prenda: ' + cam);
  ok(/^cs-molde\|46 · BK-SH .*Short.* 2 \$6\.000 \$800 \$4\.000 \$0 \$3\.000 \$8\.730 \$22\.530 \$11\.265/.test(sho), 'shorts: costo total del molde $22.530, $11.265 por prenda: ' + sho);
  ok(/^cs-ped\|COT-4000 .* 10 \$42\.100 \$1\.840 \$28\.000 \$0 \$15\.000 \$55\.000 \$141\.940 \$300\.000 52,7%/.test(ped), 'pedido: suma de sus moldes ($141.940), venta $300.000, margen 52,7%: ' + ped);
  const f2 = filas.slice(filas.findIndex(t => /COT-4001/.test(t))).join(' / ');
  ok(/\$30\.000 estimada/.test(f2) && /falta: registro del corte/.test(f2), 'COT-4001 sin corte: tela estimada con el consumo teórico ($30.000) y avisa qué falta');
  await p.evaluate(() => verCosteo(1)); await p.waitForTimeout(800);
  const det = await p.innerText('#modal');
  ok(/18 · FUTHOMU02 · Camiseta — 8 prendas \(8 cortadas\)/.test(det) && /46 · BK-SH · Short.* — 2 prendas \(2 cortadas\)/.test(det), 'detalle: una sección por molde con sus prendas cortadas');
  ok(/Pro\s+teórico 8 m\s+2,5 kg\s+0,4 kg\s+13,8%\s+\$9\.000\s+\$26\.100/.test(det), 'detalle camiseta: Pro 2,5 kg + 0,4 merma a $9.000/kg = $26.100');
  ok(/Costo total del molde\s+\$119\.410\s+Costo por prenda\s+\$14\.926/.test(det) && !/Precio sugerido/.test(det), 'detalle: costo total del molde, por prenda y precio sugerido (directo ÷ (1 − 18,3% − 30%))');
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
  ok(/noviembre 2026 agosto 2026, septiembre 2026, octubre 2026 \$3\.000\.000 \$550\.000 18,3% provisorio/.test(ggP), 'pedidos de noviembre: $550.000 de gasto general ÷ $3.000.000 de ventas netas = 18,3%, provisorio (sin prendas vendidas anotadas, la mano de obra interna queda en el gasto general): ' + ggP.slice(0, 200));
  const fM = m => ggM.find(x => x.startsWith(m)) || '';
  ok(/^octubre 2026 \$1\.000\.000 \$0 \$0 \$100\.000 \$100\.000 10% \$40\.000 1 gasto \$0 sugerido: 0 Aceptar sugerido$/.test(fM('octubre')), 'octubre: sin la venta anulada; tela, comisión e IVA no entran; software en neto; $40.000 en revisión: ' + fM('octubre'));
  ok(/^septiembre 2026 \$1\.000\.000 \$120\.000 \$15\.000 \$15\.000 \$150\.000 15% — \$0 sugerido: 0 Aceptar sugerido$/.test(fM('septiembre')), 'septiembre: arriendo repartido 80/10/10: ' + fM('septiembre'));
  ok(/^agosto 2026 \$1\.000\.000 \$0 \$0 \$0 \$0 0% — \$300\.000 sugerido: 0 Aceptar sugerido$/.test(fM('agosto')), 'agosto: el sueldo de producción ya no es gasto general: es mano de obra interna: ' + fM('agosto'));
  ok(/\$550\.000 18,3% provisorio \$300\.000 en el gasto general 0 0 al mes —/.test(ggP), 'sin prendas a confeccionar en esos meses (sin fichas), la mano de obra interna ($300.000) queda en el gasto general');
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
  ok(!(await p.$('#cv-margen')) && !/precio sugerido/i.test(await p.innerText('#view-costeo')), 'ya no se pide margen: no hay precio sugerido');
  await p.fill('#cv-bajada', '150'); await p.click('#view-costeo .acciones .btn.pri'); await p.waitForTimeout(700);
  ok(JSON.parse(config.find(c => c.clave === 'costeo_valores').valor).bajada === 150, 'el precio por bajada de plancha se guarda');

  // 8 · estabilidad: el refresco automático (cada minuto y al volver a la ventana) no borra lo que se está haciendo,
  //     y la búsqueda y el período de Pedidos se aplican
  await p.fill('#cv-bajada', '175');
  await p.evaluate(() => recargar(true)); await p.waitForTimeout(900);
  await p.evaluate(() => document.dispatchEvent(new Event('visibilitychange'))); await p.waitForTimeout(900);
  ok(await p.inputValue('#cv-bajada') === '175', 'Ploteo y estampado: lo escrito sin guardar sigue ahí tras el refresco automático y al volver a la ventana');
  await p.evaluate(() => { COSTEO_MODO = 'pedidos'; renderCosteo(); }); await p.waitForTimeout(900);
  await p.fill('#cs-q', 'COT-4001'); await p.waitForTimeout(900);
  let peds = await p.$$eval('#cs-tabla tr.cs-ped', t => t.map(x => x.innerText.split(' · ')[0].trim()));
  ok(peds.join() === 'COT-4001' && await p.inputValue('#cs-q') === 'COT-4001', 'buscar un pedido filtra la lista y el buscador conserva lo escrito (' + peds.join() + ')');
  await p.evaluate(() => recargar(true)); await p.waitForTimeout(900);
  peds = await p.$$eval('#cs-tabla tr.cs-ped', t => t.map(x => x.innerText.split(' · ')[0].trim()));
  ok(peds.join() === 'COT-4001' && await p.inputValue('#cs-q') === 'COT-4001', 'tras el refresco automático sigue la misma búsqueda');
  await p.fill('#cs-q', ''); await p.waitForTimeout(900);
  await p.fill('#cs-desde', '2026-11-06'); await p.dispatchEvent('#cs-desde', 'change'); await p.waitForTimeout(1200);
  peds = await p.$$eval('#cs-tabla tr.cs-ped', t => t.map(x => x.innerText.split(' · ')[0].trim()));
  ok(peds.join() === 'COT-4001' && await p.inputValue('#cs-desde') === '2026-11-06', 'cambiar «Desde» se aplica: queda solo el pedido del 6-11 (' + peds.join() + ')');
  await p.evaluate(() => { window.__antes = COSTEO_DATOS; }); await p.evaluate(() => actualizarAhora()); await p.waitForTimeout(1500);
  ok(await p.evaluate(() => COSTEO_DATOS && COSTEO_DATOS !== window.__antes && COSTEO_DATOS.d1 === '2026-11-06'), '«↻ Actualizar» vuelve a leer los datos del costeo, con el mismo período');

  // 9 · moldes sin registros: la tela y el ploteo se estiman con el promedio del mismo tipo de prenda (o la referencia)
  const est = await p.evaluate(async () => {
    PROM_TIPO = null; await cargarPromediosTipo();
    const sim = async (n, tela) => { const D = await datosSimMolde(n), R = calcSimulacion(n, D, tela);
      return { kg: R.partes[0].kg, est: !!R.partes[0].est, como: R.partes[0].como, mPP: R.mPP, plEst: R.plEst, faltan: R.faltan, tela: R.tela }; };
    const s17 = await sim(17, 'Pro'), s20 = await sim(20, 'Pro'), s106 = await sim(106, 'Pro');
    const guardado = PROM_TIPO; PROM_TIPO = {}; SIM_DATOS = {}; const ref = await sim(17, 'Pro'); PROM_TIPO = guardado; SIM_DATOS = {};
    const E = estimacionTipo(17);
    const P = calcCosteo({ id: 99, cot: 'COT-9999', cliente: 'Sin ficha', prendas: 5, desglose: { '17 · FUTMUJU02': 5 }, requiere_sublimacion: true },
      { rows: [], asig: [], fc: null, venta: null, gg: null }).moldes[0];
    return { s17, s20, s106, ref, pk: E.pkProm, ped: { tela: P.tela, t0: P.telas[0], metros: P.metros, metrosEst: P.metrosEst, faltan: P.faltan } };
  });
  ok(est.s17.est && Math.abs(est.s17.kg - 0.4875) < 1e-6 && /promedio de 1 corte de camiseta adulto \(1 molde\)/.test(est.s17.como) && Math.abs(est.s17.tela - 0.4875 * 9000) < 0.01,
    'molde 17 sin cortes: tela con el promedio de las camisetas adulto (3,9 kg ÷ 8 = 0,4875 kg por prenda) × $9.000/kg de Pro: ' + est.s17.como);
  ok(est.s17.plEst && est.s17.mPP === 2 && !est.s17.faltan.some(x => /cortes registrados|ploteos registrados/.test(x)), 'y el ploteo con el promedio de las camisetas (16 m ÷ 8 = 2 m por prenda); ya no falta nada de eso');
  ok(est.s20.est && Math.abs(est.s20.kg - 0.4875 * 0.7) < 1e-6 && Math.abs(est.s20.mPP - 1.4) < 1e-9 && /× 70% del adulto/.test(est.s20.como), 'molde 20 (infantil, sin cortes de infantiles): el promedio adulto × 70%');
  ok(!est.s106.est && est.s106.kg == null && est.s106.faltan.some(x => /cortes registrados de falda o su peso de referencia/.test(x)), 'falda sin registros ni referencia: pide el peso de referencia');
  ok(est.ref.est && est.ref.kg === 0.18 && est.ref.mPP === 1.5 && /referencia anotada para camiseta/.test(est.ref.como), 'sin ningún corte de camisetas: la referencia de partida (0,18 kg de tela y 1,5 m de papel por camiseta)');
  ok(est.ped.t0 && est.ped.t0.est && Math.abs(est.ped.t0.kgEst - 0.4875 * 5) < 1e-6 && Math.abs(est.ped.tela - 0.4875 * 5 * est.pk) < 0.01 && est.ped.metros === 10 && est.ped.metrosEst &&
    est.ped.faltan[0] === 'registro del corte (tela estimada con el peso promedio)', 'pedido sin ficha ni corte: tela con el peso promedio × 5 prendas y el $/kg promedio de las telas cortadas; ploteo 2 m × 5');
  await p.evaluate(() => { COSTEO_MODO = 'simular'; SIM.molde = '17'; SIM.principal = 'Pro'; SIM.piezas = {}; SIM_DATOS = {}; renderCosteo(); }); await p.waitForTimeout(1500);
  ok(/aún no tiene cortes ni ploteos registrados/.test(await p.textContent('#sim-estimado')) && /estimado/.test(await p.textContent('#sim-res')), 'Simular costo con el molde 17 avisa que es un valor estimado y de dónde sale');
  ok(!/sugerido/i.test(await p.innerText('#view-costeo')) && /anota el precio para calcular el gasto general/.test(await p.textContent('#sim-venta-res')), 'sin precio sugerido; sin precio de venta, el gasto general espera el precio simulado');
  await p.fill('#sim-venta', '20000'); await p.dispatchEvent('#sim-venta', 'change'); await p.waitForTimeout(1200);
  const sv = await p.evaluate(async () => { const D = await datosSimMolde(17), R = calcSimulacion(17, D, 'Pro'); return { gg: R.gg, ggM: R.ggMonto, total: R.total, res: R.resultado, directo: R.directo }; });
  const pz = n => '$' + Math.round(n).toLocaleString('es-CL'), vt = (await p.innerText('#sim-venta-res')).replace(/\s+/g, ' ');
  ok(sv.gg > 0 && Math.abs(sv.ggM - 20000 * sv.gg) < 1e-6 && Math.abs(sv.total - (sv.directo + sv.ggM)) < 1e-6 && Math.abs(sv.res - (20000 - sv.total)) < 1e-6 &&
    vt.includes('Gasto general ' + (Math.round(sv.gg * 1000) / 10).toLocaleString('es-CL') + '% del precio de venta ' + pz(sv.ggM)) && vt.includes('Margen precio de venta − costo total ' + pz(sv.res)),
    'con un precio de venta simulado de $20.000: gasto general = $20.000 × % de gasto general; costo total = directo + gasto general; margen = precio − costo total');
  await p.evaluate(() => { SIM.venta = ''; });
  await p.evaluate(() => { COSTEO_MODO = 'valores'; renderCosteo(); }); await p.waitForTimeout(900);
  ok(/0,49 kg \(1 corte\) · 2 m \(1 ploteo\)/.test(await p.textContent('#cv-ref')) && await p.inputValue('[data-ref-kg="camiseta"]') === '0.18' && await p.inputValue('#cv-inf') === '70',
    'Ploteo y estampado: promedio de lo registrado por prenda, referencia de la camiseta y % infantil');
  await p.fill('[data-ref-kg="falda"]', '0.12'); await p.fill('#cv-inf', '65'); await p.click('#view-costeo .acciones .btn.pri'); await p.waitForTimeout(800);
  const cv = JSON.parse(config.find(c => c.clave === 'costeo_valores').valor);
  ok(cv.ref && cv.ref.falda && cv.ref.falda.kg === 0.12 && !cv.ref.camiseta && cv.infPct === 65, 'se guardan la referencia de la falda y el % infantil (la camiseta, igual al valor de partida, no se guarda)');
  const rf = await p.evaluate(() => { const antes = COSTEO_VAL.ref, out = {};
    COSTEO_VAL.ref = { camiseta: { kg: 0.18, m: 0.8 } }; out.viejo = refEst('camiseta');
    COSTEO_VAL.ref = { camiseta: { m: 1.2 } }; out.propio = refEst('camiseta');
    COSTEO_VAL.ref = antes; out.prot = (COSTEO_VAL.protF === '' ? 1 : +COSTEO_VAL.protF); return out; });
  ok(rf.viejo.m === 1.5 && rf.viejo.kg === 0.18 && rf.propio.m === 1.2 && rf.propio.kg === 0.18 && rf.prot === 1,
    'el 0,8 m guardado antes como valor de partida pasa a 1,5 m; un valor propio (1,2 m) se respeta; protección = los mismos metros');
  const f106 = await p.evaluate(async () => { const D = await datosSimMolde(106), R = calcSimulacion(106, D, 'Pro'); return R.partes[0].kg; });
  ok(Math.abs(f106 - 0.12) < 1e-9, 'la falda ya tiene valor: 0,12 kg de referencia');
  // lo pesado manda: un corte sin las prendas anotadas (toma las del pedido) y uno registrado para el pedido completo
  // (el pedido lleva un solo molde) cuentan como reales para su molde
  costeo.push({ id: 900, etapa: 'CORTE', planificacion_id: 2, cot: 'COT-4001', molde: '18 · FUTHOMU02', tela: 'Pro', kg_cortado: 3.2, kg_merma: 0, prendas: null },
    { id: 901, etapa: 'CORTE', planificacion_id: 2, cot: 'COT-4001', molde: '', tela: 'Nacional', kg_cortado: 0.8, kg_merma: 0, prendas: null });
  const pesado = await p.evaluate(async () => {
    CORTES_SIM = null; SIM_DATOS = {}; PROM_TIPO = null;
    const D = await datosSimMolde(18), R = calcSimulacion(18, D, 'Pro'); await cargarPromediosTipo();
    return { cortes: D.cortes.length, kgPP: R.kgPP, est: R.telaEst, prom17: estimacionTipo(17).kgPP };
  });
  ok(pesado.cortes === 2 && Math.abs(pesado.kgPP - 7.9 / 16) < 1e-9 && !pesado.est && Math.abs(pesado.prom17 - 7.9 / 16) < 1e-9,
    'molde 18: el corte sin prendas anotadas (8 del pedido) y el del pedido completo cuentan como reales: (3,9 + 4,0) kg ÷ 16 prendas, sin estimar');
  costeo.splice(costeo.findIndex(x => x.id === 900), 2);

  // 10 · pedido antiguo con desglose incompleto (1 BK-CSUB + 1 BK-SH de 40 vendidas, sin N° de molde): la venta
  // se toma en la parte de esas 2 prendas (si no, todo el gasto general del pedido cae sobre 2 prendas) y la tela y el
  // ploteo se estiman por el tipo de prenda que dice el código
  const inc = await p.evaluate(() => {
    const G = { pct: 0.498, meses: ['2026-08', '2026-09', '2026-10'] };
    const R = calcCosteo({ id: 98, cot: 'COT-9998', cliente: 'Antiguo', prendas: 2, desglose: { 'BK-CSUB': 1, 'BK-SH': 1 }, requiere_sublimacion: true },
      { rows: [], asig: [], fc: null, venta: 1180000, ventaCant: 40, gg: G });
    const T = calcCosteo({ id: 97, cot: 'COT-9997', cliente: 'Completo', prendas: 40, desglose: { 'BK-CSUB': 20, 'BK-SH': 20 }, requiere_sublimacion: true },
      { rows: [], asig: [], fc: null, venta: 1180000, ventaCant: 40, gg: G });
    return { venta: R.venta, ventaTotal: R.ventaTotal, gg: R.ggMonto, inc: R.desgloseIncompleto, faltan: R.faltan, porPrenda: R.porPrenda, margen: R.margen,
      cam: { tela: R.moldes[0].tela, est: !!(R.moldes[0].telas[0] || {}).est, metros: R.moldes[0].metros },
      sho: { tela: R.moldes[1].tela, como: (R.moldes[1].telas[0] || {}).como || '' }, tVenta: T.venta, tInc: T.desgloseIncompleto || null, tGG: T.ggMonto };
  });
  ok(inc.venta === 59000 && inc.ventaTotal === 1180000 && Math.abs(inc.gg - 59000 * 0.498) < 1e-6 && inc.inc.costeadas === 2 && inc.inc.vendidas === 40 &&
    inc.faltan.includes('desglose por molde: tiene 2 de 40 prendas (se usa esa parte de la venta)') && inc.porPrenda < 40000,
    'desglose de 2 de 40 prendas: venta $59.000 (2/40 de $1.180.000) y gasto general $29.382, no $587.640 sobre 2 prendas (por prenda ' + Math.round(inc.porPrenda) + ')');
  ok(inc.cam.est && inc.cam.tela > 0 && inc.cam.metros > 0 && inc.sho.tela > 0 && /short/.test(inc.sho.como),
    'sin N° de molde: la tela y el ploteo se estiman por el tipo de prenda del código (BK-CSUB camiseta, BK-SH short): ' + inc.sho.como);
  ok(inc.tVenta === 1180000 && !inc.tInc && Math.abs(inc.tGG - 1180000 * 0.498) < 1e-6, 'con el desglose completo (40 de 40) se usa la venta entera');

  // 11 · sueldos por persona: los de quienes hacen la prenda son costo directo (mano de obra interna, por prenda), no
  // gasto general; la diseñadora de vestuario y ventas son gasto general; las leyes sociales se reparten según los sueldos
  ventasPed[1].cantidad = 100; ventasPed[2].cantidad = 100; ventasPed[3].cantidad = 100;
  // las prendas del mes salen de las fichas de tallas creadas en el panel ese mes (100 prendas sin medias cada una)
  [['COT-3900', '2026-08-10'], ['COT-3901', '2026-09-10'], ['COT-3902', '2026-10-10']].forEach(([ref, d]) => fichasF.push({ id: ref, ref, proyecto: 'Prueba ' + ref, cliente: 'Cliente ' + ref,
    items: [{ prenda: 'camiseta', cant: 60 }, { prenda: 'short', cant: 40 }, { prenda: 'medias', cant: 100 }], specs: {}, created_at: d + 'T12:00:00Z' }));
  vGastosNeto.push(gn(9, '2026-09-01', '3.02', '3', 'clasificado', 200000, 200000), gn(10, '2026-09-01', '3.01', '3', 'clasificado', 200000, 200000),
    gn(11, '2026-09-01', '3.03', '3', 'clasificado', 40000, 40000), gn(12, '2026-10-01', '4.01', '4', 'clasificado', 100000, 100000));
  gastosV.push({ id: 1, proveedor: 'GERALDINE PRUEBA' }, { id: 9, proveedor: 'BELÉN PRUEBA' }, { id: 10, proveedor: 'Geraldine Prueba' }, { id: 12, proveedor: 'VENDEDORA PRUEBA' });
  await ctx.route(/nnisdusdujcpkrbjqnhe\.supabase\.co\/rest\/v1\/gestion_parametros/, r => {
    const q = r.request(); if (q.method() === 'GET') return r.fulfill({ contentType: 'application/json', body: JSON.stringify(gestionParametros) });
    [].concat(JSON.parse(q.postData())).forEach(x => { const ya = gestionParametros.find(y => y.clave === x.clave); if (ya) Object.assign(ya, x); else gestionParametros.push(x); });
    return r.fulfill({ status: 201, contentType: 'application/json', body: '' }); });
  await p.evaluate(() => { GG_DATOS = null; COSTEO_DATOS = null; COSTEO_MODO = 'gg'; renderCosteo(); }); await p.waitForTimeout(1500);
  const per = await p.$$eval('#gg-personas tr[data-persona]', trs => trs.map(t => ({ k: t.dataset.persona, v: (t.querySelector('select') || {}).value, tx: t.innerText.replace(/\s+/g, ' ') })));
  const g1 = await p.evaluate(() => { const x = calcularGG().pct('2026-11'); return { pct: x.pct, mod: x.mod, pr: x.prendas, pp: x.modPP }; });
  ok(per.length === 3 && per.find(x => x.k === 'geraldine prueba').v === 'directo' && /también: Geraldine Prueba/.test(per.find(x => x.k === 'geraldine prueba').tx) &&
    per.find(x => x.k === 'belen prueba').v === 'directo' && per.find(x => x.k === 'vendedora prueba').v === 'general' && per.every(x => /sin confirmar/.test(x.tx)) &&
    /3 personas sin confirmar/.test(await p.textContent('#gg-sin-confirmar')),
    'lista de personas con sueldo (el mismo nombre escrito distinto es una sola): sin confirmar, cada una según su cuenta: ' + per.map(x => x.k + '=' + x.v).join(', '));
  ok(Math.abs(g1.pct - 350000 / 3000000) < 1e-9 && g1.mod === 740000 && g1.pr === 300 && Math.abs(g1.pp - 740000 / 300) < 1e-9,
    'sin confirmar: gasto general $350.000 (11,7%); mano de obra interna $740.000 (sueldos de producción y diseño + leyes) ÷ 300 prendas vendidas');
  await p.selectOption('[data-sp="belen prueba"]', 'general'); await p.click('#gg-personas + .acciones .btn.pri'); await p.waitForTimeout(1500);
  const sp = (gestionParametros.find(x => x.clave === 'sueldos_personas') || {}).valor || {};
  ok(sp['belen prueba'] === 'general' && sp['geraldine prueba'] === 'directo' && sp['vendedora prueba'] === 'general', 'se guarda en Ventas a qué va cada persona: ' + JSON.stringify(sp));
  const g2 = await p.evaluate(() => { const G = calcularGG(), x = G.pct('2026-11'), sep = G.mes('2026-09'); return { pct: x.pct, mod: x.mod, pp: x.modPP, k: sep.kDir, ld: sep.leyesDir, prod: sep.prod }; });
  const sep = (await p.$$eval('#gg-meses tr', trs => trs.map(t => t.innerText.replace(/\s+/g, ' ')))).find(x => x.startsWith('septiembre')) || '';
  ok(Math.abs(g2.k - 0.5) < 1e-9 && g2.ld === 20000 && g2.prod === 120000 + 200000 + 20000 && /50% de las leyes sociales/.test(sep),
    'septiembre: leyes sociales $40.000 repartidas según los sueldos: 50% al costo directo (Geraldine) y 50% al gasto general (Belén): ' + sep);
  ok(Math.abs(g2.pct - 0.19) < 1e-9 && g2.mod === 520000 && Math.abs(g2.pp - 520000 / 300) < 1e-9 && !/sin confirmar/.test(await p.innerText('#gg-personas')),
    'Belén al gasto general: gasto general $570.000 (19%); mano de obra interna $520.000 ÷ 300 = $1.733 por prenda');
  await p.evaluate(() => { COSTEO_MODO = 'pedidos'; COSTEO_Q = 'COT-4000'; COSTEO_PER = null; COSTEO_DATOS = null; renderCosteo(); }); await p.waitForTimeout(2500);
  const cam2 = (await p.$$eval('#cs-tabla tr.cs-molde', trs => trs.map(t => t.innerText.replace(/\s+/g, ' '))))[0] || '';
  ok(/ 8 \$[\d.]+ \$[\d.]+ \$24\.000 \$13\.867 /.test(cam2), 'pedido: la camiseta lleva 8 × $1.733 = $13.867 de mano de obra interna en su costo directo: ' + cam2);
  await p.evaluate(() => verCosteo(1)); await p.waitForTimeout(700);
  ok(/Mano de obra interna\s+\$1\.733 por prenda: sueldos y leyes sociales de quienes hacen la prenda \(\$520\.000\) ÷ 300 prendas a confeccionar \(100 al mes\) de agosto 2026, septiembre 2026, octubre 2026, según las fichas de tallas \(sin confirmar\)\s+\$13\.867/.test(await p.innerText('#modal')),
    'detalle: de dónde sale la mano de obra interna');
  await p.evaluate(() => cerrarModal());
  const sim = await p.evaluate(async () => { SIM_DATOS = {}; const D = await datosSimMolde(17), R = calcSimulacion(17, D, 'Pro'); return { mo: R.mo, directo: R.directo }; });
  ok(Math.abs(sim.mo - 520000 / 300) < 1e-9, 'Simular costo: la mano de obra interna por prenda ($1.733) va en el costo directo');
  await p.evaluate(() => { COSTEO_Q = ''; });

  // 12 · prendas a confeccionar: solo las que se cosen (sin medias ni aplicaciones); kit y dúo = 2 por unidad. El
  // total del mes sale de las fichas de tallas creadas en el panel ese mes; un pedido con partes cuenta una vez
  fichasF.push({ ref: 'COT-3990', cliente: 'Kit', items: [{ prenda: 'camiseta', cant: 10 }, { prenda: 'short', cant: 10 }, { prenda: 'medias', cant: 10 }], created_at: '2026-06-10T10:00:00Z' },
    { ref: 'COT-3991-1', cliente: 'Partes', items: [{ prenda: 'camiseta', cant: 5 }], created_at: '2026-06-11T10:00:00Z' },
    { ref: 'COT-3991-2', cliente: 'Partes', items: [{ prenda: 'short', cant: 5 }], created_at: '2026-06-12T10:00:00Z' },
    { ref: 'COT-3992', cliente: 'Solo medias', items: [{ prenda: 'medias', cant: 30 }], created_at: '2026-06-12T10:00:00Z' });
  const pc = await p.evaluate(async () => {
    const f = d => factorVenta(d); GG_DATOS = null; await cargarGG('2026-04'); const m = calcularGG().mes('2026-06');
    return { f: [f('20 KIT ORO'), f('DUO DIAMANTE'), f('MEDIAS'), f('ESCUDOS BORDADOS'), f('CAMISETAS + ESCUDOS'), f('Indumentaria de rugby')],
      desg: prendasDesglose({ '18 · FUTHOMU02': 8, '46 · BK-SH': 2, 'VINILO': true, 'MEDIAS-ADL': true }),
      txt: textoVentaPrendas({ cantidad: 20, descripcion: 'KIT DIAMANTE' }), m: { pr: m.prendas, ficha: m.nFicha, det: m.det.map(x => x.cot + '=' + x.n + ' ' + x.origen) } };
  });
  ok(pc.f.join() === '2,2,0,0,1,1' && pc.desg === 10 && pc.txt === '20 kits o dúos = 40 prendas a confeccionar',
    'regla en Ventas e ingreso: kit y dúo = 2 prendas; solo medias o aplicaciones = 0; con prendas = 1; el desglose no cuenta medias ni servicios: ' + JSON.stringify(pc.f));
  ok(pc.m.pr === 30 && pc.m.ficha === 2 && pc.m.det.includes('COT-3990=20 Camiseta 10 · Short o calza 10') && pc.m.det.includes('COT-3991=10 Camiseta 5 · Short o calza 5'),
    'junio desde las fichas del panel: el kit cuenta camiseta y short (20, sin sus medias), las partes de un pedido se suman (10) y una ficha de solo medias no cuenta: ' + JSON.stringify(pc.m));
  // sugerido desde las fichas: se acepta o se registra a mano; manda en la mano de obra por prenda
  await p.evaluate(() => { COSTEO_MODO = 'gg'; renderCosteo(); }); await p.waitForTimeout(1500);
  const sugNov = await p.evaluate(() => calcularGG().mes('2026-11').prendasCalc);
  await p.evaluate(() => verPrendasMes('2026-11')); await p.waitForTimeout(300);
  const detNov = (await p.innerText('#pm-detalle')).replace(/\s+/g, ' ');
  ok(sugNov === 18 && /COT-4000 Club Costeo Uniformes Camiseta 8 · Short o calza 2 10/.test(detNov) && /COT-4001 .* Camiseta 8 8/.test(detNov),
    'noviembre: sugerido 18 desde las fichas creadas en el mes (COT-4000: 10, COT-4001: 8); el detalle muestra cada ficha: ' + detNov.slice(0, 200));
  await p.evaluate(() => cerrarModal());
  await p.click('[data-pm="2026-10"] ~ div button'); await p.fill('[data-pm="2026-09"]', '400'); await p.click('#gg-pm-guardar'); await p.waitForTimeout(1500);
  const pmG = JSON.parse(config.find(c => c.clave === 'costeo_valores').valor).prendasMes || {};
  const g3 = await p.evaluate(() => { const x = calcularGG().pct('2026-11'); return { pr: x.prendas, pp: x.modPP, nm: x.nManual }; });
  ok(pmG['2026-10'] === 100 && pmG['2026-09'] === 400 && pmG['2026-08'] == null && g3.pr === 600 && g3.nm === 2 && Math.abs(g3.pp - 520000 / 600) < 1e-9
    && /registrado por ti/.test(await p.innerText('#gg-meses')),
    'octubre: se acepta el sugerido (100); septiembre: se registra a mano (400); agosto sigue con el sugerido (100): 600 prendas y $867 por prenda: ' + JSON.stringify({ pmG, g3 }));

  // 13 · desde diciembre 2026 las prendas del mes son las de los pedidos ingresados a producción ese mes: solo prendas
  // de vestir del desglose (sin medias, aplicaciones ni otros artículos); las fichas de ese mes ya no cuentan
  proys.push({ id: 30, cot: 'COT-5000', cliente: 'Club Diciembre', prendas: 45, desglose: { '18 · FUTHOMU02': 20, '46 · BK-SH': 20, 'MEDIAS-ADL': true, 'VINILO': true, 'BOLSO': 5 },
    fecha_ingreso_ficha: '2026-12-03', fecha_entrega_cliente: '2027-01-10', tipo: 'normal', requiere_sublimacion: true, estado_general: 'en_produccion', created_at: ahora });
  fichasF.push({ ref: 'COT-5001', cliente: 'Ficha de diciembre', items: [{ prenda: 'camiseta', cant: 50 }], created_at: '2026-12-05T10:00:00Z' });
  const dic = await p.evaluate(async () => { GG_DATOS = null; await cargarGG('2026-04'); const m = calcularGG().mes('2026-12');
    return { pr: m.prendas, n: m.nIngr, fichas: m.nFicha, det: m.det.map(x => x.cot + '=' + x.n + ' ' + x.origen) }; });
  ok(dic.pr === 40 && dic.n === 1 && !dic.fichas && dic.det[0] === 'COT-5000=40 18 · FUTHOMU02 20 · 46 · BK-SH 20',
    'diciembre: 40 prendas de vestir del pedido ingresado (camisetas y shorts; sin medias, vinilo ni bolsos); la ficha creada en diciembre no cuenta: ' + JSON.stringify(dic));
  proys.splice(proys.findIndex(x => x.id === 30), 1);

  // 14 · telas del pedido: al ingresar, cada molde con las telas de la ficha; se confirma la tela y su proveedor; se
  // descuenta el estimado (cortes del mismo molde con la misma tela); sin estimado, el cortador debe pesar
  await ctx.route(/ygcsqrylpibhofvetdyh\.supabase\.co\/rest\/v1\/planificacion\?id=eq\.\d+/, r => { const q = r.request();
    if (q.method() !== 'PATCH') return r.fallback(); const id = +new URL(q.url()).searchParams.get('id').slice(3), x = proys.find(y => y.id === id);
    if (x) Object.assign(x, JSON.parse(q.postData())); return r.fulfill({ contentType: 'application/json', body: '[]' }); });
  const pesosPro = costeo.filter(r => r.etapa === 'CORTE' && r.molde === '18 · FUTHOMU02' && r.tela === 'Pro' && +r.prendas > 0);
  const kgPro = pesosPro.reduce((t, r) => t + (+r.kg_cortado || 0) + (+r.kg_merma || 0), 0) / pesosPro.reduce((t, r) => t + +r.prendas, 0);
  movs = movs.filter(m => m.planificacion_id !== 2);
  const ti = await p.evaluate(async () => {
    FICHAS_MAP['COT-4001'] = (await apiF('fichas_tallas?select=*')).find(f => f.ref === 'COT-4001');
    DETS_MAP['COT-4001'] = (await apiF('fichas_detalle?select=*')).filter(d => d.ref === 'COT-4001');
    CORTES_SIM = null; await Promise.all([cargarInsumos(), cargarCortesSim()]);
    if (!$('f-consumo')) document.body.insertAdjacentHTML('beforeend', '<div id="f-consumo"></div>');
    const desg = { '18 · FUTHOMU02': 8, 'MEDIAS-ADL': true };
    leerGrid = (orig => cid => cid === 'f-desglose' ? { desglose: desg, total: 8 } : orig(cid))(leerGrid);
    const fm = telasFichaPorMolde('COT-4001'); pintarTelasIngreso('COT-4001', desg);
    const filas1 = [...document.querySelectorAll('#ti-tabla tr[data-ti]')].map(t => t.innerText.replace(/\s+/g, ' '));
    const falta1 = faltaTelasIngreso('COT-4001');
    cambiarTelaIngreso(0, 'prov', 'Lafayette', true); cambiarTelaIngreso(1, 'tela', 'Dry fit'); cambiarTelaIngreso(1, 'prov', 'Comercial Alameda', true);
    const filas2 = [...document.querySelectorAll('#ti-tabla tr[data-ti]')].map(t => t.innerText.replace(/\s+/g, ' '));
    const falta2 = faltaTelasIngreso('COT-4001');
    const n = await guardarTelasPedido(proyCosteo(2), 'COT-4001');   // (al ingresar, la recarga trae las telas guardadas)
    return { fm, filas1, falta1, filas2, falta2, n };
  });
  ok(JSON.stringify(ti.fm) === JSON.stringify({ '18 · FUTHOMU02': ['Pro', 'Nacional'] }), 'ingreso: el molde trae las telas de la ficha (Pro y la manga en Nacional): ' + JSON.stringify(ti.fm));
  ok(ti.filas1.length === 2 && new RegExp(String(Math.round(kgPro * 8 * 100) / 100).replace('.', ',') + ' ?kg ?8 × ').test(ti.filas1[0]) && /promedio de \d+ cortes? \(\d+ prendas\) de este molde con esta tela/.test(ti.filas1[0])
    && ti.falta1.length === 2 && ti.falta1.every(x => /falta el proveedor/.test(x)),
    'ingreso: Pro con su estimado (8 × kg por prenda de los cortes del mismo molde con Pro); falta elegir el proveedor de cada tela: ' + ti.filas1[0]);
  ok(/sin estimado/.test(ti.filas2[1]) && !ti.falta2.length && ti.n === 1, 'ingreso: se cambia la manga a Dry fit (sin cortes de este molde con esa tela: sin estimado) y se eligen los proveedores; se descuenta solo el estimado de Pro');
  const plan2 = proys.find(x => x.id === 2).telas || [], mv2 = movs.filter(m => m.planificacion_id === 2);
  ok(plan2.length === 2 && plan2[0].tela === 'Pro' && plan2[0].proveedor === 'Lafayette' && Math.abs(plan2[0].kg_prenda - kgPro) < 1e-3 && plan2[1].tela === 'Dry fit' && plan2[1].kg_prenda == null
    && mv2.length === 1 && mv2[0].insumo_id === 1 && Math.abs(mv2[0].cantidad + kgPro * 8) < 0.01 && mv2[0].proveedor === 'Lafayette' && /^Estimado al ingresar · 18 · FUTHOMU02: 8 prendas × /.test(mv2[0].nota),
    'se guardan las telas del pedido (con proveedor y estimado) y se descuenta del stock el estimado de Pro con su proveedor: ' + JSON.stringify(mv2.map(m => m.cantidad + ' ' + m.nota)));
  // corte: Dry fit no tiene estimado, así que hay que pesarla: no se puede terminar sin registrar ni guardar sin ella
  await p.evaluate(() => abrirRegistroCosteo(2, 'CORTE', true)); await p.waitForTimeout(700);
  const mc = await p.innerText('#modal');
  ok(/Hay que pesar: 18 · FUTHOMU02 · Dry fit/.test(mc) && /Pesar: obligatorio/.test(mc) && !/Terminar sin registrar/.test(mc) && /descontado al ingresar/.test(mc),
    'corte: avisa que Dry fit se pesa obligatoriamente, muestra lo estimado de Pro y no deja terminar sin registrar');
  await p.evaluate(() => cerrarModal()); await p.evaluate(() => abrirRegistroCosteo(2, 'CORTE')); await p.waitForTimeout(700);
  await p.fill('#rc-c-0-0', '3.1'); await p.fill('#rc-m-0-0', '0.3'); await p.click('#modal .acciones .btn.pri'); await p.waitForTimeout(600);
  ok(!costeo.some(r => r.planificacion_id === 2 && r.etapa === 'CORTE') && await p.isVisible('#rc-c-0-1'), 'sin el peso de Dry fit no se guarda el corte');
  await p.fill('#rc-c-0-1', '1'); await p.fill('#rc-m-0-1', '0.2'); await p.click('#modal .acciones .btn.pri'); await p.waitForTimeout(1200);
  const mv3 = movs.filter(m => m.planificacion_id === 2).map(m => ({ i: m.insumo_id, c: m.cantidad, p: m.proveedor, n: m.nota }));
  ok(costeo.filter(r => r.planificacion_id === 2 && r.etapa === 'CORTE').length === 2 && mv3.length === 2 && mv3.find(m => m.i === 1).c === -3.4 && mv3.find(m => m.i === 1).p === 'Lafayette'
    && /^Corte pesado/.test(mv3.find(m => m.i === 1).n) && Math.abs(mv3.find(m => m.i === 9).c + 1.2 * 5) < 1e-9 && mv3.find(m => m.i === 9).p === 'Comercial Alameda',
    'corte: lo pesado reemplaza al estimado en el stock (Pro 3,4 kg con Lafayette; Dry fit 1,2 kg = 6 m con Comercial Alameda): ' + JSON.stringify(mv3));
  // el costeo usa el precio del proveedor elegido
  const pk = await p.evaluate(() => { const antes = [PRECIOS, PRECIOS_OK]; PRECIOS = [{ id: 1, insumo_id: 1, proveedor: 'Lafayette', presentacion: 'kg', precio: 12000, activo: true },
    { id: 2, insumo_id: 1, proveedor: 'Otro', presentacion: 'kg', precio: 15000, activo: true }]; PRECIOS_OK = true;
    const r = { prov: precioKgPedido(proyCosteo(2), '18 · FUTHOMU02', insumoDe(1)), sin: precioKgPedido(proyCosteo(1), '18 · FUTHOMU02', insumoDe(1)), ins: precioKg(insumoDe(1)) }; [PRECIOS, PRECIOS_OK] = antes; return r; });
  ok(pk.prov === 12000 && pk.sin === pk.ins && pk.ins !== 12000, 'costeo: la tela del pedido con el precio de su proveedor (Lafayette $12.000/kg); sin proveedor elegido, el precio del insumo: ' + JSON.stringify(pk));
  // registros de pesos: todos los cortes, con su kg por prenda frente al promedio del mismo molde y tela
  costeo.push({ id: 950, etapa: 'CORTE', planificacion_id: 31, cot: 'COT-5002', molde: '18 · FUTHOMU02', tela: 'Pro', kg_cortado: 30, kg_merma: 0, prendas: 8, usuario: 'Cortador', updated_at: '2026-11-20T10:00:00Z' });
  await p.evaluate(() => { CORTES_SIM = null; COSTEO_MODO = 'pesos'; PESOS_Q = ''; PESOS_ALERTA = false; renderCosteo(); }); await p.waitForTimeout(1500);
  const raro = (await p.innerText('#ps-tabla tr[data-peso="950"]')).replace(/\s+/g, ' ');
  const nTodos = await p.$$eval('#ps-tabla tr[data-peso]', t => t.length);
  await p.check('#view-costeo input[type=checkbox]'); await p.waitForTimeout(900);
  const nRaros = await p.$$eval('#ps-tabla tr[data-peso]', t => t.length);
  const est18 = await p.evaluate(() => estimadoMoldeTela('18 · FUTHOMU02', 'Pro'));
  ok(/COT-5002 .*18 · FUTHOMU02 Pro 8 30 0 0% 3,75 /.test(raro) && /más de 1,2 kg por prenda/.test(raro) && /% de lo típico/.test(raro) && /no entra al estimado/.test(raro)
    && nTodos === costeo.filter(r => r.etapa === 'CORTE').length && nRaros === 1,
    'registros de pesos: lista todos los cortes y marca solo el de 30 kg para 8 camisetas (3,75 kg por prenda, lejos de lo típico); el filtro deja solo ese: ' + raro);
  ok(est18.fuera === 1 && est18.cortes === 2 && est18.kgPP < 0.5, 'el peso mal anotado no entra al estimado del molde con esa tela hasta corregirlo: ' + JSON.stringify(est18));
  costeo.splice(costeo.findIndex(r => r.id === 950), 1);

  ok(!errores.length, 'sin errores JS ' + errores.join(' | '));
  await b.close();
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
