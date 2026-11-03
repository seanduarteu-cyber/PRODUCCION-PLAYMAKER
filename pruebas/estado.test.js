// Pestaña «Estado» para todos y pendientes que vuelven a Armado de mesa y Corte juntos
const { chromium, contexto, revisar } = require('./comun_movil');
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, 'plan_movil.js'), 'utf8');
const datos = new Function('require', src.slice(src.indexOf('const d ='), src.indexOf('(async')) + 'return datos;')(require);
datos.tablas.plan_pendientes = [{ id: 1, planificacion_id: 3, cot: 'COT-3612', cliente: 'x', etapa: 'CORTE', estado: 'pendiente', tipo_prenda: 'Camiseta', pieza: 'Manga', cantidad: 1, ruta: 'CORTE>SUBL>CONFEC', grupo: 'g1' },
  { id: 2, planificacion_id: 3, cot: 'COT-3612', cliente: 'x', etapa: 'ARMADO', estado: 'pendiente', tipo_prenda: 'Camiseta', pieza: 'Manga', cantidad: 1, ruta: 'ARMADO>REVISION>PLOTEO>SUBL>CONFEC', grupo: 'g1' }];
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const PERFILES = { admin: { roles: ['admin'] }, corte: { roles: ['CORTE'] }, vendedor: { roles: ['fichas', 'ventas'] }, taller: { roles: ['taller'], ejecutante_id: 2 } };
(async () => {
  const b = await chromium.launch(); const errores = [];
  for (const [k, perfil] of Object.entries(PERFILES)) {
    const comun = require('./comun_movil');
    const ctx = await contexto(b, datos, k === 'admin' ? { viewport: { width: 1366, height: 800 }, isMobile: false, hasTouch: false, deviceScaleFactor: 1, userAgent: undefined } : {});
    // usuario de cada perfil
    await ctx.route(/ygcsqrylpibhofvetdyh\.supabase\.co\/rest\/v1\/rpc\/plan_sesion/, r => r.fulfill({ contentType: 'application/json', body: JSON.stringify({ usuario: 'u.' + k, nombre: 'Usuario ' + k, rol: perfil.roles[0], roles: perfil.roles, ejecutante_id: perfil.ejecutante_id || null }) }));
    const p = await ctx.newPage(); p.on('pageerror', e => errores.push(k + ': ' + e.message)); p.on('dialog', d => d.accept());
    await p.goto('https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(2500);
    const tabs = await p.evaluate(() => tabsPara());
    if (k === 'taller') { ok(!tabs.includes('estado'), '[taller] no ve «Estado» (sigue viendo solo lo suyo): ' + tabs.join(',')); await ctx.close(); continue; }
    ok(tabs.includes('estado'), `[${k}] ve la pestaña «Estado» (${tabs.join(',')})`);
    await p.evaluate(() => irTab('estado')); await p.waitForTimeout(500);
    const filas = await p.$$eval('#lista-est tr.fila-est', t => t.length);
    ok(filas === 8, `[${k}] muestra los 8 pedidos (${filas})`);
    if (k === 'admin') {
      // pedido 1 (i=0): Armado en proceso, el resto espera; Corte puede empezar (sin dependencias)
      const celdas = await p.$$eval('#lista-est tr.fila-est', t => t.map(r => [...r.querySelectorAll('.ce')].map(c => c.className.replace('ce ', '')).join(' ')));
      console.log('      ', celdas.slice(0, 4).join('\n        '));
      const c1 = celdas[0].split(' ');
      ok(c1[0] === 'proc' && c1[1] === 'listo' && c1[2] === 'espera' && c1[4] === 'espera', '[admin] COT-3610: Armado en proceso, Corte puede empezar, Revisión y Sublimación esperan');
      const c3 = celdas[2].split(' ');   // i=2: ARMADO y CORTE terminados, REVISION en proceso
      ok(c3[0] === 'ok' && c3[1] === 'ok' && c3[2] === 'proc' && c3[4] === 'espera', '[admin] COT-3612: Armado y Corte ✓, Revisión en proceso, Sublimación espera');
      ok(await p.$eval('#lista-est tr.fila-est:nth-child(3) .chip-pend', e => e.textContent).catch(() => '') === '1 por rehacer · Armado, Corte', '[admin] COT-3612 muestra «1 por rehacer · Armado, Corte»');
      const tip = await p.$eval('#lista-est tr.fila-est:nth-child(1) td:nth-child(7) .ce', e => e.title);
      ok(/Sublimación: Espera que termine: Ploteo, Corte/.test(tip), '[admin] Sublimación explica qué espera: «' + tip + '»');
      // filtros
      await p.selectOption('#f-est', 'pend'); await p.waitForTimeout(200);
      ok(await p.$$eval('#lista-est tr.fila-est', t => t.length) === 1, '[admin] filtro «Con pendientes» deja 1');
      await p.selectOption('#f-est', ''); await p.selectOption('#fe-est', 'SUBL'); await p.waitForTimeout(200);
      ok(await p.$$eval('#lista-est tr.fila-est', t => t.map(r => r.querySelector('b').textContent).join()) === 'COT-3614', '[admin] filtro «En Sublimación»');
      await p.selectOption('#fe-est', ''); await p.fill('#q-est', '3613'); await p.waitForTimeout(200);
      ok(await p.$$eval('#lista-est tr.fila-est', t => t.length) === 1, '[admin] búsqueda por N° de pedido');
      await p.fill('#q-est', ''); await p.evaluate(() => renderListaEstado());
      await p.screenshot({ path: 'movil/estado_escritorio.png', fullPage: true });
      await p.click('#lista-est tr.fila-est'); await p.waitForTimeout(500);
      ok(await p.evaluate(() => document.getElementById('fondo').classList.contains('on')), '[admin] tocar un pedido abre su detalle');
      await p.evaluate(() => cerrarModal());
      // pendiente: opciones de reingreso
      await p.evaluate(() => abrirPendiente(1, 'SUBL')); await p.waitForTimeout(300);
      const ops = await p.$$eval('#pe-etapa option', o => o.map(x => x.textContent));
      ok(ops[0] === 'Armado de mesa y Corte, a la vez' && !ops.some(t => /Solo|^Corte$|^Armado de mesa$/.test(t)), '[admin] pendiente: Armado y Corte solo juntos · ' + ops.join(' | '));
      ok(/Recorrido: Armado de mesa → Revisión de mesa → Ploteo → Sublimación/.test(await p.textContent('#pe-ruta')) && /Corte<\/b>, que se junta en Sublimación/.test(await p.innerHTML('#pe-ruta')), '[admin] recorrido: Armado → Revisión → Ploteo → Sublimación, y Corte se junta en Sublimación');
      await p.evaluate(() => cerrarModal());
    } else {
      const r = await revisar(p); ok(r.anchoPagina <= r.ancho, `[${k}] celular: la página no se sale del ancho (${r.anchoPagina}/${r.ancho})`);
      await p.screenshot({ path: 'movil/estado_' + k + '.png', fullPage: true });
    }
    await ctx.close();
  }
  ok(errores.length === 0, 'sin errores de JavaScript ' + errores.join(' | '));
  await b.close(); console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
