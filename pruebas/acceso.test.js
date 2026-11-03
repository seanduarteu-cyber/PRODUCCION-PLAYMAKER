// Prueba del acceso único: los tres sitios con sus direcciones reales (route) y la base de Producción simulada
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const BASE = path.resolve(__dirname, '../sistemas');
const SITIOS = { 'https://planificacion-playmaker.netlify.app/': 'produccion', 'https://panel-fichas-playmaker.netlify.app/': 'panel-fichas', 'https://ventas-playmaker.netlify.app/': 'ventas' };
const PLAN = 'https://planificacion-playmaker.netlify.app/', FICHAS = 'https://panel-fichas-playmaker.netlify.app/', VENTAS = 'https://ventas-playmaker.netlify.app/';
const PORTAL = PLAN + 'sistemas.html';
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.webmanifest': 'application/manifest+json' };
let fallas = 0;
const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
// base de Producción simulada
const USUARIOS = {
  'sean.duarte': { nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'], clave: 'sean1' },
  'javiera.dorival': { nombre: "Javiera D'Orival", rol: 'ventas', roles: ['ventas'], clave: 'jav1' },
  'pedro.corte': { nombre: 'Pedro Corte', rol: 'CORTE', roles: ['CORTE'], clave: 'ped1' },
  'taller.uno': { nombre: 'Taller Uno', rol: 'taller', roles: ['taller'], ejecutante_id: 5, clave: 'tal1' },
  'ana.nueva': { nombre: 'Ana Nueva', rol: 'fichas', roles: ['fichas'], clave: '1234', debe_cambiar: true },
};
const SES = {}; let nTok = 0; const LLAMADAS = [];
const pub = u => { const x = USUARIOS[u]; return { usuario: u, nombre: x.nombre, rol: x.rol, roles: x.roles, ejecutante_id: x.ejecutante_id || null }; };
function prod(fn, body) {
  LLAMADAS.push(fn);
  if (fn === 'plan_login') { const x = USUARIOS[body.p_usuario]; if (!x || x.clave !== body.p_clave) return null; const t = 'tok' + (++nTok); SES[t] = body.p_usuario; return { ...pub(body.p_usuario), token: t, debe_cambiar: !!x.debe_cambiar }; }
  if (fn === 'plan_sesion') return SES[body.p_token] ? pub(SES[body.p_token]) : null;
  if (fn === 'plan_logout') { delete SES[body.p_token]; return null; }
  if (fn === 'plan_cambiar_clave') { const u = SES[body.p_token]; if (u) { USUARIOS[u].clave = body.p_nueva; USUARIOS[u].debe_cambiar = false; } return null; }
  return [];
}
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 800 }, serviceWorkers: 'block' });
  await ctx.route('**/*', async r => {
    const req = r.request(), u = new URL(req.url());
    const raiz = Object.keys(SITIOS).find(k => req.url().startsWith(k));
    if (raiz) {
      const f = path.join(BASE, SITIOS[raiz], decodeURIComponent(u.pathname).replace(/^\//, '') || 'index.html');
      if (fs.existsSync(f) && fs.statSync(f).isFile()) return r.fulfill({ status: 200, body: fs.readFileSync(f), contentType: TIPOS[path.extname(f)] || 'application/octet-stream' });
      return r.fulfill({ status: 404, body: 'no' });
    }
    if (u.host === 'ygcsqrylpibhofvetdyh.supabase.co') {
      const m = u.pathname.match(/\/rpc\/(\w+)/);
      if (m) return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(prod(m[1], JSON.parse(req.postData() || '{}'))) });
      if (u.pathname.endsWith('/plan_usuarios')) return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(Object.keys(USUARIOS).map(k => ({ ...pub(k), activo: true }))) });
      return r.fulfill({ status: 200, contentType: 'application/json', body: '[]' });
    }
    if (/supabase\.co/.test(u.host)) return r.fulfill({ status: 200, contentType: 'application/json', body: '[]' });
    if (/cdnjs|fonts\.(googleapis|gstatic)/.test(u.host)) return r.fulfill({ status: 200, body: '' });
    return r.abort();
  });
  const errores = [];
  const pagina = async () => { const p = await ctx.newPage(); p.on('pageerror', e => errores.push(p.url().slice(0, 50) + ': ' + e.message)); p.on('dialog', d => d.accept()); return p; };
  const espera = (p, ms = 900) => p.waitForTimeout(ms);
  const barra = p => p.evaluate(() => { const d = document.querySelector('.pmk-sis'); if (!d || getComputedStyle(d).display === 'none') return 'oculta';
    return [...d.querySelectorAll('a[data-sis]')].filter(a => getComputedStyle(a).display !== 'none').map(a => a.dataset.sis).join(','); });
  const ingresar = async (p, usuario, clave) => { await p.waitForSelector('#i-usuario option[value="' + usuario + '"]', { state: 'attached' }); await p.selectOption('#i-usuario', usuario); await p.fill('#i-clave', clave); await p.click('#btn-entrar'); };

  // A. Ventas sin sesión → página principal → ingreso de una vendedora → vuelve a Ventas ya dentro
  let p = await pagina();
  await p.goto(VENTAS); await p.waitForURL(/sistemas\.html/); await espera(p, 400);
  ok(p.url().startsWith(PORTAL + '?volver=' + encodeURIComponent(VENTAS)), 'A. Ventas sin sesión va a ingresar a la página principal');
  ok(/Ventas/.test(await p.textContent('#bajada')) && await p.isVisible('#antiguo'), 'A. la página dice que es para entrar a Ventas y ofrece la clave anterior');
  await p.screenshot({ path: 'acc_ingreso.png' });
  await ingresar(p, 'javiera.dorival', 'malaclave'); await espera(p, 300);
  ok((await p.textContent('#msg')).includes('incorrecta'), 'A. clave incorrecta avisa');
  await ingresar(p, 'javiera.dorival', 'jav1'); await p.waitForURL(VENTAS + '**'); await espera(p, 1200);
  ok(p.url() === VENTAS, 'A. vuelve a Ventas y limpia la dirección (' + p.url() + ')');
  ok(!(await p.isVisible('#login-screen')), 'A. Ventas: ya dentro, sin pedir clave');
  ok((await p.textContent('#header-user')).includes('Javiera'), 'A. Ventas reconoce a Javiera');
  ok(await p.evaluate(() => sessionStorage.getItem('pmk_rol')) === 'vendedor', 'A. Ventas: rol vendedor');
  ok(await p.evaluate(() => sessionStorage.getItem('pmk_user')) === "Javiera D'Orival", 'A. Ventas: el nombre calza con el vendedor');
  ok(await barra(p) === 'planificacion,fichas,ventas', 'A. barra con los tres sistemas (' + await barra(p) + ')');
  await p.screenshot({ path: 'acc_ventas_dentro.png' });

  // B. Ventas → Fichas → Planificación sin volver a ingresar
  await p.click('.pmk-sis [data-sis="fichas"]'); await p.waitForURL(FICHAS + '**'); await espera(p, 1200);
  ok(p.url() === FICHAS, 'B. Ventas → Fichas (dirección limpia: ' + p.url() + ')');
  ok(await p.evaluate(() => !!document.querySelector('[data-ir]') && !document.getElementById('btn-pin')), 'B. Fichas: dentro sin pedir clave');
  ok(await p.evaluate(() => !document.querySelector('[data-ir="usuarios"]')), 'B. Fichas: sin «Usuarios del panel» (los usuarios se administran en Planificación)');
  await p.screenshot({ path: 'acc_fichas_dentro.png' });
  await p.click('.pmk-sis [data-sis="planificacion"]'); await p.waitForURL(PLAN + '**'); await espera(p, 1500);
  ok(!(await p.evaluate(() => document.getElementById('login').classList.contains('on'))), 'B. Fichas → Planificación: dentro sin pedir clave');
  ok((await p.textContent('#userbox')).includes('Javiera'), 'B. Planificación reconoce a Javiera');
  ok(!/pmk_acceso/.test(p.url()), 'B. Planificación limpia la dirección');
  await p.click('.pmk-sis [data-sis="ventas"]'); await p.waitForURL(VENTAS + '**'); await espera(p, 1200);
  ok(!(await p.isVisible('#login-screen')), 'B. Planificación → Ventas: dentro');
  // Planificación → Fichas con ?volver= y vuelta a la misma sección
  await p.goto(PLAN + '#tab=calendario'); await espera(p, 1500);
  await p.click('.pmk-sis [data-sis="fichas"]'); await p.waitForURL(FICHAS + '**'); await espera(p, 1200);
  ok(/\?volver=/.test(p.url()) && !/pmk_acceso/.test(p.url()), 'B. Planificación → Fichas lleva ?volver= y limpia la sesión de la dirección');
  await p.click('.pmk-sis [data-sis="planificacion"]'); await p.waitForURL(PLAN + '**'); await espera(p, 1500);
  ok(await p.evaluate(() => typeof TAB !== 'undefined' && TAB) === 'calendario', 'B. Fichas → Planificación vuelve a la misma sección (' + await p.evaluate(() => typeof TAB !== 'undefined' && TAB) + ')');
  // Fichas en pestaña nueva (sin sesión propia) con ?ref=: pasa por la página principal y vuelve con la ficha
  await ctx.clearCookies(); await p.evaluate(() => {});
  const pf = await pagina();
  await pf.evaluate(() => 0).catch(() => {});
  await pf.goto(FICHAS); await espera(pf, 300);
  await pf.evaluate(() => localStorage.removeItem('pmk_fichas_sesion'));
  await pf.goto(FICHAS + '?ref=COT-9999'); await pf.waitForURL(FICHAS + '**'); await espera(pf, 1500);
  ok(pf.url() === FICHAS + '?ref=COT-9999', 'B. Fichas sin sesión propia: toma la sesión en la página principal y vuelve a ?ref= (' + pf.url() + ')');
  ok(await pf.evaluate(() => !document.getElementById('btn-pin')), 'B. … ya dentro');
  await pf.close();

  // I. ?pdf= no pide ingreso
  const pp = await pagina(); await pp.goto(FICHAS + '?pdf=COT-1'); await espera(pp, 800);
  ok(pp.url() === FICHAS + '?pdf=COT-1', 'I. ficha sola (?pdf=) no va a ingresar'); await pp.close();

  // F. Salir en Ventas cierra la sesión en todos los sistemas
  await p.goto(VENTAS); await espera(p, 1200);
  await p.click('header button[onclick="cerrarSesion()"]'); await p.waitForURL(/sistemas\.html/); await espera(p, 800);
  ok(LLAMADAS.includes('plan_logout') && Object.keys(SES).length === 0, 'F. Salir en Ventas cierra la sesión Playmaker');
  ok(await p.isVisible('#ingreso'), 'F. … y la página principal pide ingresar');
  await p.goto(PLAN); await espera(p, 1500);
  ok(await p.evaluate(() => document.getElementById('login').classList.contains('on')), 'F. Planificación también pide ingresar');

  // C. Perfil de área (Corte): Planificación y Fichas, no Ventas
  await p.goto(PORTAL); await ingresar(p, 'pedro.corte', 'ped1'); await espera(p, 600);
  const cards = await p.$$eval('.sis', e => e.map(x => x.dataset.sis + (x.classList.contains('no') ? ':no' : ':si')).join());
  ok(cards === 'planificacion:si,fichas:si,ventas:no', 'C. Corte: accesos ' + cards);
  await p.screenshot({ path: 'acc_portal_corte.png' });
  const pv = await pagina(); await pv.goto(VENTAS); await pv.waitForURL(/sistemas\.html/); await espera(pv, 800);
  ok((await pv.textContent('#aviso')).includes('no tiene acceso a Ventas'), 'C. Corte en Ventas: «Tu perfil no tiene acceso a Ventas»');
  await pv.close();
  await p.goto(PLAN); await espera(p, 1500);
  ok(await barra(p) === 'planificacion,fichas', 'C. barra de Corte: ' + await barra(p));
  // con la sesión de Corte, un enlace con su sesión directo a Ventas tampoco entra
  const tokCorte = await p.evaluate(() => USER.token);
  const pv2 = await pagina(); await pv2.goto(VENTAS + '#pmk_acceso=' + tokCorte); await espera(pv2, 1200);
  ok(pv2.url() === VENTAS && await pv2.isVisible('#login-screen') && (await pv2.textContent('#login-error')).includes('no tiene acceso'), 'C. sesión de Corte llevada a Ventas: no entra y lo explica');
  await pv2.close();
  await p.evaluate(() => salir()); await espera(p, 400);

  // D. Taller: solo Planificación (sin barra); en la página principal entra directo
  await p.goto(PORTAL); await ingresar(p, 'taller.uno', 'tal1'); await p.waitForURL(PLAN + '**'); await espera(p, 1500);
  ok(p.url() === PLAN, 'D. Taller: la página principal lo lleva directo a Planificación (' + p.url() + ')');
  ok(await barra(p) === 'oculta', 'D. Taller: sin barra (solo tiene Planificación)');
  const pf2 = await pagina(); await pf2.goto(FICHAS); await pf2.waitForURL(/sistemas\.html/); await espera(pf2, 800);
  ok((await pf2.textContent('#aviso')).includes('no tiene acceso a Fichas'), 'D. Taller en Fichas: sin acceso');
  await pf2.close();
  await p.evaluate(() => salir()); await espera(p, 400);

  // E. Gerencia (Sean, administrador): Ventas como gerencia
  await p.goto(PORTAL); await ingresar(p, 'sean.duarte', 'sean1'); await espera(p, 600);
  await p.click('a.sis[data-sis="ventas"]'); await p.waitForURL(VENTAS + '**'); await espera(p, 1200);
  ok(await p.evaluate(() => sessionStorage.getItem('pmk_rol')) === 'gerencia', 'E. Sean entra a Ventas como gerencia');
  ok(await p.evaluate(() => [...document.querySelectorAll('nav button')].some(b => b.textContent.trim() === 'Gastos' && getComputedStyle(b).display !== 'none')), 'E. Gerencia ve Gastos');
  // recargar Ventas mantiene la sesión
  await p.reload(); await espera(p, 1200);
  ok(!(await p.isVisible('#login-screen')) && p.url() === VENTAS, 'E. recargar Ventas mantiene la sesión');
  // Ventas en pestaña nueva: toma la sesión en la página principal sin pedir clave
  const pn = await pagina(); await pn.goto(VENTAS); await pn.waitForURL(VENTAS + '**'); await espera(pn, 1500);
  ok(pn.url() === VENTAS && !(await pn.isVisible('#login-screen')), 'E. Ventas en pestaña nueva: entra solo (' + pn.url() + ')');
  await pn.close();
  await p.goto(PORTAL); await espera(p, 600);
  ok(await p.isVisible('#sistemas') && (await p.textContent('#quien-nombre')) === 'Sean Duarte', 'E. la página principal muestra los accesos de Sean');
  await p.screenshot({ path: 'acc_portal_sean.png' });
  await p.click('#btn-salir'); await espera(p, 400);

  // G. Primer ingreso (clave 1234): crea su clave en la página principal
  await ingresar(p, 'ana.nueva', '1234'); await espera(p, 400);
  ok(await p.isVisible('#paso2'), 'G. primer ingreso: pide crear la clave');
  await p.fill('#i-nueva', '1234'); await p.fill('#i-nueva2', '1234'); await p.click('#btn-clave'); await espera(p, 200);
  ok((await p.textContent('#msg')).includes('distinta'), 'G. no acepta 1234');
  await p.fill('#i-nueva', 'ana9'); await p.fill('#i-nueva2', 'ana9'); await p.click('#btn-clave'); await espera(p, 600);
  ok(USUARIOS['ana.nueva'].clave === 'ana9' && await p.isVisible('#sistemas'), 'G. clave creada y dentro');
  await p.click('#btn-salir'); await espera(p, 300);

  // H. Clave anterior: volver sin usuario Playmaker no hace bucle y muestra el ingreso propio
  const ph = await pagina(); await ph.goto(VENTAS); await ph.waitForURL(/sistemas\.html/); await espera(ph, 600);
  await ph.click('#antiguo a'); await ph.waitForURL(VENTAS + '**'); await espera(ph, 1500);
  ok(ph.url() === VENTAS && await ph.isVisible('#login-screen') && await ph.isVisible('#login-user'), 'H. «clave anterior» vuelve a Ventas con su ingreso propio, sin bucle');
  await ph.screenshot({ path: 'acc_ventas_login.png' });
  const pfh = await pagina(); await pfh.goto(FICHAS + '#pmk_acceso='); await espera(pfh, 1200);
  ok(pfh.url() === FICHAS && await pfh.isVisible('#btn-playmaker'), 'H. Fichas con clave anterior: botón «Entrar con mi usuario Playmaker» + ingreso propio');
  await pfh.screenshot({ path: 'acc_fichas_login.png' });
  await pfh.click('#btn-playmaker'); await pfh.waitForURL(/sistemas\.html/);
  ok(true, 'H. el botón lleva a la página principal');
  // K. sesión inválida en la dirección: no hace bucle
  const pk = await pagina(); await pk.goto(VENTAS + '#pmk_acceso=falsa'); await espera(pk, 1200);
  ok(pk.url() === VENTAS && await pk.isVisible('#login-screen'), 'K. sesión falsa: Ventas muestra su ingreso, sin bucle');
  // L. app instalada: abre en la página principal (mismo id que la app ya instalada) y la barra muestra el acceso
  const man = JSON.parse(fs.readFileSync(path.join(BASE, 'produccion/manifest.webmanifest'), 'utf8'));
  ok(man.start_url === 'sistemas.html' && man.id === './' && man.scope === './', 'L. manifest: abre en sistemas.html con el mismo id');
  ok(/'sistemas\.html'/.test(fs.readFileSync(path.join(BASE, 'produccion/sw.js'), 'utf8')), 'L. sw.js guarda sistemas.html');
  const pl = await pagina(); await pl.goto(PLAN); await espera(pl, 800);
  ok(await pl.evaluate(() => { const a = document.querySelector('.pmk-sis-inicio'); const r = a.getBoundingClientRect(); return !!a.querySelector('svg') && r.width > 80 && r.top === 0; }), 'L. barra: «PLAYMAKER» con ícono de todos los sistemas');
  await pl.click('.pmk-sis-inicio'); await pl.waitForURL(PORTAL + '**');
  ok(true, 'L. «PLAYMAKER» lleva a la página principal');
  ok(await pl.evaluate(() => !!document.querySelector('link[rel="manifest"]')), 'L. la página principal es instalable (manifest)');
  await pl.close();
  const cm = await b.newContext({ viewport: { width: 390, height: 780 }, userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36', serviceWorkers: 'block' });
  await cm.route('**/*', r => { const u = new URL(r.request().url()); if (u.host === 'planificacion-playmaker.netlify.app') { const f = path.join(BASE, 'produccion', u.pathname.slice(1) || 'index.html'); return fs.existsSync(f) ? r.fulfill({ body: fs.readFileSync(f), contentType: f.endsWith('.html') ? 'text/html' : 'application/octet-stream' }) : r.fulfill({ status: 404 }); }
    if (/plan_usuarios/.test(u.pathname)) return r.fulfill({ contentType: 'application/json', body: '[]' }); return r.fulfill({ contentType: 'application/json', body: 'null' }); });
  const pm = await cm.newPage(); pm.on('pageerror', e => errores.push('movil: ' + e.message)); await pm.goto(PORTAL); await espera(pm, 600);
  ok(await pm.isVisible('#btn-instalar'), 'L. celular: botón «Instalar Playmaker en este teléfono»');
  await pm.click('#btn-instalar'); await espera(pm, 200);
  ok((await pm.textContent('#pasos-instalar')).includes('Instalar aplicación'), 'L. celular: explica cómo instalar');
  await pm.screenshot({ path: 'acc_movil_instalar.png', fullPage: true });
  await cm.close();
  ok(errores.length === 0, 'sin errores de JavaScript ' + errores.join(' | '));
  await b.close();
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK');
  process.exit(fallas ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
