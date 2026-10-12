/* Prueba de punta a punta en un navegador (Playwright).
   Requiere el juego servido en http://localhost:8765 (python3 -m http.server 8765 desde expedicion-saber/).
   Uso: node pruebas/e2e.js [ruta-de-capturas] */
'use strict';
const path = require('path');
const pw = (() => { try { return require('playwright'); } catch (e) { return require('/opt/node-tools/node_modules/playwright'); } })();
const salida = process.argv[2] || path.join(__dirname, 'capturas');
require('fs').mkdirSync(salida, { recursive: true });

// Responde el desafío actual usando la interfaz, como lo haría un niño.
async function responder(page, bien = true) {
  const d = await page.evaluate(() => window.ES.A.ses.d);
  const clic = sel => page.click(sel);
  switch (d.tipo) {
    case 'opcion_multiple': case 'completar': {
      const i = bien ? d.correcta : (d.correcta + 1) % 4;
      return clic(`#zona [data-i="${i}"]`);
    }
    case 'ordenar_secuencia': {
      const orden = bien ? d.elementos : d.elementos.slice().reverse();
      // tras un intento fallido las fichas quedan en la fila (las malas marcadas): se devuelven primero
      while (await page.locator('#zona [data-fila]').count()) await page.locator('#zona [data-fila]').first().click();
      for (const t of orden) await page.locator('#zona [data-banco]', { hasText: t }).first().click();
      return clic('#btn-comprobar');
    }
    case 'emparejar':
      for (let i = 0; i < d.pares.length; i++) {
        const a = d.pares[i][0], b = d.pares[bien ? i : (i + 1) % d.pares.length][1];
        await page.locator(`#zona [data-izq="${a.replace(/"/g, '\\"')}"]`).click();
        await page.locator(`#zona [data-der="${b.replace(/"/g, '\\"')}"]`).click();
      }
      return clic('#btn-comprobar');
    case 'arrastrar_categoria':
      for (let i = 0; i < d.elementos.length; i++) {
        await page.click(`#zona [data-el="${i}"]`);
        const c = bien ? d.elementos[i].categoria : (d.elementos[i].categoria + 1) % d.categorias.length;
        await page.click(`#zona .bandeja[data-bandeja="${c}"]`);
      }
      return clic('#btn-comprobar');
    case 'respuesta_numerica':
      for (const k of String(bien ? d.respuesta : d.respuesta + d.tolerancia + 1)) await page.click(`#zona [data-k="${k}"]`);
      return clic('#btn-comprobar');
  }
  throw new Error('tipo desconocido ' + d.tipo);
}

(async () => {
  const browser = await pw.chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => pw.chromium.launch());
  const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const errores = [];
  page.on('pageerror', e => errores.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/404/.test(m.text())) errores.push('console: ' + m.text()); });
  page.on('response', r => { if (r.status() >= 400 && !r.url().endsWith('/favicon.ico')) errores.push(`HTTP ${r.status()} ${r.url()}`); });
  await page.goto('http://localhost:8765/index.html');
  await page.waitForSelector('#form-perfil');
  await page.fill('#nombre', 'León');
  await page.selectOption('#nivel', '3_basico');
  await page.click('#form-perfil button[type=submit]');
  await page.click('[data-mundo="bloques"]');
  await page.click('[data-jugar="matematica"]');
  const tipos = new Set();
  for (let k = 0; k < 10; k++) {
    await page.waitForSelector('#zona');
    const d = await page.evaluate(() => window.ES.A.ses.d);
    tipos.add(d.tipo);
    if (k === 1 && ['opcion_multiple', 'completar', 'respuesta_numerica'].includes(d.tipo)) {
      await responder(page, false); // un error: debe mostrar la pista y no restar monedas
      const pista = await page.textContent('#retro');
      if (!/Pista/.test(pista)) throw new Error('no apareció la pista tras un error');
    }
    if (k === 2) await page.screenshot({ path: path.join(salida, 'desafio.png') });
    await responder(page, true);
    await page.waitForSelector('#btn-sig:not([hidden])');
    await page.click('#btn-sig');
  }
  await page.waitForSelector('.resumen');
  const resumen = await page.evaluate(() => {
    const p = window.ES.perfil();
    return { monedas: p.monedas, racha: p.racha.dias, sesiones: p.historial.sesiones, oas: Object.fromEntries(Object.entries(p.oas).map(([k, v]) => [k, v.nivel])) };
  });
  console.log('Tras la sesión:', JSON.stringify(resumen), '| tipos vistos:', [...tipos].join(', '));
  if (resumen.monedas < 50) throw new Error('la primera sesión no alcanza para la primera mejora');
  await page.click('.resumen [data-ir="taller"]');
  await page.click('[data-mejorar="casco"]');
  await page.click('[data-mejorar="herramienta"]').catch(() => {});
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(salida, 'taller.png') });
  const avatar = await page.evaluate(() => window.ES.perfil().avatares.bloques);
  console.log('Avatar:', JSON.stringify(avatar));
  // persistencia: recargar y seguir con el mismo perfil
  await page.reload();
  await page.waitForSelector('.asignatura');
  const persistido = await page.evaluate(() => ({ nombre: window.ES.perfil().nombre, casco: window.ES.perfil().avatares.bloques.casco }));
  console.log('Tras recargar:', JSON.stringify(persistido));
  // árbol de Lenguaje
  await page.click('[data-arbol="lenguaje"]');
  await page.waitForSelector('.nodo');
  console.log('Nodos en el árbol de Lenguaje:', await page.locator('.nodo').count());
  // los seis tipos de desafío: se fuerza uno de cada tipo, con un intento fallido antes del correcto
  for (const tipo of ['opcion_multiple', 'completar', 'ordenar_secuencia', 'emparejar', 'arrastrar_categoria', 'respuesta_numerica']) {
    await page.evaluate(t => {
      const d = Object.values(window.ES.A.datos.objetivos).flatMap(o => o.desafios.map(x => ({ x, o }))).find(z => z.x.tipo === t && (t !== 'respuesta_numerica' || z.x.tolerancia === 0));
      window.__forzado = d.x; window.Motor.elegirDesafio = () => window.__forzado;
      window.ES.iniciarSesion(d.o.asignatura, d.o.id_objetivo);
    }, tipo);
    await page.waitForSelector('#zona');
    const antes = await page.evaluate(() => window.ES.perfil().monedas);
    await responder(page, false);
    if (!/Pista/.test(await page.textContent('#retro'))) throw new Error(tipo + ': falta la pista tras el error');
    if (await page.evaluate(() => window.ES.perfil().monedas) !== antes) throw new Error(tipo + ': un error cambió las monedas');
    if (tipo === 'arrastrar_categoria') await page.screenshot({ path: path.join(salida, 'categoria.png') });
    await responder(page, true);
    await page.waitForSelector('#btn-sig:not([hidden])');
    const ganadas = await page.evaluate(() => window.ES.perfil().monedas) - antes;
    if (ganadas !== 5) throw new Error(`${tipo}: al segundo intento debía dar 5 monedas y dio ${ganadas}`);
    console.log(`✓ ${tipo}: pista tras el error y 5 monedas al segundo intento`);
  }
  console.log('Errores de consola:', errores.length ? errores.join('\n') : 'ninguno');
  await browser.close();
  if (errores.length) process.exit(1);
})().catch(e => { console.error(e); process.exit(1); });
