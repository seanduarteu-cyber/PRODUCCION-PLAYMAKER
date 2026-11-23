// Costeo › Precios por proveedor (SQL 23A), Ploteo y estampado (4 tintas por separado) y Simular costo.
// Bases simuladas con estado (Producción, Fichas y Ventas): leen, cambian, agregan y borran filas como Supabase.
const { chromium, contexto } = require('./comun_movil');
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const cerca = (a, b, tol) => Math.abs(a - b) <= (tol || 0.5);
const ahora = new Date().toISOString();
const moldes = require('./datos_moldes_catalogo.json').map(m => Object.assign({}, m));
moldes.find(m => m.numero === 18).piezas = [{ pieza: 'Delantero', cant: 1, consumo: 0.5 }, { pieza: 'Espalda', cant: 1, consumo: 0.5 }, { pieza: 'Manga', cant: 2, consumo: 0.3 }, { pieza: 'Cuello', cant: 1 }];
const ins = (id, nombre, categoria, unidad, precio, extra) => ({ id, nombre, categoria, unidad, precio, rendimiento: null, proveedor: null, stock: 100, activo: true, ...extra });
const insumos = [ins(1, 'Pro', 'Tela', 'kg', 9500, { proveedor: 'Telas Norte' }), ins(2, 'Nacional', 'Tela', 'm', 2500, { rendimiento: 4 }), ins(3, 'Elástico', 'Elástico', 'm', 300),
  ins(4, 'Etiqueta', 'Etiqueta', 'unid', 50), ins(5, 'Bolsa', 'Embalaje', 'unid', 80), ins(6, 'Papel sublimación', 'Papel', 'm', 400, { proveedor: 'PapelCo' }),
  ins(7, 'Papel protección', 'Papel', 'm', 150), ins(11, 'Tinta cian', 'Tinta', 'litro', 50000), ins(12, 'Tinta magenta', 'Tinta', 'litro', 50000),
  ins(13, 'Tinta amarilla', 'Tinta', 'litro', 50000), ins(14, 'Tinta negra', 'Tinta', 'litro', 45000), ins(15, 'Rib', 'Tela', 'kg', 12000)];
