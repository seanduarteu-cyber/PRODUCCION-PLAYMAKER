// Catálogo ordenado (noviembre 2026): orden y secciones del catálogo en el panel de fichas y en Planificación,
// moldes nuevos 83 y 84, y que nada se rompa si la base aún no tiene el SQL 17A o no responde.
const { chromium, contexto } = require('./comun_movil');
const CON_17A = require('./datos_moldes_catalogo.json');      // la tabla moldes después del SQL 17A
const ANTES_17A = require('./datos_moldes_antes_17a.json');   // la tabla como estaba (sin orden, deportes antiguos, sin 83 ni 84)
const SECCIONES = ['Fútbol', 'Básquetbol', 'Vóleibol', 'Hockey', 'Rugby', 'Multideporte', 'Salida y entrenamiento'];
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const hoy = new Date().toISOString().slice(0, 10), ahora = new Date().toISOString();
// ficha de rugby con una calza (E05, que en el catálogo quedó en Vóleibol): el molde elegido no se puede perder
const ficha = { id: 1, ref: 'COT-3610', proyecto: 'Uniformes 2026', cliente: 'Club Rugby', vendedor: 'Sean Duarte', entrega: hoy, entrega_interna: hoy, entrega_cliente: hoy,
  estado: 'abierto', created_at: ahora, imagenes: [], items: [{ prenda: 'camiseta', cant: 22 }, { prenda: 'short', cant: 22 }],
  specs: { camiseta: { deporte: 'Rugby', moldes: { Masculino: 'RB-HOMU02|58', Femenino: 'RB-MUJU02|111' }, unidades: { Masculino: 12, Femenino: 10 } },
           short: { deporte: 'Rugby', moldes: { Masculino: 'CA-MUJ|105' }, unidades: { Masculino: 22 } } } };
const datosCon = moldes => ({ tablas: { fichas_tallas: [ficha], fichas_detalle: [], fichas_avisos: [], catalogo_tecnico: [], pedidos: [], moldes,
  planificacion: [], planificacion_etapas: [], plan_usuarios: [], ejecutantes: [] } });
