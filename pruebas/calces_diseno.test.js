// Un diseño con varios calces (un molde por calce) en una sola hoja de la ficha de producción; unir diseños que se
// cargaron por separado sin volver a cargar personas; aviso de personas en un calce sin molde (lo que Planificación
// no deja ingresar) y copiar la configuración de telas a otros diseños. Bases simuladas, con estado.
const { chromium, contexto } = require('./comun_movil');
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const hoy = new Date().toISOString().slice(0, 10), ahora = new Date().toISOString();
const moldes = require('./datos_moldes_catalogo.json').map(m => Object.assign({}, m));
const pz = ['Delantero', 'Espalda', 'Manga'];
moldes.forEach(m => { if ([17, 18, 20].indexOf(m.numero) >= 0) m.piezas = pz.map(p => ({ pieza: p, cant: 1, tela: '' })); });

// COT-3900: «Jugadores» (masculino, 18) y «Jugadoras» (femenino, 17) cargados como dos diseños; un niño quedó en «Jugadores»
const ficha = { id: 1, ref: 'COT-3900', proyecto: 'Club mixto', cliente: 'Club Prueba', vendedor: 'Sean Duarte', entrega: hoy, entrega_interna: hoy, entrega_cliente: hoy,
  estado: 'confirmado', created_at: ahora,
  items: [{ prenda: 'camiseta', cant: 3 }, { prenda: 'camiseta_2', cant: 2 }, { prenda: 'short', cant: 3 }],
  specs: { camiseta: { nombre: 'Jugadores', deporte: 'Fútbol', tela: 'Pro', moldes: { Masculino: 'FUTHOMU02|18' }, unidades: { Masculino: 3 },
      despiece: { molde: '18 · FUTHOMU02', piezas: [{ pieza: 'Delantero', cant: 1, tela: 'Pro azul', detalle: 'Sublimada' }, { pieza: 'Espalda', cant: 1, tela: 'Pro azul', detalle: 'Sublimada' }, { pieza: 'Manga', cant: 2, tela: 'Pro blanco', detalle: '' }] } },
    camiseta_2: { nombre: 'Jugadoras', moldes: { Femenino: 'FUTMUJU02|17' }, unidades: { Femenino: 2 }, nota: 'Escudo bordado' },
    short: { moldes: { Masculino: 'BK-SH|46', Femenino: 'BK-SH|46' }, unidades: { Masculino: 2, Femenino: 1 }, tela: 'Nacional' } },
  imagenes: [{ url: 'https://x.test/cam.jpg', prendas: ['camiseta'], prenda: 'camiseta', moldes: ['FUTHOMU02|18'], vista: 'Completo', path: 'a/1.jpg' },
    { url: 'https://x.test/fem.jpg', prendas: ['camiseta_2'], prenda: 'camiseta_2', moldes: ['FUTMUJU02|17'], vista: 'Completo', path: 'a/2.jpg' }] };
const per = (id, nom, num, calce, t, sh) => ({ id: id, ref: 'COT-3900', nombre: nom, estampado: nom.toUpperCase(), numero: num, calce: calce, manga: 'Corta', arquero: false, obs: '',
  tallas: Object.assign(t, sh ? { short: sh } : {}), disenos: {}, created_at: ahora });
const personas = [per('p1', 'Ana', '1', 'Masculino', { camiseta: 'S' }, 'S'), per('p2', 'Beto', '2', 'Masculino', { camiseta: 'M' }, 'M'),
  per('p3', 'Caro', '3', 'Infantil', { camiseta: '10' }, null), per('p4', 'Dani', '4', 'Femenino', { camiseta_2: 'S' }, null), per('p5', 'Eli', '5', 'Femenino', { camiseta_2: 'M' }, 'L')];
