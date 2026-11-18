// Despiece de los moldes: acceso directo desde el inicio del panel de Fichas y desde Planificación › Moldes
// (resumen del despiece de cada molde y botón que abre el panel en el despiece de ese molde). Bases simuladas.
const { chromium, contexto } = require('./comun_movil');
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const moldes = require('./datos_moldes_catalogo.json').map(m => Object.assign({}, m));
moldes.find(m => m.numero === 2).piezas = [{ pieza: 'Delantero', cant: 1, tela: '', consumo: 0.5 }, { pieza: 'Espalda', cant: 1, tela: '', consumo: 0.5 }, { pieza: 'Manga', cant: 2, tela: '', consumo: 0.2 }];
moldes.find(m => m.numero === 21).piezas = [{ pieza: 'Delantero', cant: 1, tela: '' }, { pieza: 'Espalda', cant: 1, tela: '' }];
const datos = { tablas: { moldes, catalogo_tecnico: [], fichas_tallas: [], fichas_detalle: [], fichas_avisos: [], pedidos: [] } };
const PLAN = 'https://planificacion-playmaker.netlify.app/', PANEL = 'https://panel-fichas-playmaker.netlify.app/';

(async () => {
  const b = await chromium.launch(); const errores = [];
  const ctx = await contexto(b, datos, { viewport: { width: 1280, height: 900 }, isMobile: false, hasTouch: false, deviceScaleFactor: 1, userAgent: undefined });
  const guardados = [];
  await ctx.route(/jvgifibnoigpicwklasw\.supabase\.co\/rest\/v1\/moldes/, r => {
    const q = r.request(); if (q.method() === 'GET') return r.fallback();
    const d = JSON.parse(q.postData()); guardados.push(d);
    const i = moldes.findIndex(m => m.numero === d.numero); if (i >= 0) Object.assign(moldes[i], d);
    return r.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify([d]) });
  });
  const p = await ctx.newPage(); p.on('pageerror', e => errores.push(e.message)); p.on('dialog', d => d.accept());

  // 1 · inicio del panel: botón directo al catálogo de moldes y despiece
  await p.goto(PANEL + '#pmk_acceso=tok1'); await p.waitForTimeout(2500);
  ok(await p.isVisible('#pmk [data-ir="moldes"]'), 'panel: el inicio tiene «Catálogo de moldes y despiece»');
  await p.click('#pmk [data-ir="moldes"]'); await p.waitForTimeout(1200);
  ok(/Catálogo de\s*moldes/i.test(await p.innerText('#pmk')) && (await p.$$('.molde-card')).length === 104, 'abre el catálogo con los 104 moldes');
  ok(await p.isVisible('#pmk button.btn.plano[data-ir="lista"]') && /Volver a las fichas/i.test(await p.innerText('#pmk')), 'desde el inicio, el botón de abajo vuelve a las fichas');
  await p.click('#pmk button.btn.plano[data-ir="lista"]'); await p.waitForTimeout(900);
  ok(/Fichas de talla/i.test(await p.innerText('#pmk')), 'y vuelve al inicio del panel');

  // 2 · Planificación › Moldes: despiece de cada molde y botón al despiece
  await p.goto(PLAN + '#pmk_acceso=tok1'); await p.waitForTimeout(2500);
  await p.evaluate(() => irTab('moldes')); await p.waitForTimeout(500);
  const filaDe = n => p.$$eval('#view-moldes tr', (t, n) => { const r = t.find(x => (x.querySelector('td b') || {}).textContent === n); return r ? r.innerText.replace(/\s+/g, ' ') : ''; }, n);
  const f02 = await filaDe('02'), f21 = await filaDe('21'), f03 = await filaDe('03');
  ok(/3 piezas: Delantero, Espalda, Manga ×2 · 1,2 m por prenda/.test(f02) && /Editar despiece/.test(f02), 'molde 02: «3 piezas: Delantero, Espalda, Manga ×2 · 1,2 m por prenda» y «Editar despiece» · ' + f02);
  ok(/2 piezas: Delantero, Espalda · sin consumo de tela/.test(f21), 'molde 21: avisa que no tiene consumo de tela · ' + f21);
  ok(/Sin despiece/.test(f03) && /Definir despiece/.test(f03) && /Ver guía/.test(f03), 'molde sin piezas: «Sin despiece» y «Definir despiece», junto a «Ver guía» · ' + f03);
  ok(/102 moldes aún sin despiece/.test(await p.innerText('#view-moldes')), 'dice cuántos moldes faltan (102 de 104)');
  const href = await p.$$eval('#view-moldes tr', t => { const r = t.find(x => (x.querySelector('td b') || {}).textContent === '02'); return r.querySelector('a.btn').href; });
  const u = new URL(href);
  ok(u.origin + u.pathname === PANEL && u.searchParams.get('molde') === '2' && /#tab=moldes$/.test(u.searchParams.get('volver')), 'el botón abre el panel en el molde 2 y vuelve a Moldes · ' + href.slice(0, 90));
  ok(new URL(await p.getAttribute('#view-moldes .toolbar a.btn', 'href')).searchParams.get('molde') === 'todos', 'arriba, «Catálogo de moldes y despiece» abre el catálogo completo');
  await p.screenshot({ path: 'movil/moldes_despiece_plan.png', clip: { x: 0, y: 0, width: 1280, height: 900 } });

  // 3 · desde Planificación se llega al despiece del molde, se edita, se guarda y se vuelve
  await p.click('#view-moldes tr:has(td b:text-is("02")) a.btn'); await p.waitForTimeout(2000);
  ok(p.url().startsWith(PANEL) && /Molde N° 02/i.test(await p.innerText('#pmk')), 'el panel abre directo el despiece del molde 02');
  const piezas = await p.$$eval('[data-mp][data-k="pieza"]', i => i.map(x => x.value).join());
  ok(piezas === 'Delantero,Espalda,Manga', 'con sus piezas: ' + piezas);
  await p.fill('[data-mp="2"][data-k="consumo"]', '0.25');
  await p.click('#me-add'); await p.waitForTimeout(200);
  await p.fill('[data-mp="3"][data-k="pieza"]', 'Cuello'); await p.fill('[data-mp="3"][data-k="consumo"]', '0.05');
  await p.click('#me-guardar'); await p.waitForTimeout(800);
  const g = guardados[guardados.length - 1] || {};
  ok(g.numero === 2 && JSON.stringify(g.piezas) === JSON.stringify([{ pieza: 'Delantero', cant: 1, tela: '', consumo: 0.5 }, { pieza: 'Espalda', cant: 1, tela: '', consumo: 0.5 }, { pieza: 'Manga', cant: 2, tela: '', consumo: 0.25 }, { pieza: 'Cuello', cant: 1, tela: '', consumo: 0.05 }]),
    'guarda el despiece del molde 2 en el catálogo · ' + JSON.stringify(g.piezas));
  ok(/Molde N° 02 · FUTHOMU01 guardado \(4 piezas\)/i.test(await p.innerText('#pmk')), 'confirma «Molde N° 02 · FUTHOMU01 guardado (4 piezas)»');
  const aPlan = await p.getAttribute('#pmk a.btn:has-text("Volver a Planificación")', 'href').catch(() => '');
  ok(/planificacion-playmaker\.netlify\.app\/.*#tab=moldes$/.test(aPlan), 'ofrece «Volver a Planificación» (a Moldes) · ' + aPlan);
  await p.screenshot({ path: 'movil/moldes_despiece_panel.png', fullPage: false });
  ok(await p.evaluate(() => window.scrollY) === 0, 'tras guardar, la pantalla sube a la confirmación');
  await p.goto(aPlan + '&pmk_acceso=tok1'); await p.waitForTimeout(2500);
  ok(await p.evaluate(() => TAB) === 'moldes' && /4 piezas: Delantero, Espalda, Manga ×2, Cuello · 1,3 m por prenda/.test(await filaDe('02')), 'de vuelta en Moldes, el 02 muestra el despiece nuevo · ' + await filaDe('02'));

  // 4 · un perfil de área (sin editar proyectos) ve el despiece, pero no los botones
  const ctx2 = await contexto(b, datos, { viewport: { width: 390, height: 844 } });
  await ctx2.route(/ygcsqrylpibhofvetdyh\.supabase\.co\/rest\/v1\/rpc\/plan_sesion/, r => r.fulfill({ contentType: 'application/json', body: JSON.stringify({ usuario: 'u.corte', nombre: 'Pedro Corte', rol: 'CORTE', roles: ['CORTE'] }) }));
  const p2 = await ctx2.newPage(); p2.on('pageerror', e => errores.push('corte: ' + e.message));
  await p2.goto(PLAN + '#pmk_acceso=tok1'); await p2.waitForTimeout(2500);
  await p2.evaluate(() => irTab('moldes')); await p2.waitForTimeout(500);
  const t2 = await p2.innerText('#view-moldes');
  ok(/piezas/.test(t2) && !/Definir despiece|Editar despiece|Catálogo de moldes y despiece/.test(t2), 'Corte ve el despiece pero no los botones para cambiarlo');
  const anchos = await p2.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
  ok(anchos[0] <= anchos[1], 'celular: la página no se sale del ancho (' + anchos.join('/') + ')');

  ok(errores.length === 0, 'sin errores de JavaScript ' + errores.join(' | '));
  await b.close(); console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
