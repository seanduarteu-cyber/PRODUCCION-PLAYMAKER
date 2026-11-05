// Panel de fichas y Planificación: medias por diseño (nombre, montaje, pares por talla y hoja propia),
// sin arquero ni número obligatorio. Bases simuladas.
const { chromium, contexto } = require('./comun_movil');
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const hoy = new Date().toISOString().slice(0, 10), ahora = new Date().toISOString();
const moldes = require('./datos_moldes_catalogo.json');
// ficha ya creada: camiseta de jugador (10) y de arquero (1, otro diseño con el mismo molde), medias azules (10) y blancas (1)
const ficha = { id: 1, ref: 'COT-3610', proyecto: 'Uniformes 2026', cliente: 'Club Prueba', vendedor: 'Sean Duarte', entrega: hoy, entrega_interna: hoy, entrega_cliente: hoy,
  estado: 'abierto', created_at: ahora,
  items: [{ prenda: 'camiseta', cant: 10 }, { prenda: 'camiseta_2', cant: 1 }, { prenda: 'medias', cant: 10 }, { prenda: 'medias_2', cant: 1 }],
  specs: { camiseta: { nombre: 'Jugadores', moldes: { Masculino: 'FUTHOMU02|18' }, unidades: { Masculino: 10 } },
    camiseta_2: { nombre: 'Arquero', moldes: { Masculino: 'FUTHOMU02|18' }, unidades: { Masculino: 1 } },
    medias: { nombre: 'Medias azules', cantidades: { S: 4, M: 6 }, origen: 'PMK' }, medias_2: { nombre: 'Medias blancas', cantidades: { Infantil: 1 } } },
  imagenes: [{ url: 'https://x.test/cam.jpg', prendas: ['camiseta'], prenda: 'camiseta', vista: 'Completo', path: 'a/1.jpg' },
    { url: 'https://x.test/arq.jpg', prendas: ['camiseta_2'], prenda: 'camiseta_2', vista: 'Completo', path: 'a/2.jpg' },
    { url: 'https://x.test/azul.jpg', prendas: ['medias'], prenda: 'medias', vista: 'Completo', path: 'a/3.jpg' },
    { url: 'https://x.test/blanca.jpg', prendas: ['medias_2'], prenda: 'medias_2', vista: 'Completo', path: 'a/4.jpg' }] };
const personas = Array.from({ length: 11 }, (_, i) => ({ id: 'p' + i, ref: 'COT-3610', nombre: i < 2 ? '' : 'Jugador ' + i, estampado: i < 2 ? '' : 'JUG' + i, numero: i < 2 ? '' : String(i),
  calce: 'Masculino', manga: 'Corta', arquero: false, obs: '', tallas: i === 10 ? { camiseta_2: 'L' } : { camiseta: ['S', 'M', 'L'][i % 3] }, disenos: {}, created_at: ahora }));
const datos = { tablas: { fichas_tallas: [ficha], fichas_detalle: personas, fichas_avisos: [], moldes, catalogo_tecnico: [], pedidos: [] } };