// modo: 'con17a' · 'sin17a' (la columna orden no existe: la base responde 400 si se pide) · 'sinbase' (moldes no responde)
async function abrir(b, modo) {
  const ctx = await contexto(b, datosCon(modo === 'con17a' ? CON_17A : ANTES_17A), { viewport: { width: 1280, height: 900 }, isMobile: false, hasTouch: false, userAgent: undefined });
  await ctx.route(/supabase\.co\/rest\/v1\/moldes/, r => {
    const u = new URL(r.request().url());
    if (modo === 'sinbase') return r.fulfill({ status: 503, body: 'sin conexión' });
    if (modo === 'sin17a' && /orden/.test(u.searchParams.get('select') || '')) return r.fulfill({ status: 400, contentType: 'application/json', body: '{"message":"column moldes.orden does not exist"}' });
    return r.fallback();
  });
  const p = await ctx.newPage(); p.errores = []; p.on('pageerror', e => p.errores.push(e.message)); p.on('dialog', d => d.accept());
  return p;
}
async function panel(b, modo) {
  const p = await abrir(b, modo), r = {};
  const valores = sel => p.$$eval(sel + ' option', os => os.map(o => o.value).filter(v => v && v !== '__manual').map(v => +v.split('|')[1]));
  await p.goto('https://panel-fichas-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(1500);
  // catálogo al crear una ficha: todos los moldes, sus deportes y, con Hockey, primero los de hockey
  await p.goto('https://panel-fichas-playmaker.netlify.app/'); await p.waitForTimeout(1000);
  await p.click('[data-ir="crear"]'); await p.waitForTimeout(600);
  await p.click('#btn-catalogo'); await p.waitForTimeout(400);
  r.orden = await p.$$eval('[data-add-molde]', bs => bs.map(x => +x.dataset.addMolde));
  r.secciones = await p.$$eval('[data-cf="deporte"] option', os => os.map(o => o.value).filter(Boolean));
  await p.selectOption('[data-cf="deporte"]', 'Hockey'); await p.waitForTimeout(400);
  r.catHockey = await p.$$eval('[data-add-molde]', bs => bs.map(x => +x.dataset.addMolde));
  await p.selectOption('[data-cf="deporte"]', 'Rugby'); await p.waitForTimeout(300);
  r.catRugby = await p.$$eval('[data-add-molde]', bs => bs.map(x => +x.dataset.addMolde));
  await p.selectOption('[data-cf="deporte"]', 'Fútbol'); await p.waitForTimeout(300);
  r.catFutbol = await p.$$eval('[data-add-molde]', bs => bs.map(x => +x.dataset.addMolde));
  // ficha técnica: los moldes ya elegidos siguen elegidos; la lista de cada calce según el deporte
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3610'); await p.waitForTimeout(1500);
  await p.click('[data-ir="tecnica"]'); await p.waitForTimeout(800);
  r.elegidos = await p.evaluate(() => [...document.querySelectorAll('select[data-molde]')].map(s => s.dataset.molde + '/' + s.dataset.calce + '=' + s.value));
  r.rugbyFem = await valores('#m-camiseta-Femenino');
  r.rugbyMas = await valores('#m-camiseta-Masculino');
  await p.evaluate(() => { const x = document.getElementById('dep-camiseta'); x.value = 'Hockey'; x.dispatchEvent(new Event('change', { bubbles: true })); });
  await p.waitForTimeout(500);
  r.hockeyFem = await valores('#m-camiseta-Femenino');
  r.femTrasCambio = await p.$eval('#m-camiseta-Femenino', s => s.value);
  r.masTrasCambio = await p.$eval('#m-camiseta-Masculino', s => s.value);
  await p.evaluate(() => { const x = document.getElementById('dep-camiseta'); x.value = 'Fútbol'; x.dispatchEvent(new Event('change', { bubbles: true })); });
  await p.waitForTimeout(500);
  r.futMas = (await valores('#m-camiseta-Masculino')).filter(n => n !== 58);   // el 58 es el ya elegido: se mantiene arriba
  // pantalla «Catálogo de moldes» (desde la ficha técnica)
  if (modo !== 'sinbase') {
    await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3610'); await p.waitForTimeout(1500);
    await p.click('[data-ir="tecnica"]'); await p.waitForTimeout(800);
    await p.click('[data-ir="catalogo"]'); await p.waitForTimeout(800);
    await p.click('[data-ir="moldes"]'); await p.waitForTimeout(800);
    r.titulos = await p.$$eval('.mc-seccion', xs => xs.map(x => x.textContent));
    r.tarjetas = await p.$$eval('.molde-card .mc-cab b', xs => xs.map(x => x.textContent.split(' · ')[0]));
    const srcs = await p.$$eval('.molde-card .mc-guia a', as => as.map(a => a.href));
    r.guia01 = srcs[0] || ''; r.guia83 = srcs.find(s => /molde-83/.test(s)) || '';
    r.guiaServida = await p.evaluate(u => fetch(u).then(x => x.status).catch(() => 0), (r.guia83 || '').split('?')[0]);
    await p.screenshot({ path: 'movil/catalogo_panel_' + modo + '.png' });
  }
  r.errores = p.errores; await p.context().close();
  return r;
}
async function plan(b, modo) {
  const p = await abrir(b, modo), r = {};
  await p.goto('https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(2500);
  r.grupos = await p.evaluate(() => GRUPOS_PRENDA.filter(g => g.moldes).map(g => [g.grupo, g.tipos.map(t => t.split(' · ')[0])]));
  await p.evaluate(() => { TAB = 'moldes'; renderTabs(); renderVista(); }); await p.waitForTimeout(500);
  r.titulos = await p.$$eval('#view-moldes th[colspan]', xs => xs.map(x => x.textContent));
  r.filas = await p.$$eval('#view-moldes tr td:first-child b', xs => xs.map(x => x.textContent));
  r.guia83 = await p.$$eval('#view-moldes tr', trs => { const t = trs.find(x => (x.querySelector('td b') || {}).textContent === '83'); return t ? t.querySelector('a').getAttribute('href') : ''; });
  r.guiaServida = await p.evaluate(u => fetch(u).then(x => x.status).catch(() => 0), r.guia83);
  r.guiasArchivo = require('fs').readdirSync(require('path').resolve(__dirname, '../sistemas/produccion/guias')).filter(f => /^molde-(E\d\d|\d\d)\.jpg$/.test(f)).length;
  await p.fill('#q-moldes', 'hockey'); await p.waitForTimeout(300);
  r.buscaHockey = await p.$$eval('#view-moldes tr td:first-child b', xs => xs.map(x => x.textContent));
  if (modo !== 'sinbase') {
    await p.evaluate(() => { TAB = 'config'; renderTabs(); renderVista(); }); await p.waitForTimeout(1200);
    r.config = await p.$$eval('#cfg-prendas details > summary', xs => xs.map(x => x.textContent.split(' · ')[0]));
  }
  r.errores = p.errores; await p.context().close();
  return r;
}
const es = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const COD = {}; CON_17A.forEach(m => { COD[m.numero] = m.codigo; });
const de = (ns, pref) => ns.filter(n => new RegExp('^' + pref).test(COD[n] || ''));
function sinMezcla(r, cuando) {
  ok(!de(r.catRugby, 'FUT').length && de(r.catRugby, 'RB').length >= 10, cuando + 'catálogo con Rugby: ningún molde de fútbol (' + (de(r.catRugby, 'FUT').join(',') || 'ninguno') + ')');
  ok(!de(r.catFutbol, 'RB').length && de(r.catFutbol, 'FUT').length >= 20, cuando + 'catálogo con Fútbol: ningún molde de rugby (' + (de(r.catFutbol, 'RB').join(',') || 'ninguno') + ')');
  ok(!de(r.rugbyMas, 'FUT').length && r.rugbyMas.includes(58) && r.rugbyMas.includes(110), cuando + 'ficha técnica, camiseta de rugby: solo moldes de rugby (y multideporte): ' + r.rugbyMas.join(','));
  ok(!de(r.futMas, 'RB').length && r.futMas.includes(104), cuando + 'ficha técnica, camiseta de fútbol: sin moldes de rugby, con E04: ' + r.futMas.join(','));
}
(async () => {
  const b = await chromium.launch();
  console.log('— Panel de fichas, base con el SQL 17A');
  let r = await panel(b, 'con17a');
  ok(r.orden.slice(0, 3).join() === '1,2,3' && r.orden.indexOf(104) === 28 && r.orden.indexOf(69) === 33, 'moldes en el orden del catálogo completo: parte en 01, E04 después del 28, 69 cierra Fútbol');
  ok(es(r.secciones, SECCIONES), 'secciones del catálogo en orden: ' + r.secciones.join(', '));
  ok(r.orden.length === 95 && r.orden[94] === 68, 'los 95 moldes del catálogo, el último es el 68 (Salida y entrenamiento)');
  ok(r.rugbyFem.slice(0, 5).join() === '59,61,63,111,83', 'ficha técnica, camiseta femenina de rugby: primero las de Rugby, con E11 y el 83 nuevo (' + r.rugbyFem.slice(0, 6).join(',') + '…)');
  ok(r.hockeyFem.slice(0, 4).join() === '111,64,65,84', 'con Hockey: el ya elegido (E11) arriba, luego 64, 65 y el 84 nuevo (' + r.hockeyFem.slice(0, 5).join(',') + '…)');
  ok(r.femTrasCambio === 'RB-MUJU02|111' && r.masTrasCambio === 'RB-HOMU02|58', 'cambiar el deporte no borra los moldes ya elegidos (ni el 58, que es de Rugby)');
  ok(es(r.titulos, SECCIONES), 'pantalla «Catálogo de moldes» con el título de cada sección (ninguno fuera del catálogo)');
  ok(/planificacion-playmaker\.netlify\.app\/guias\/molde-01\.jpg/.test(r.guia01) && /guias\/molde-83\.jpg/.test(r.guia83) && r.guiaServida === 200, 'guías del catálogo: el panel las toma del sistema (' + r.guia83 + ' → ' + r.guiaServida + ')');
  ok(r.tarjetas[0] === '01' && r.tarjetas.length === 95 && r.tarjetas.indexOf('83') > r.tarjetas.indexOf('E11') && r.tarjetas.indexOf('84') === r.tarjetas.indexOf('E09') + 1, 'tarjetas en el orden del catálogo (83 tras E11, 84 tras E09)');
  sinMezcla(r, '');
  ok(r.catHockey.slice(0, 7).join() === '64,65,106,107,108,109,84' && !r.catHockey.includes(104) && r.catHockey.includes(80), 'catálogo con Hockey: los de Hockey y después multideporte y salida, sin especiales de otro deporte (' + r.catHockey.slice(0, 9).join(',') + '…)');
  ok(r.elegidos.includes('camiseta/Masculino=RB-HOMU02|58') && r.elegidos.includes('short/Masculino=CA-MUJ|105'), 'ficha técnica: los moldes ya elegidos siguen elegidos (incluida la calza E05 en una ficha de rugby)');
  ok(!r.errores.length, 'sin errores JS ' + r.errores.join(' | '));

  console.log('— Panel de fichas, base sin el SQL 17A');
  r = await panel(b, 'sin17a');
  ok(r.orden.slice(0, 3).join() === '1,2,3' && !r.orden.includes(83) && r.orden[r.orden.length - 1] === 68, 'sin la columna orden: toma el orden y las secciones del catálogo completo');
  sinMezcla(r, 'sin SQL 17A · ');
  ok(es(r.titulos, SECCIONES), 'pantalla «Catálogo de moldes» con las secciones del catálogo, cada una una vez (' + r.titulos.join(', ') + ')');
  ok(r.elegidos.includes('short/Masculino=CA-MUJ|105') && !r.errores.length, 'ficha técnica y moldes sin errores ' + r.errores.join(' | '));

  console.log('— Panel de fichas, sin conexión a la tabla moldes (respaldo del código)');
  r = await panel(b, 'sinbase');
  ok(r.orden.slice(0, 3).join() === '1,2,3' && r.orden.length === 95, 'el respaldo ya trae el catálogo completo (95 moldes)');
  ok(!r.errores.length, 'sin errores JS ' + r.errores.join(' | '));

  console.log('— Planificación, base con el SQL 17A');
  r = await plan(b, 'con17a');
  ok(es(r.grupos.map(g => g[0]), SECCIONES), 'lista de moldes al ingresar un pedido, por sección del catálogo: ' + r.grupos.map(g => g[0]).join(', '));
  const g = Object.fromEntries(r.grupos);
  ok(g['Fútbol'][0] === '01' && g['Fútbol'].indexOf('E04') === 28 && g['Fútbol'][g['Fútbol'].length - 1] === '69' && g['Fútbol'].length === 34, 'Fútbol en el orden del catálogo completo (01 al 28, E04, 72 al 75 y 69)');
  ok(g['Rugby'].includes('83') && g['Hockey'].includes('84') && g['Rugby'].includes('E01'), 'Rugby trae el 83 y los E01…; Hockey el 84');
  ok(es(r.titulos, SECCIONES), '«Moldes vigentes» con el título de cada sección');
  ok(r.guia83 === 'guias/molde-83.jpg' && r.guiaServida === 200 && r.guiasArchivo === 95, '«Ver guía» abre la guía del catálogo que viene con el sitio (' + r.guiasArchivo + ' de 95 en la carpeta guias)');
  ok(r.filas[0] === '01' && r.filas.includes('83') && r.filas.includes('84') && r.filas.length === 95, '«Moldes vigentes»: los 95, desde el 01');
  ok(r.buscaHockey.join() === '64,65,E06,E07,E08,E09,84', 'buscar «hockey» encuentra la sección completa (' + r.buscaHockey.join(',') + ')');
  ok(es(r.config, SECCIONES.concat([])) || es(r.config.slice(0, 7), SECCIONES), 'Configuración › catálogo de moldes agrupado por sección, en orden: ' + r.config.join(', '));
  ok(!r.errores.length, 'sin errores JS ' + r.errores.join(' | '));

  console.log('— Planificación, base sin el SQL 17A');
  r = await plan(b, 'sin17a');
  ok(es(r.grupos.map(g => g[0]), SECCIONES) && r.grupos[0][1][0] === '01', 'sin la columna orden: las mismas secciones del catálogo (sin grupo «Especiales»): ' + r.grupos.map(g => g[0]).join(', '));
  const gs = Object.fromEntries(r.grupos);
  ok(gs['Fútbol'].includes('E04') && !gs['Fútbol'].some(k => /^E(01|02|03|10|11)$/.test(k)) && gs['Rugby'].includes('E01') && !gs['Rugby'].includes('E04'), 'sin la columna orden: E04 en Fútbol y E01, E02, E03, E10, E11 en Rugby');
  ok(es(r.titulos, SECCIONES), '«Moldes vigentes» con las secciones del catálogo (' + r.titulos.join(', ') + ')');
  ok(r.config.length >= 5 && !r.errores.length, 'Configuración sin errores ' + r.errores.join(' | '));

  console.log('— Planificación, sin conexión a la tabla moldes (respaldo del código)');
  r = await plan(b, 'sinbase');
  ok(es(r.grupos.map(g => g[0]).slice(0, 7), SECCIONES) && Object.fromEntries(r.grupos)['Rugby'].includes('83'), 'el respaldo arma las mismas secciones, con 83 y 84');
  ok(!r.errores.length, 'sin errores JS ' + r.errores.join(' | '));
  await b.close();
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