const original = JSON.parse(JSON.stringify({ ficha: ficha, personas: personas }));
// COT-3901: tres camisetas con la misma configuración de telas (se copia desde la primera)
const ficha2 = { id: 2, ref: 'COT-3901', proyecto: 'Muchos moldes', cliente: 'Club Dos', vendedor: 'Sean Duarte', entrega: hoy, entrega_cliente: hoy, estado: 'abierto', created_at: ahora,
  items: [{ prenda: 'camiseta', cant: 2 }, { prenda: 'camiseta_2', cant: 2 }, { prenda: 'camiseta_3', cant: 2 }, { prenda: 'short', cant: 2 }], imagenes: [],
  specs: { camiseta: { nombre: 'A', tela: 'Pro', aplicacion: 'Sublimado', moldes: { Masculino: 'FUTHOMU02|18' }, unidades: { Masculino: 2 },
      despiece: { molde: '18 · FUTHOMU02', piezas: [{ pieza: 'Delantero', cant: 1, tela: 'Pro azul', detalle: 'Sublimada' }, { pieza: 'Manga', cant: 2, tela: 'Pro blanco', detalle: 'Color de tela (sin sublimar)' }] } },
    camiseta_2: { nombre: 'B', moldes: { Femenino: 'FUTMUJU02|17' }, unidades: { Femenino: 2 }, nota: 'Solo B' },
    camiseta_3: { nombre: 'C', moldes: { Infantil: 'FUTINHOMU02|20' }, unidades: { Infantil: 2 }, despiece: { molde: '20 · FUTINHOMU02', piezas: [{ pieza: 'Delantero', cant: 1, tela: '', detalle: '' }, { pieza: 'Cuello', cant: 1, tela: 'Rib', detalle: '' }] } },
    short: { moldes: { Masculino: 'BK-SH|46' }, unidades: { Masculino: 2 } } } };
const porRef = filas => u => { const m = (u.searchParams.get('ref') || '').replace(/^eq\./, ''); return m ? filas.filter(f => f.ref === m) : filas; };
const fichas = [ficha, ficha2];
const datos = { tablas: { fichas_tallas: porRef(fichas), fichas_detalle: porRef(personas), fichas_avisos: [], moldes, catalogo_tecnico: [], pedidos: [] } };