(async () => {
  const b = await chromium.launch();
  const ctx = await contexto(b, datos, { viewport: { width: 1280, height: 900 }, isMobile: false, hasTouch: false, userAgent: undefined });
  const creadas = [];
  await ctx.route(/supabase\.co\/rest\/v1\/fichas_tallas/, r => { if (r.request().method() === 'POST') { creadas.push(JSON.parse(r.request().postData())); return r.fulfill({ contentType: 'application/json', body: '[]' }); } return r.fallback(); });
  const p = await ctx.newPage(); const errores = []; p.on('pageerror', e => errores.push(e.message)); p.on('dialog', d => d.accept());
  const texto = () => p.innerText('#app').catch(() => p.innerText('body'));

  // 1 · crear ficha: un molde y dos líneas de medias, cada una con su nombre y pares por talla
  await p.goto('https://panel-fichas-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(1500);
  await p.click('[data-ir="crear"]'); await p.waitForTimeout(700);
  await p.fill('#c-ref', 'COT-9001'); await p.fill('#c-proy', 'Uniforme prueba'); await p.fill('#c-cliente', 'Club Nuevo');
  ok(/El arquero o líbero es otro diseño/.test(await texto()), 'la ayuda explica que el arquero es otro diseño del mismo molde');
  await p.click('#btn-catalogo'); await p.waitForTimeout(400);
  await p.click('[data-add-molde="18"]'); await p.waitForTimeout(400);
  await p.click('[data-add-molde="18"]'); await p.waitForTimeout(400);
  await p.click('#btn-sinmolde'); await p.waitForTimeout(300);
  await p.click('#btn-sinmolde'); await p.waitForTimeout(300);
  const lineas = await p.$$('[data-linea]');
  ok(lineas.length === 4, 'cuatro líneas: el molde dos veces (jugador y arquero) y dos de medias');
  ok((await p.$$('[data-linea] [data-med="Adulto"]')).length === 2 && (await p.$$('[data-linea] [data-mj-linea]')).length === 4, 'cada línea de medias tiene pares por talla (S, M, L, Adulto, Infantil) y botón de montaje');
  await p.fill('[data-linea="0"] [data-campo="cant"]', '10'); await p.fill('[data-linea="1"] [data-campo="cant"]', '1');
  await p.fill('[data-linea="2"] [data-campo="disnom"]', 'Medias azules');
  await p.fill('[data-linea="2"] [data-med="S"]', '4'); await p.fill('[data-linea="2"] [data-med="M"]', '6');
  await p.fill('[data-linea="3"] [data-campo="disnom"]', 'Medias blancas');
  await p.fill('[data-linea="3"] [data-med="Infantil"]', '1');
  ok(await p.inputValue('[data-linea="2"] [data-campo="cant"]') === '10', 'la cantidad de las medias es la suma de sus tallas (10)');
  await p.click('#btn-crear'); await p.waitForTimeout(1200);
  const c = creadas[0] || {};
  ok(c.items && c.items.map(i => i.prenda + ':' + i.cant).join() === 'camiseta:10,camiseta_2:1,medias:10,medias_2:1', 'items: ' + (c.items || []).map(i => i.prenda + ':' + i.cant).join());
  ok(c.specs && JSON.stringify(c.specs.medias) === '{"nombre":"Medias azules","cantidades":{"S":4,"M":6}}' && JSON.stringify(c.specs.medias_2) === '{"nombre":"Medias blancas","cantidades":{"Infantil":1}}',
    'cada línea de medias queda con su nombre y sus pares por talla');

  // 2 · ficha de producción: una hoja por cada diseño de medias, con su montaje y sus pares por talla
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3610'); await p.waitForTimeout(1500);
  ok(!/Arqueros y líberos/.test(await texto()), 'la ficha ya no pide marcar arqueros o líberos');
  await p.click('[data-ir="pdf"]'); await p.waitForTimeout(1000);
  const hojas = await p.$$eval('section.fp:not(.portada)', ss => ss.map(s => ({ t: s.querySelector('.prenda').textContent, d: (s.querySelector('.diseno-hoja') || {}).textContent || '',
    img: (s.querySelector('.fp-montaje img') || {}).src || '', tabla: (s.querySelector('.fp-tallas') || {}).innerText || '' })));
  const az = hojas.find(h => /azules/.test(h.d)), bl = hojas.find(h => /blancas/.test(h.d));
  ok(hojas.length === 4, 'cuatro hojas: jugadores, arquero, medias azules y medias blancas (' + hojas.map(h => h.d || h.t).join(' · ') + ')');
  ok(az && /azul\.jpg/.test(az.img) && /S\s+4/.test(az.tabla) && /M\s+6/.test(az.tabla) && /10 pares/.test(az.tabla), 'hoja de medias azules: su montaje y S 4 · M 6 = 10 pares');
  ok(bl && /blanca\.jpg/.test(bl.img) && /Infantil\s+1/.test(bl.tabla), 'hoja de medias blancas: su montaje e Infantil 1');
  const arqH = hojas.find(h => /Arquero/.test(h.d));
  ok(arqH && /arq\.jpg/.test(arqH.img), 'el arquero sale en su propia hoja con su montaje (es otro diseño)');
  const portada = await p.innerText('section.portada');
  ok(!/Arqueros o líberos/.test(portada) && /10 pares/.test(portada), 'portada: sin fila de arqueros; las medias en pares');

  // 3 · listado: sin columna de arquero ni medias por persona; se agrega una persona solo con talla
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3610'); await p.waitForTimeout(1500);
  await p.click('[data-pest="listado"]'); await p.waitForTimeout(500);
  const ths = await p.$$eval('.tabla-scroll th', ts => ts.map(t => t.textContent));
  ok(!ths.some(t => /^(Arquero o líbero|Arquero|Líbero)$/.test(t.trim()) || /^Medias/.test(t.trim())), 'listado sin columna «arquero» ni de medias (el diseño «Arquero» es su propia columna de talla): ' + ths.join(' | '));
  await p.click('#ep-nueva'); await p.waitForTimeout(400);
  ok(!(await p.$('#ep-arq')), 'agregar persona: sin casilla de arquero');
  await p.selectOption('#ep-calce', 'Masculino'); await p.selectOption('[data-ep-talla="camiseta"]', 'M');
  await p.click('#ep-guardar'); await p.waitForTimeout(800);
  ok(!(await p.$('#form-persona .aviso.error')), 'se guarda sin nombre ni número');
  // editar todo el listado: sin columna de arquero
  await p.click('[data-ir="listado-ed"]'); await p.waitForTimeout(600);
  ok(!(await p.$('[data-k="arquero"]')), 'editar todo el listado: sin columna de arquero');

  // 4 · ficha técnica: medias con sus pares por talla; al cambiar un montaje no se pregunta «¿es de arquero?»
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3610'); await p.waitForTimeout(1500);
  await p.click('[data-ir="tecnica"]'); await p.waitForTimeout(900);
  await p.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = true; }));
  ok(/S: 4 · M: 6 \(10 pares\)/.test(await texto()), 'ficha técnica: las medias azules muestran sus pares por talla');
  await p.click('[data-editar-img]'); await p.waitForTimeout(400);
  ok(!/¿Es de arquero/.test(await texto()), 'al cambiar un montaje no pregunta si es de arquero');
  ok(!errores.length, 'panel sin errores JS ' + errores.join(' | '));

  // 5 · Planificación: lee las medias por pares por talla
  const q = await ctx.newPage(); const errP = []; q.on('pageerror', e => errP.push(e.message));
  await q.goto('https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'); await q.waitForTimeout(2500);
  const r = await q.evaluate(f => { FICHAS_MAP['COT-3610'] = f; DETS_MAP['COT-3610'] = [];
    return { tr: traducirFicha('COT-3610').desglose, it: desgloseDesdeItems('COT-3610').desglose,
      mo: armarMoldes('COT-3610').filter(g => /MEDIAS/.test(g.codigo)).map(g => g.prenda + '|' + g.codigo + '|' + g.cant + '|' + JSON.stringify(g.tallas)) }; }, ficha);
  ok(r.tr['MEDIAS-ADL'] === true && r.tr['MEDIAS-INF'] === true, 'al ingresar a producción: medias adulto e infantil en el desglose');
  ok(r.mo.join(' / ') === 'Medias · Medias azules|MEDIAS-ADL|10|{"S":4,"M":6} / Medias 2 · Medias blancas|MEDIAS-INF|1|{"Infantil":1}', 'plantilla de moldes con los pares por talla: ' + r.mo.join(' / '));
  await q.evaluate(() => { PROY = PROY || []; });
  ok(!errP.length, 'Planificación sin errores JS ' + errP.join(' | '));
  await b.close();
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