const L = (id, insumo_id, proveedor, proveedor_id, presentacion, precio, extra) => ({ id, insumo_id, proveedor, proveedor_id, presentacion, contenido: 1, precio, ancho_m: null, gramaje: null, rendimiento: null, activo: true, ...extra });
const DB = {
  prod: {
    plan_insumos: insumos, plan_insumos_stock: insumos, plan_insumos_mov: [],
    plan_insumo_precios: [L(1, 1, 'Textil Sur', 101, 'kg', 9000, { ancho_m: 1.6, gramaje: 150 }), L(2, 1, 'Telas Norte', 102, 'kg', 9500, { ancho_m: 1.8, gramaje: 140 }),
      L(3, 2, 'Sin proveedor', null, 'm', 2500, { rendimiento: 4 }), L(4, 6, 'PapelCo', 103, 'm', 400),
      ...[11, 12, 13, 14].map((k, j) => L(10 + j, k, 'Mimaki Chile', 104, 'envase', k === 14 ? 45000 : 50000, { contenido: 1000 })), L(20, 15, 'Textil Sur', 101, 'kg', 12000, { ancho_m: 1, gramaje: 220 })],
    plan_proveedores_estado: [],
    plan_config: [{ clave: 'costeo_valores', valor: JSON.stringify({ papel: '6', tinta: '', tintaM: 0, prot: '7', protF: 1, margen: 30 }) }],
    // COT-4000: frente y mangas en Pro, espalda en Nacional (con sus piezas, SQL 23B); COT-4001: corte anterior sin piezas (se completan desde su ficha)
    plan_costeo: [{ id: 1, planificacion_id: 1, cot: 'COT-4000', etapa: 'CORTE', molde: '18 · FUTHOMU02', tela: 'Pro', kg_cortado: 2.5, kg_merma: 0.4, prendas: 8, piezas: ['Delantero', 'Manga'] },
      { id: 2, planificacion_id: 1, cot: 'COT-4000', etapa: 'CORTE', molde: '18 · FUTHOMU02', tela: 'Nacional', kg_cortado: 0.8, kg_merma: 0.2, prendas: 8, piezas: ['Espalda'] },
      { id: 4, planificacion_id: 2, cot: 'COT-4001', etapa: 'CORTE', molde: '18 · FUTHOMU02', tela: 'Pro', kg_cortado: 2.2, kg_merma: 0.2, prendas: 6, piezas: null },
      { id: 5, planificacion_id: 2, cot: 'COT-4001', etapa: 'CORTE', molde: '18 · FUTHOMU02', tela: 'Nacional', kg_cortado: 0.7, kg_merma: 0.1, prendas: 6, piezas: null },
      { id: 3, planificacion_id: 1, etapa: 'PLOTEO', molde: '18 · FUTHOMU02', tela: '', metros: 16 }],
    plan_asignaciones: [{ id: 1, planificacion_id: 1, etapa: 'CONFEC', ejecutante: 'Taller Las Rosas', tipo_prenda: '18 · FUTHOMU02', cantidad: 8, precio_unit: 3000 }],
    plan_insumos_molde: [{ id: 1, molde: '*', insumo_id: 4, cantidad: 1 }, { id: 2, molde: '*', insumo_id: 5, cantidad: 1 }],
    plan_tarifas: [{ tipo: '18 · FUTHOMU02', precio: 2800 }],
    planificacion: [{ id: 1, cot: 'COT-4000', cliente: 'Club Costeo', prendas: 8, desglose: { '18 · FUTHOMU02': 8 }, fecha_ingreso_ficha: '2026-10-05', fecha_entrega_cliente: '2026-10-30',
      tipo: 'normal', requiere_sublimacion: true, estado_general: 'entregado', created_at: ahora }],
    plan_usuarios: [{ usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'], activo: true }]
  },
  fichas: { moldes, catalogo_tecnico: [],
    fichas_tallas: [{ id: 2, ref: 'COT-4001', cliente: 'Club Dos', estado: 'confirmado', items: [{ prenda: 'camiseta', cant: 6 }], created_at: ahora,
      specs: { camiseta: { tela: 'Pro', moldes: { Masculino: 'FUTHOMU02|18' }, despiece: { molde: '18 · FUTHOMU02', piezas: [{ pieza: 'Espalda', tela: 'Nacional' }] } } } }],
    fichas_detalle: Array.from({ length: 6 }, (_, i) => ({ id: 'q' + i, ref: 'COT-4001', calce: 'Masculino', manga: 'Corta', tallas: { camiseta: 'M' }, created_at: ahora })) },
  ventas: {
    proveedores: [{ id: 101, nombre: 'Textil Sur', rut: '76.111.111-1', tipo_documento: 'afecta' }, { id: 102, nombre: 'Telas Norte', tipo_documento: 'afecta' },
      { id: 103, nombre: 'PapelCo', tipo_documento: 'afecta' }, { id: 104, nombre: 'Mimaki Chile', tipo_documento: 'afecta' }],
    // gasto general de agosto a octubre: $550.000 ÷ $3.000.000 = 18,3% (como en costeo.test.js)
    pedidos: [{ id: 2, cot: '3900', fecha: '2026-08-10', neto: 1000000 }, { id: 3, cot: '3901', fecha: '2026-09-10', neto: 1000000 }, { id: 4, cot: '3902', fecha: '2026-10-10', neto: 1000000 }],
    v_gastos_neto: [{ gasto_id: 1, periodo: '2026-08-01', cuenta_codigo: '3.01', nivel: '3', estado: 'clasificado', monto_bruto: 300000, monto_neto: 300000 },
      { gasto_id: 2, periodo: '2026-09-01', cuenta_codigo: '3.07', nivel: '3', estado: 'clasificado', monto_bruto: 150000, monto_neto: 150000 },
      { gasto_id: 5, periodo: '2026-10-01', cuenta_codigo: '5.02', nivel: '5', estado: 'clasificado', monto_bruto: 119000, monto_neto: 100000, iva_recuperable: true }],
    plan_cuentas: [{ codigo: '3.01', nivel: '3', prorrateo: null }, { codigo: '3.07', nivel: '3', prorrateo: 'local' }, { codigo: '5.02', nivel: '5', prorrateo: null }],
    gestion_parametros: [{ clave: 'inicio_analisis', valor: '2026-04-01' }, { clave: 'prorrateo_local', valor: { produccion: 80, ventas: 10, administracion: 10 } }]
  }
};
// filtros de PostgREST que usa la página
function calza(f, k, v) {
  const val = f[k], txt = val == null ? null : String(val), d = x => decodeURIComponent(x);
  if (v.startsWith('eq.')) return txt === d(v.slice(3));
  if (v.startsWith('neq.')) return txt !== d(v.slice(4));
  if (v === 'is.null') return val == null;
  if (v === 'is.true') return val !== false;
  if (v.startsWith('in.(')) return v.slice(4, -1).split(',').map(x => d(x).replace(/^"|"$/g, '')).includes(txt);
  if (v.startsWith('like.')) { const re = new RegExp('^' + d(v.slice(5)).replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*') + '$'); return txt != null && re.test(txt); }
  for (const [op, fn] of [['lte.', (a, b) => a <= b], ['gte.', (a, b) => a >= b], ['lt.', (a, b) => a < b], ['gt.', (a, b) => a > b]]) if (v.startsWith(op)) return txt != null && fn(txt, d(v.slice(op.length)));
  return true;
}
const filtrar = (filas, u) => { const fs = [...u.searchParams.entries()].filter(([k]) => !['select', 'order', 'limit', 'offset', 'or', 'on_conflict'].includes(k));
  return +u.searchParams.get('offset') > 0 ? [] : filas.filter(f => fs.every(([k, v]) => calza(f, k, v))); };
const escrituras = [];
const CLAVE = { plan_proveedores_estado: 'clave', plan_config: 'clave', proveedores: 'id' };
async function ruta(r, tablas) {
  const q = r.request(), u = new URL(q.url());
  if (/\/rpc\//.test(u.pathname)) return r.fallback();
  const t = u.pathname.split('/').pop(), m = q.method();
  if (!tablas[t]) return m === 'GET' ? r.fulfill({ contentType: 'application/json', body: '[]' }) : r.fulfill({ status: 201, body: '' });
  if (m === 'GET') return r.fulfill({ contentType: 'application/json', body: JSON.stringify(filtrar(tablas[t], u)) });
  const body = q.postData() ? JSON.parse(q.postData()) : null; escrituras.push({ t, m, q: decodeURIComponent(u.search), body });
  if (m === 'PATCH') { filtrar(tablas[t], u).forEach(f => Object.assign(f, body)); return r.fulfill({ status: 204, body: '' }); }
  if (m === 'DELETE') { const fuera = new Set(filtrar(tablas[t], u)); tablas[t] = tablas[t].filter(f => !fuera.has(f)); if (t === 'plan_insumo_precios') DB.prod.plan_insumo_precios = tablas[t]; return r.fulfill({ status: 204, body: '' }); }
  const nuevas = [].concat(body).map(x => { const k = CLAVE[t], ya = k && tablas[t].find(y => String(y[k]) === String(x[k]));
    if (ya) return Object.assign(ya, x);
    const n = { created_at: ahora, ...x }; if (n.id == null) n.id = Math.max(0, ...tablas[t].map(y => +y.id || 0)) + 1; tablas[t].push(n); return n; });
  return /return=representation/.test(q.headers()['prefer'] || '') ? r.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(nuevas) }) : r.fulfill({ status: 201, body: '' });
}
const insumo = id => insumos.find(i => i.id === id), lineas = id => DB.prod.plan_insumo_precios.filter(l => l.insumo_id === id);
const config = () => JSON.parse(DB.prod.plan_config.find(c => c.clave === 'costeo_valores').valor);

(async () => {
  const b = await chromium.launch(); const errores = [];
  const ctx = await contexto(b, { tablas: {} }, { viewport: { width: 1366, height: 900 }, isMobile: false, hasTouch: false, deviceScaleFactor: 1, userAgent: undefined });
  await ctx.route(/ygcsqrylpibhofvetdyh\.supabase\.co\/rest\/v1\//, r => ruta(r, DB.prod));
  await ctx.route(/jvgifibnoigpicwklasw\.supabase\.co\/rest\/v1\//, r => ruta(r, DB.fichas));
  await ctx.route(/nnisdusdujcpkrbjqnhe\.supabase\.co\/rest\/v1\//, r => ruta(r, DB.ventas));
  const p = await ctx.newPage(); p.on('pageerror', e => errores.push(e.message));
  const dialogos = []; p.on('dialog', x => { dialogos.push(x.message()); x.accept(); });
  await p.goto('https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(2500);
  const ir = async modo => { await p.evaluate(m => { TAB = 'costeo'; renderTabs(); COSTEO_MODO = m; renderCosteo(); }, modo); await p.waitForTimeout(1200); };
  const filaProd = id => p.$eval(`#pr-cuerpo tr[data-ins="${id}"]`, t => t.innerText.replace(/\s+/g, ' ')).catch(() => '');

  // 1 · por producto: el costeo usa el más caro de los proveedores activos
  await ir('precios');
  const chips = await p.$$eval('#view-costeo .chips:first-of-type .chip', c => c.map(x => x.textContent).join(' | '));
  ok(chips === 'Pedidos | Por molde | Simular costo | Precios | Insumos por prenda | Ploteo y estampado | Gasto general', 'pestañas: ' + chips);
  ok(/\$9\.500\/kg/.test(await filaProd(1)) && /★ Telas Norte/.test(await filaProd(1)) && /\b2\b/.test(await filaProd(1)), 'Pro: dos proveedores; el costeo usa el más caro, Telas Norte $9.500/kg · ' + await filaProd(1));
  await p.evaluate(() => verPreciosProducto(1)); await p.waitForTimeout(400);
  const mod = (await p.innerText('#modal')).replace(/\s+/g, ' ');
  ok(/Textil Sur .*por kg · ancho 1,6 m · 150 g\/m² · 4,17 m por kg \$9\.000 \$9\.000\/kg · \$2\.160\/m/.test(mod) && /Telas Norte ★/.test(mod), 'detalle de Pro: cada proveedor con su ancho, gramaje y lo que equivale por kg y por metro');
  await p.evaluate(() => cerrarModal());

  // 2 · desactivar un proveedor: Pro pasa a Textil Sur
  await p.evaluate(() => { PRECIOS_VISTA = 'proveedor'; PRECIOS_PROV = 'telas norte'; renderCosteo(); }); await p.waitForTimeout(900);
  await p.click('#pr-cuerpo button:has-text("Desactivar proveedor")'); await p.waitForTimeout(1200);
  ok(/1 producto\(s\) cambian al precio de otro proveedor/.test(dialogos.join('|')), 'al desactivar avisa cuántos productos cambian de precio');
  ok(DB.prod.plan_proveedores_estado.some(x => x.clave === 'telas norte' && x.activo === false), 'queda desactivado (plan_proveedores_estado)');
  ok(insumo(1).precio === 9000 && insumo(1).proveedor === 'Textil Sur', 'Pro queda a $9.000/kg de Textil Sur (' + insumo(1).precio + ')');
  ok(DB.prod.plan_insumos_mov.some(m => m.insumo_id === 1 && m.tipo === 'edicion' && /\$9\.500 → \$9\.000 por kg \(Textil Sur, el más caro de los proveedores activos\).*Telas Norte desactivado/.test(m.nota)), 'y queda en el historial del insumo');
  ok(/Desactivado: sus precios no cuentan/.test(await p.innerText('#pr-cuerpo')), 'la ficha del proveedor dice que está desactivado');

  // 3 · tela por metro de un proveedor nuevo (se crea en Ventas): ancho y gramaje → rendimiento
  await p.evaluate(() => { cerrarModal(); PRECIOS_VISTA = 'producto'; renderCosteo(); }); await p.waitForTimeout(900);
  await p.evaluate(() => abrirLineaPrecio(2, null)); await p.waitForTimeout(300);
  await p.fill('#lp-prov', 'Tejidos Sur SpA'); await p.selectOption('#lp-pres', 'm'); await p.fill('#lp-precio', '2600'); await p.fill('#lp-ancho', '1.5'); await p.fill('#lp-gram', '160');
  await p.waitForTimeout(200);
  ok(await p.isVisible('#lp-nuevo'), 'proveedor que no está en Ventas: pide su tipo de documento para crearlo allá');
  const calc = await p.textContent('#lp-calc');
  ok(/1 metro pesa 0,24 kg · rinde 4,17 m por kg · = \$10\.833\/kg · \$2\.600\/m/.test(calc), 'calcula: ' + calc);
  await p.click('#lp-ok'); await p.waitForTimeout(300);
  ok(/tipo de documento/.test(await p.innerText('#md-err')), 'sin tipo de documento no se guarda');
  await p.selectOption('#lp-doc', 'afecta'); await p.fill('#lp-rut', '77.222.333-4'); await p.click('#lp-ok'); await p.waitForTimeout(1500);
  const pv = DB.ventas.proveedores.find(x => x.nombre === 'Tejidos Sur SpA'), ln = lineas(2).find(l => l.proveedor === 'Tejidos Sur SpA');
  ok(pv && pv.tipo_documento === 'afecta' && pv.rut === '77.222.333-4', 'el proveedor se crea en Ventas con su tipo de documento y RUT');
  ok(ln && ln.proveedor_id === pv.id && ln.presentacion === 'm' && ln.precio === 2600 && ln.ancho_m === 1.5 && ln.gramaje === 160, 'la línea queda con su proveedor de Ventas, por metro, ancho y gramaje');
  ok(cerca(insumo(2).precio, 2600, 0.01) && cerca(insumo(2).rendimiento, 4.1667, 0.001), 'Nacional (se lleva en metros) queda a $2.600/m con 4,17 m/kg: es la más cara ($10.833/kg vs $10.000/kg)');

  // 4 · papel por rollo: ancho, gramaje, metros y precio del rollo → $ por metro y por m²
  await p.evaluate(() => abrirLineaPrecio(6, 4)); await p.waitForTimeout(300);
  await p.fill('#lp-ancho', '1.6'); await p.fill('#lp-gram', '100'); await p.fill('#lp-cont', '100'); await p.fill('#lp-precio', '60000'); await p.waitForTimeout(200);
  ok(/= \$600\/m · \$375\/m²/.test(await p.textContent('#lp-calc')), 'papel: rollo de 100 m a $60.000 = $600 por metro y $375 por m²');
  await p.click('#lp-ok'); await p.waitForTimeout(1200);
  ok(insumo(6).precio === 600 && lineas(6)[0].presentacion === 'rollo' && lineas(6)[0].contenido === 100, 'el papel (stock en metros) queda a $600 por metro');

  // 5 · Ploteo y estampado: las 4 tintas, cada una con su rendimiento
  await p.evaluate(() => cerrarModal()); await ir('valores');
  const rend = { C: [11, 400], M: [12, 500], Y: [13, 500], K: [14, 800] };
  for (const [k, [id, m]] of Object.entries(rend)) { await p.selectOption('#cv-t-' + k, String(id)); await p.fill('#cv-tc-' + k, '1000'); await p.fill('#cv-tm-' + k, String(m)); }
  await p.waitForTimeout(300);
  const tr = k => p.textContent('#cv-tr-' + k);
  ok(/2,5 cc · \$125/.test(await tr('C')) && /1,25 cc · \$56,25/.test(await tr('K')), 'cian: 2,5 cc por metro × $50 = $125; negro: 1,25 cc × $45 = $56,25');
  ok(await p.textContent('#cv-ttot') === '$381', 'tinta por metro ploteado: $381 (125 + 100 + 100 + 56,25)');
  ok(/\$600 por metro/.test(await p.textContent('#cv-papel-txt')), 'papel: $600 por metro, del rollo');
  await p.click('#view-costeo .acciones .btn.pri'); await p.waitForTimeout(800);
  const T = config().tintas || {};
  ok(T.C && T.C.id === '11' && T.C.cc === 1000 && T.C.m === 400 && T.K && T.K.m === 800 && config().margen === 30, 'se guardan las 4 tintas con su rendimiento');

  // 6 · simular el costo: molde 18, tela principal Pro; la espalda (aprendida de los cortes) en Nacional y el cuello en Rib (% estimado)
  await p.evaluate(() => { SIM = { molde: '', principal: '', piezas: {}, sub: true }; }); await ir('simular');
  await p.selectOption('#sim-molde', '18'); await p.waitForTimeout(1500);
  await p.selectOption('#sim-tela', 'Pro'); await p.waitForTimeout(1500);
  const c4 = DB.prod.plan_costeo.filter(r => r.planificacion_id === 2);
  ok((c4.find(r => r.tela === 'Pro').piezas || []).join() === 'Delantero,Manga,Cuello' && (c4.find(r => r.tela === 'Nacional').piezas || []).join() === 'Espalda',
    'el corte anterior (COT-4001) se completa con las piezas de cada tela desde su ficha');
  // gramajes: Pro 150 g/m² (Textil Sur), Nacional 160 g/m² (Tejidos Sur), Rib 220 g/m²
  const cortes = [{ pr: 8, a: { Pro: 2.9 / 0.15, Nacional: 1.0 / 0.16 } }, { pr: 6, a: { Pro: 2.4 / 0.15, Nacional: 0.8 / 0.16 } }];
  const tot = c => c.a.Pro + c.a.Nacional, area = cortes.reduce((s, c) => s + tot(c), 0) / 14;
  const espalda = cortes.reduce((s, c) => s + c.a.Nacional / tot(c) * c.pr, 0) / 14;
  const pNac = 2600 * 1000 / (1.5 * 160), ploteo = 2 * 600 + 2 * 381.25 + 2 * 150, resto = 130 + 3000 + ploteo;
  const telaPro = area * 0.15 * 9000, directo = telaPro + resto, gg = 550000 / 3000000;
  const limpio = t => t.replace(/\s+/g, ' ');
  const res = limpio(await p.innerText('#sim-res'));
  const pesos = n => '$' + Math.round(n).toLocaleString('es-CL');
  ok(res.includes('Costo directo ' + pesos(directo)) && !/sugerido/i.test(res), `todo en Pro: costo directo ${pesos(directo)}, sin precio sugerido · ` + res.slice(0, 160));
  await p.fill('#sim-venta', '20000'); await p.dispatchEvent('#sim-venta', 'change'); await p.waitForTimeout(1200);
  const vres = limpio(await p.innerText('#sim-venta-res'));
  ok(vres.includes('Gasto general') && vres.includes(pesos(20000 * gg)) && vres.includes(pesos(directo + 20000 * gg)) && vres.includes(pesos(20000 - directo - 20000 * gg)),
    `precio de venta simulado $20.000: gasto general ${pesos(20000 * gg)} (sobre la venta), costo total ${pesos(directo + 20000 * gg)}, margen ${pesos(20000 - directo - 20000 * gg)}`);
  ok(/Confección promedio pagado al taller \(8 prendas\) \$3\.000/.test(res) && /Insumos por prenda lo común a todas y lo de este molde \$130/.test(res) && /2 m ploteados por prenda/.test(res), 'confección pagada, insumos comunes y 2 m ploteados por prenda');
  const piezasTx = limpio(await p.innerText('#sim-piezas'));
  ok((await p.$$('#sim-piezas select')).length === 2 && /Delantero y Manga: siempre en la tela principal/.test(await p.innerText('#view-costeo')), 'frente y mangas fijos en la tela principal; se elige la tela de la espalda y del cuello');
  const pctEsp = (Math.round(espalda * 1000) / 10).toLocaleString('es-CL');
  ok(piezasTx.includes(`${pctEsp}% de la prenda · de 2 cortes de este molde`), `la espalda es el ${pctEsp}% de la prenda, aprendido de 2 cortes · ` + piezasTx.slice(0, 140));
  await p.selectOption('#sim-piezas select[data-pieza="0"]', 'Nacional'); await p.waitForTimeout(900);
  const tela2 = area * (1 - espalda) * 0.15 * 9000 + area * espalda * 0.16 * pNac;
  const res2 = limpio(await p.innerText('#sim-res'));
  ok(res2.includes('Costo directo ' + pesos(tela2 + resto)) && /Tela · Espalda · Nacional/.test(res2) && /Tela · Delantero, Manga, Cuello · Pro/.test(res2), `espalda en Nacional: costo directo ${pesos(tela2 + resto)}`);
  // cuello en Rib: sin cortes con el cuello aparte → pide un % estimado, que queda guardado para el molde
  await p.selectOption('#sim-piezas select[data-pieza="1"]', 'Rib'); await p.waitForTimeout(900);
  ok(/qué parte de la prenda es cuello/.test(await p.innerText('#view-costeo')) && await p.isVisible('#sim-piezas input[data-est="1"]'), 'cuello en Rib sin datos: avisa y pide un % estimado');
  await p.fill('#sim-piezas input[data-est="1"]', '5'); await p.dispatchEvent('#sim-piezas input[data-est="1"]', 'change'); await p.waitForTimeout(1200);
  const est = JSON.parse((DB.prod.plan_config.find(c => c.clave === 'costeo_partes') || {}).valor || '{}');
  ok(est['18'] && est['18'].cuello === 5, 'el 5% del cuello queda guardado para el molde 18');
  const tela3 = area * (1 - espalda - 0.05) * 0.15 * 9000 + area * espalda * 0.16 * pNac + area * 0.05 * 0.22 * 12000;
  const res3 = limpio(await p.innerText('#sim-res'));
  ok(res3.includes('Costo directo ' + pesos(tela3 + resto)) && /Tela · Cuello · Rib/.test(res3), `y con el cuello en Rib (5%): costo directo ${pesos(tela3 + resto)}`);
  ok((await p.$$('#sim-otras tr')).length === 4, 'compara la misma prenda con otra tela principal (Nacional, Pro y Rib)');
  await p.screenshot({ path: 'movil/costeo_simular.png', fullPage: false });

  // 7 · una compra con su costo actualiza el precio de ese proveedor
  await p.evaluate(async () => { await cargarProvVentas(); abrirIngresoInsumo(1); }); await p.waitForTimeout(800);
  ok((await p.$$eval('#in-provs option', o => o.length)) >= 5, 'al registrar una compra, el proveedor se elige de la lista de Ventas');
  await p.fill('#in-cant', '10'); await p.fill('#in-prov', 'Textil Sur'); await p.fill('#in-costo', '9200');
  await p.click('#modal .btn.pri'); await p.waitForTimeout(1500);
  ok(lineas(1).find(l => l.id === 1).precio === 9200 && insumo(1).precio === 9200, 'la compra a Textil Sur a $9.200/kg deja ese precio en su línea y en el insumo');

  // 8 · desactivar un producto
  await p.evaluate(() => cerrarModal()); await ir('precios');
  await p.click('#pr-cuerpo tr[data-ins="4"] button:has-text("Desactivar")'); await p.waitForTimeout(900);
  ok(insumo(4).activo === false && !(await filaProd(4)), 'Etiqueta desactivada: deja de aparecer en Precios');
  await p.evaluate(() => { PRECIOS_INACT = true; pintarPreciosProducto(); });
  ok(/desactivado/.test(await filaProd(4)) && /Activar/.test(await filaProd(4)), '«Ver desactivados» la muestra con «Activar»');
  await p.screenshot({ path: 'movil/costeo_precios.png', fullPage: false });

  // 9 · Insumos por prenda: botón para crear un insumo
  await ir('consumo');
  ok(/Común a todas las prendas/.test(await p.innerText('#view-costeo')) && await p.isVisible('#view-costeo button:has-text("+ Nuevo insumo")'), 'Insumos por prenda: explica lo común y permite crear un insumo');

  ok(errores.length === 0, 'sin errores de JavaScript ' + errores.join(' | '));
  await b.close(); console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
