// Costeo › Estampado y aplicaciones (SQL 23C): al terminar Estampado se registran las aplicaciones de cada molde
// (escudos del listado de Precios), cuántas por prenda y las bajadas de plancha; entran al costeo del pedido y al
// simulador con el precio por bajada de plancha. Bases simuladas con estado.
const { chromium, contexto } = require('./comun_movil');
const { rutaConEstado } = require('./base_simulada');
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const d = n => { const x = new Date(); x.setDate(x.getDate() + n); return x.toISOString().slice(0, 10); };
const ahora = new Date().toISOString();
const moldes = require('./datos_moldes_catalogo.json').map(m => Object.assign({}, m));
const ins = (id, nombre, categoria, unidad, precio) => ({ id, nombre, categoria, unidad, precio, rendimiento: null, stock: 100, activo: true });
const insumos = [ins(1, 'Pro', 'Tela', 'kg', 9000), ins(31, 'Escudo vinilo', 'Aplicación', 'unid', 800), ins(32, 'Escudo texturizado', 'Aplicación', 'unid', 1500), ins(4, 'Etiqueta', 'Etiqueta', 'unid', 50)];
const ped = (id, cot, prendas, extra) => ({ id, cot, cliente: 'Club ' + cot, prendas, desglose: { '18 · FUTHOMU02': prendas }, fecha_ingreso_ficha: d(-3), fecha_entrega_cliente: d(20),
  fecha_termino_interno: d(14), tipo: 'normal', requiere_estampado: true, requiere_sublimacion: true, estado_general: 'en_produccion', created_at: ahora, ...extra });
const ETS = ['ARMADO', 'CORTE', 'REVISION', 'PLOTEO', 'SUBL', 'CONFEC', 'ESTAMP', 'ENTREGA'];
const etapas = []; let eid = 1;
[[1, 'ESTAMP'], [2, 'ESTAMP'], [3, 'ARMADO']].forEach(([pid, actual]) => ETS.forEach((k, j) => {
  const ia = ETS.indexOf(actual); etapas.push({ id: eid++, planificacion_id: pid, etapa: k, orden: j + 1, estado: j < ia ? 'terminado' : j === ia ? 'en_proceso' : 'pendiente',
    fecha_inicio_plan: d(-2), fecha_limite: d(5 + j), fecha_inicio_real: j <= ia ? ahora : null, fecha_termino_real: j < ia ? ahora : null }); }));