(async () => {
  const b = await chromium.launch();
  const ctx = await contexto(b, datos, { viewport: { width: 1280, height: 900 }, isMobile: false, hasTouch: false, userAgent: undefined });
  const envios = [];
  // la base simulada guarda lo que se envía (personas y ficha), para ver el resultado al volver a cargar
  await ctx.route(/supabase\.co\/(rest\/v1\/fichas_(tallas|detalle|avisos)|storage)/, r => {
    const q = r.request(); if (q.method() === 'GET') return r.fallback();
    const u = decodeURIComponent(q.url()), d = q.postData() ? JSON.parse(q.postData()) : null;
    envios.push({ m: q.method(), u: u, d: d });
    if (q.method() === 'POST' && /fichas_detalle/.test(u)) [].concat(d).forEach(x => { const k = personas.findIndex(y => y.id === x.id); if (k >= 0) personas[k] = x; else personas.push(x); });
    if (q.method() === 'PATCH' && /fichas_tallas/.test(u)) { const ref = (u.match(/ref=eq\.([^&]+)/) || [])[1]; const fi = fichas.find(x => x.ref === ref); if (fi) Object.assign(fi, d); }
    return r.fulfill({ contentType: 'application/json', body: '[]' });
  });
  const p = await ctx.newPage(); const errores = []; p.on('pageerror', e => errores.push(e.message)); p.on('dialog', d => d.accept());
  const texto = sel => p.innerText(sel || '#app').catch(() => '');
  const hojas = () => p.$$eval('section.fp:not(.portada)', ss => ss.map(s => ({ d: (s.querySelector('.diseno-hoja') || {}).textContent || (s.querySelector('.prenda') || {}).textContent,
    imgs: [...s.querySelectorAll('.fp-montaje img')].map(i => i.src.split('/').pop()), caps: [...s.querySelectorAll('.fp-montaje figcaption')].map(c => c.textContent),
    th: [...s.querySelectorAll('.fp-tallas thead th')].map(x => x.innerText.replace(/\s+/g, ' ').trim()), calces: [...s.querySelectorAll('table.tp:not(.dsp) tbody tr')].map(r => r.children[2].textContent),
    alerta: [...s.querySelectorAll('.alerta')].map(a => a.textContent).join(' ') })));

  await p.goto('https://panel-fichas-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(1200);

  // 1 · lo que traba a Planificación: un niño en «Jugadores», que no tiene molde infantil
  const q = await ctx.newPage(); const errP = []; q.on('pageerror', e => errP.push(e.message));
  await q.goto('https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'); await q.waitForTimeout(2500);
  const falt = await q.evaluate(o => { FICHAS_MAP['COT-3900'] = o.ficha; DETS_MAP['COT-3900'] = o.personas; return moldesFaltantes('COT-3900'); }, original);
  ok(falt.join() === '«Jugadores» (Camiseta) infantil, sin molde infantil: 1 persona', 'Planificación dice qué diseño, qué calce y cuántas personas: ' + falt.join(' | '));
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3900'); await p.waitForTimeout(1500);
  ok(/«Jugadores · Camiseta»: 1 persona infantil, sin molde infantil/.test(await texto('#aviso-sin-molde')), 'el panel avisa lo mismo en la ficha: ' + (await texto('#aviso-sin-molde')).replace(/\s+/g, ' ').slice(0, 160));

  // 2 · ficha de producción antes de corregir: una hoja por diseño y el montaje aparece igual
  await p.click('[data-ir="pdf"]'); await p.waitForTimeout(900);
  let hs = await hojas(), jug = hs.find(h => /Jugadores/.test(h.d));
  ok(hs.filter(h => /Jugadores/.test(h.d)).length === 1, 'una sola hoja para «Jugadores» (no se parte por calce): ' + hs.map(h => h.d).join(' · '));
  ok(jug && jug.imgs.join() === 'cam.jpg', 'la hoja muestra su montaje aunque haya una persona sin molde: ' + (jug ? jug.imgs.join() : ''));
  ok(jug && /1 persona en un calce sin molde en este diseño \(infantil\)/.test(jug.alerta) && jug.calces.some(c => /^Infantil \(sin molde\)$/.test(c)), 'la hoja marca a la persona sin molde: ' + (jug ? jug.calces.join(', ') : ''));

  // 3 · Prendas y moldes: agregar el molde infantil a «Jugadores» y unir «Jugadoras» como su calce femenino
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3900'); await p.waitForTimeout(1500);
  await p.click('[data-ir="editar"]'); await p.waitForTimeout(900);
  ok(/1 persona cargada como infantil y este diseño no tiene molde infantil/.test(await texto('[data-linea="0"]')), 'la línea de «Jugadores» avisa la persona sin molde');
  await p.click('[data-linea="0"] [data-agregar-calce][data-calce="Infantil"]'); await p.waitForTimeout(500);
  const cat = await texto('#cat-mol');
  ok(/Agregar calce a «Jugadores»/.test(cat) && /Ya tiene: masculino/.test(cat) && await p.$eval('#cat-mol [data-cf="calce"]', s => s.value) === 'Infantil', 'el catálogo se abre para agregar el calce infantil');
  ok(/Jugadoras/.test(await texto('#cat-mol .cat-unir')) && !(await p.$('#cat-mol [data-unir="short"]')), 'ofrece unir «Jugadoras» (otro calce de la misma prenda) y no el short');
  await p.click('[data-calce-molde="20"]'); await p.waitForTimeout(400);
  ok(/20 · FUTINHOMU02/.test(await texto('[data-linea="1"]')) && /Mismo diseño: Jugadores/.test(await texto('[data-linea="1"]')) && await p.inputValue('[data-linea="1"] [data-campo="cant"]') === '1',
    'la línea infantil queda en el mismo diseño, con 1 (la persona ya cargada)');
  ok(!/no tiene molde infantil/.test(await texto('[data-linea="0"]')), 'ya no avisa la persona sin molde');
  ok(await p.inputValue('[data-linea="0"] [data-campo="cant"]') === '2', 'el masculino baja de 3 a 2: el total del diseño no cambia');
  await p.click('[data-linea="0"] [data-agregar-calce]'); await p.waitForTimeout(400);
  await p.click('[data-unir="camiseta_2"]'); await p.waitForTimeout(400);
  const l2 = await texto('[data-linea="2"]');
  ok(/17 · FUTMUJU02/.test(l2) && /Se une a este diseño \(antes «Jugadoras»\)/.test(l2) && /2 cargadas por el cliente/.test(l2), '«Jugadoras» queda como el calce femenino de «Jugadores», con sus 2 personas');
  ok(!(await p.$('[data-linea="0"] [data-agregar-calce]')), 'con los tres calces ya no ofrece agregar otro');
  // separar y volver a unir
  await p.click('[data-separar="2"]'); await p.waitForTimeout(300);
  ok((await p.$$('[data-linea] [data-separar]')).length === 0 && /Jugadoras/.test(await p.inputValue('[data-linea="2"] [data-campo="disnom"]')), '«Separar» deja «Jugadoras» como antes');
  await p.click('[data-linea="0"] [data-agregar-calce]'); await p.waitForTimeout(300);
  await p.click('[data-unir="camiseta_2"]'); await p.waitForTimeout(300);
  await p.fill('[data-linea="0"] [data-campo="cant"]', '2');
  envios.length = 0;
  await p.click('#btn-guardar-items'); await p.waitForTimeout(1600);
  const iP = envios.findIndex(e => e.m === 'POST' && /fichas_detalle/.test(e.u)), iT = envios.findIndex(e => e.m === 'PATCH' && /fichas_tallas/.test(e.u) && e.d && e.d.specs);
  const pp = (envios[iP] || {}).d || [], tt = (envios[iT] || {}).d || {};
  ok(iP >= 0 && iP < iT, 'primero pasan las personas, después la ficha');
  ok(pp.length === 2 && pp.every(x => x.tallas.camiseta && !x.tallas.camiseta_2) && pp.find(x => x.id === 'p5').tallas.short === 'L' && pp.every(x => x.nombre && x.numero && x.calce === 'Femenino'),
    'las 2 personas de «Jugadoras» pasan a «Jugadores» con su talla, nombre, número y calce');
  ok(tt.items && tt.items.map(i => i.prenda + ':' + i.cant).join() === 'camiseta:5,short:3', 'un solo diseño de camiseta con 5: ' + (tt.items || []).map(i => i.prenda + ':' + i.cant).join());
  const sc = (tt.specs || {}).camiseta || {};
  ok(JSON.stringify(sc.moldes) === '{"Masculino":"FUTHOMU02|18","Infantil":"FUTINHOMU02|20","Femenino":"FUTMUJU02|17"}' && JSON.stringify(sc.unidades) === '{"Masculino":2,"Infantil":1,"Femenino":2}',
    'un molde por calce: ' + JSON.stringify(sc.moldes) + ' ' + JSON.stringify(sc.unidades));
  ok(!(tt.specs || {}).camiseta_2 && sc.nombre === 'Jugadores' && sc.tela === 'Pro' && sc.nota === 'Escudo bordado', 'la ficha técnica queda en «Jugadores» (y toma la nota que solo tenía «Jugadoras»)');
  const ti = (envios.find(e => e.m === 'PATCH' && e.d && e.d.imagenes) || {}).d || {};
  ok(ti.imagenes && ti.imagenes.length === 2 && ti.imagenes.every(i => i.prendas.join() === 'camiseta'), 'los dos montajes quedan en «Jugadores»');
  ok(!envios.some(e => e.m === 'DELETE' && /storage|fichas_detalle/.test(e.u)), 'no se borra ningún montaje ni ninguna persona');

  // 4 · ficha de producción: una sección con los tres calces, cada persona con el número de su molde
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3900'); await p.waitForTimeout(1500);
  ok(!(await p.$('#aviso-sin-molde')), 'la ficha ya no avisa personas sin molde');
  await p.click('[data-ir="pdf"]'); await p.waitForTimeout(900);
  hs = await hojas(); jug = hs.find(h => /Jugadores/.test(h.d));
  ok(hs.length === 2, 'dos hojas: «Jugadores» (con sus tres calces) y el short: ' + hs.map(h => h.d).join(' · '));
  ok(jug && jug.th.join('|') === 'Talla|Masculino Molde 18|Femenino Molde 17|Talla|Infantil Molde 20', 'resumen de tallas con el molde de cada calce: ' + (jug ? jug.th.join(' | ') : ''));
  ok(jug && jug.calces.join() === 'Masculino (molde 18),Masculino (molde 18),Femenino (molde 17),Femenino (molde 17),Infantil (molde 20)', 'detalle: el calce y el molde de cada persona: ' + (jug ? jug.calces.join(', ') : ''));
  ok(jug && jug.imgs.join() === 'cam.jpg,fem.jpg' && jug.caps.join() === 'Completo · Masculino,Completo · Femenino' && !jug.alerta, 'los dos montajes en la misma hoja, cada uno con su calce: ' + (jug ? jug.caps.join(', ') : ''));
  const falt2 = await q.evaluate(o => { FICHAS_MAP['COT-3900'] = o.f; DETS_MAP['COT-3900'] = o.d; return moldesFaltantes('COT-3900'); }, { f: fichas[0], d: personas });
  ok(!falt2.length, 'Planificación ya deja ingresar el pedido (sin moldes faltantes)');

  // 5 · copiar la configuración de telas a otros diseños
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3901'); await p.waitForTimeout(1500);
  await p.click('[data-ir="tecnica"]'); await p.waitForTimeout(900);
  await p.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = true; }));
  ok((await p.$$('[data-copia="camiseta"]')).length === 2 && !(await p.$('[data-copia="camiseta"][value="short"]')), 'ofrece copiar a las otras dos camisetas (no al short)');
  await p.check('[data-copia-todos="camiseta"]'); await p.click('[data-copiar-conf="camiseta"]'); await p.waitForTimeout(400);
  ok(/Copiado a 2 diseños/.test(await texto('[data-sec="c-camiseta"]')), 'confirma la copia');
  envios.length = 0;
  await p.click('#btn-guardar-tec'); await p.waitForTimeout(1200);
  const s2 = ((envios.find(e => e.m === 'PATCH' && e.d && e.d.specs) || {}).d || {}).specs || {};
  const b2 = s2.camiseta_2 || {}, c3 = s2.camiseta_3 || {};
  ok(b2.tela === 'Pro' && b2.aplicacion === 'Sublimado' && b2.nombre === 'B' && b2.nota === 'Solo B' && JSON.stringify(b2.moldes) === '{"Femenino":"FUTMUJU02|17"}', 'B: tela y aplicación copiadas; su nombre, nota y molde no cambian');
  ok(b2.despiece && b2.despiece.molde === '17 · FUTMUJU02' && b2.despiece.piezas.map(x => x.pieza + '=' + x.tela + '/' + x.detalle).join() === 'Delantero=Pro azul/Sublimada,Espalda=/,Manga=Pro blanco/Color de tela (sin sublimar)',
    'B: carga las piezas de su molde con la tela de las que se llaman igual: ' + (b2.despiece ? b2.despiece.piezas.map(x => x.pieza + '=' + x.tela).join(', ') : ''));
  ok(c3.despiece && c3.despiece.piezas.map(x => x.pieza + '=' + x.tela).join() === 'Delantero=Pro azul,Cuello=Rib' && c3.tela === 'Pro', 'C: conserva sus piezas y toma la tela de las que se llaman igual');
  ok(!(s2.short || {}).tela, 'el short no cambia');

  // 6 · al crear una ficha: un diseño con dos calces
  const creadas = [];
  await ctx.route(/supabase\.co\/rest\/v1\/fichas_tallas/, r => { if (r.request().method() === 'POST') { creadas.push(JSON.parse(r.request().postData())); return r.fulfill({ contentType: 'application/json', body: '[]' }); } return r.fallback(); });
  await p.goto('https://panel-fichas-playmaker.netlify.app/'); await p.waitForTimeout(1200);
  await p.click('[data-ir="crear"]'); await p.waitForTimeout(700);
  await p.fill('#c-ref', 'COT-9100'); await p.fill('#c-proy', 'Mixto'); await p.fill('#c-cliente', 'Club Tres');
  await p.click('#btn-catalogo'); await p.waitForTimeout(300);
  await p.click('[data-add-molde="18"]'); await p.waitForTimeout(300);
  await p.click('[data-linea="0"] [data-agregar-calce]'); await p.waitForTimeout(300);
  await p.selectOption('#cat-mol [data-cf="calce"]', 'Femenino'); await p.waitForTimeout(300);
  await p.click('[data-calce-molde="17"]'); await p.waitForTimeout(300);
  await p.fill('[data-linea="0"] [data-campo="cant"]', '10'); await p.fill('[data-linea="1"] [data-campo="cant"]', '8');
  await p.click('#btn-crear'); await p.waitForTimeout(1200);
  const cr = creadas[0] || {};
  ok(cr.items && cr.items.map(i => i.prenda + ':' + i.cant).join() === 'camiseta:18' && JSON.stringify(cr.specs.camiseta.moldes) === '{"Masculino":"FUTHOMU02|18","Femenino":"FUTMUJU02|17"}',
    'al crear: un diseño con molde masculino y femenino (' + JSON.stringify(cr.items) + ')');

  ok(!errores.length, 'panel sin errores JS ' + errores.join(' | '));
  ok(!errP.length, 'Planificación sin errores JS ' + errP.join(' | '));
  await b.close();
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