const DB = {
  prod: {
    planificacion: [ped(1, 'COT-5000', 10), ped(2, 'COT-5001', 6), ped(3, 'COT-5002', 4)], planificacion_etapas: etapas, planificacion_log: [],
    plan_insumos: insumos, plan_insumos_stock: insumos, plan_insumos_mov: [], plan_insumo_precios: [], plan_insumos_molde: [],
    plan_config: [{ clave: 'costeo_valores', valor: JSON.stringify({ papel: '', prot: '', protF: 1, margen: 30 }) }],
    plan_costeo: [], plan_asignaciones: [], plan_tarifas: [{ tipo: '18 · FUTHOMU02', precio: 2800 }],
    plan_usuarios: [{ usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'], activo: true }]
  },
  fichas: { moldes, catalogo_tecnico: [],
    fichas_tallas: [{ id: 1, ref: 'COT-5000', cliente: 'Club COT-5000', estado: 'confirmado', items: [{ prenda: 'camiseta', cant: 10 }], created_at: ahora,
      specs: { camiseta: { tela: 'Pro', aplicacion: 'Escudo texturizado', moldes: { Masculino: 'FUTHOMU02|18' } } } }],
    fichas_detalle: Array.from({ length: 10 }, (_, i) => ({ id: 'p' + i, ref: 'COT-5000', calce: 'Masculino', manga: 'Corta', tallas: { camiseta: 'M' }, created_at: ahora })) },
  ventas: {}
};
const costeo = () => DB.prod.plan_costeo, config = () => JSON.parse(DB.prod.plan_config.find(c => c.clave === 'costeo_valores').valor);

(async () => {
  const b = await chromium.launch(); const errores = [];
  const ctx = await contexto(b, { tablas: {} }, { viewport: { width: 1366, height: 900 }, isMobile: false, hasTouch: false, deviceScaleFactor: 1, userAgent: undefined });
  await ctx.route(/ygcsqrylpibhofvetdyh\.supabase\.co\/rest\/v1\//, rutaConEstado(DB.prod));
  await ctx.route(/jvgifibnoigpicwklasw\.supabase\.co\/rest\/v1\//, rutaConEstado(DB.fichas));
  await ctx.route(/nnisdusdujcpkrbjqnhe\.supabase\.co\/rest\/v1\//, rutaConEstado(DB.ventas));
  const p = await ctx.newPage(); p.on('pageerror', e => errores.push(e.message));
  const dialogos = []; p.on('dialog', x => { dialogos.push(x.message()); x.accept(); });
  await p.goto('https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(2500);
  const costeoModo = async m => { await p.evaluate(m => { TAB = 'costeo'; renderTabs(); COSTEO_MODO = m; COSTEO_DATOS = null; renderCosteo(); }, m); await p.waitForTimeout(1300); };

  // 1 · precio por bajada de plancha (uno para todo)
  await costeoModo('valores');
  ok(/Ploteo, estampado y margen/.test(await p.innerText('#view-costeo .chips')), 'la pestaña se llama «Ploteo, estampado y margen»');
  await p.fill('#cv-bajada', '150'); await p.click('#view-costeo .acciones .btn.pri'); await p.waitForTimeout(800);
  ok(config().bajada === 150, 'se guarda el precio por bajada de plancha: $150');
  ok(await p.evaluate(() => CATEG_INS.includes('Aplicación')), 'los insumos tienen la categoría «Aplicación»');

  // 2 · al terminar Estampado se registran las aplicaciones (precargadas desde la ficha)
  await p.evaluate(() => { AREA_SEL = 'ESTAMP'; irTab('area'); }); await p.waitForTimeout(800);
  ok(/Registrar aplicaciones/.test(await p.innerText('#view-area')), 'la tarjeta de Estampado tiene «Registrar aplicaciones»');
  await p.evaluate(() => accionEtapa(1, 'ESTAMP', 'terminar')); await p.waitForTimeout(1500);
  const modal = await p.innerText('#modal');
  ok(/Estampado · COT-5000/.test(modal) && /La ficha dice: Escudo texturizado/.test(modal) && /No lleva aplicaciones/.test(modal), 'al terminar se abre el registro de estampado, con lo que dice la ficha');
  ok(await p.$eval('#re-i-0-0', s => s.options[s.selectedIndex].text) === 'Escudo texturizado · $1.500/unid' && await p.inputValue('#re-u-0') === '10', 'viene con el escudo texturizado de la ficha y las 10 prendas');
  await p.click('#modal button:has-text("+ Agregar aplicación")'); await p.waitForTimeout(200);
  await p.selectOption('#re-i-0-1', '31'); await p.fill('#re-c-0-1', '2'); await p.fill('#re-b-0-1', '1');
  await p.click('#modal .btn.pri'); await p.waitForTimeout(2000);
  const es = costeo().filter(r => r.planificacion_id === 1 && r.etapa === 'ESTAMP');
  const tex = es.find(r => r.insumo_id === 32), vin = es.find(r => r.insumo_id === 31);
  ok(es.length === 2 && tex && tex.cantidad === 1 && tex.bajadas === 1 && tex.prendas === 10 && vin && vin.cantidad === 2 && vin.bajadas === 1 && vin.tela === 'Escudo vinilo',
    'quedan las dos aplicaciones del molde: texturizado 1 por prenda (1 bajada), vinilo 2 por prenda (1 bajada)');
  const movs = DB.prod.plan_insumos_mov.filter(m => m.planificacion_id === 1 && m.tipo === 'consumo').map(m => m.insumo_id + ':' + m.cantidad).sort().join(' ');
  ok(movs === '31:-20 32:-10', 'salen del stock: 20 escudos vinilo y 10 texturizados (' + movs + ')');
  ok(etapas.find(e => e.planificacion_id === 1 && e.etapa === 'ESTAMP').estado === 'terminado', 'y el estampado se termina');

  // 3 · «No lleva aplicaciones»
  await p.evaluate(() => accionEtapa(2, 'ESTAMP', 'terminar')); await p.waitForTimeout(1500);
  await p.click('#modal button:has-text("No lleva aplicaciones")'); await p.waitForTimeout(1800);
  const es2 = costeo().filter(r => r.planificacion_id === 2 && r.etapa === 'ESTAMP');
  ok(es2.length === 1 && es2[0].tela === '' && es2[0].cantidad === 0 && etapas.find(e => e.planificacion_id === 2 && e.etapa === 'ESTAMP').estado === 'terminado', '«No lleva aplicaciones» lo deja registrado y termina el estampado');

  // 4 · costeo del pedido: aplicaciones + bajadas de plancha
  await costeoModo('pedidos');
  await p.evaluate(() => verCosteo(1)); await p.waitForTimeout(900);
  const det = (await p.innerText('#modal')).replace(/\s+/g, ' ');
  // 10 × 1 × $1.500 + 10 × 2 × $800 = $31.000; bajadas 10 × (1 + 1) = 20 × $150 = $3.000
  ok(/Estampado y aplicaciones Escudo (texturizado|vinilo).*20 bajadas de plancha \(\$3\.000\) \$34\.000/.test(det), 'detalle: estampado $34.000 = aplicaciones $31.000 + 20 bajadas × $150 · ' + (det.match(/Estampado y aplicaciones[^$]*\$[\d.]+[^$]*\$[\d.]+/) || [''])[0]);
  ok(/Registrar o editar aplicaciones/.test(det), 'desde el detalle se puede registrar o editar');
  await p.evaluate(() => cerrarModal());
  const faltan = await p.evaluate(() => Object.fromEntries(COSTEO_DATOS.proy.map(x => [x.cot, costeoDe(x).faltan.join(' · ')])));
  ok(/aplicaciones del estampado/.test(faltan['COT-5002']) && !/aplicaciones del estampado/.test(faltan['COT-5001']) && !/aplicaciones del estampado/.test(faltan['COT-5000']),
    'un pedido con estampado sin registro avisa «falta: aplicaciones del estampado»; el que no lleva o ya registró, no');

  // 5 · editar desde Costeo: el registro trae lo guardado
  await p.evaluate(() => abrirRegistroCosteo(1, 'ESTAMP')); await p.waitForTimeout(1200);
  ok((await p.$$('#re-moldes select')).length === 2 && await p.inputValue('#re-c-0-1') === '2', 'al editar trae las aplicaciones guardadas');
  await p.click('#modal button:has-text("×") >> nth=1'); await p.waitForTimeout(200);
  await p.click('#modal .btn.pri'); await p.waitForTimeout(1500);
  ok(costeo().filter(r => r.planificacion_id === 1 && r.etapa === 'ESTAMP').length === 1 && DB.prod.plan_insumos_mov.filter(m => m.planificacion_id === 1 && m.insumo_id === 31).length === 0,
    'al quitar el vinilo se borra su registro y vuelve al stock');

  // 6 · simulador: aplicaciones y bajadas
  await p.evaluate(() => { SIM = { molde: '18', principal: 'Pro', piezas: {}, sub: false }; }); await costeoModo('simular');
  await p.click('#view-costeo button:has-text("+ Agregar aplicación")'); await p.waitForTimeout(700);
  await p.selectOption('#sim-aplic select[data-aplic="0"]', '32'); await p.waitForTimeout(700);
  await p.fill('#sim-aplic tr:nth-child(2) input >> nth=0', '2'); await p.dispatchEvent('#sim-aplic tr:nth-child(2) input >> nth=0', 'change'); await p.waitForTimeout(900);
  const res = (await p.innerText('#sim-res')).replace(/\s+/g, ' ');
  ok(/Aplicaciones Escudo texturizado × 2 \$3\.000/.test(res) && /Bajadas de plancha 2 × \$150 \$300/.test(res), 'simulador: 2 escudos texturizados ($3.000) y 2 bajadas de plancha ($300) · ' + (res.match(/Aplicaciones.*?Costo directo/) || [''])[0]);
  await p.screenshot({ path: 'movil/costeo_estampado.png', fullPage: false });

  ok(errores.length === 0, 'sin errores de JavaScript ' + errores.join(' | '));
  await b.close(); console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
