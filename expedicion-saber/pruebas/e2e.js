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
    case 'respuesta_numerica': {
      const v = bien ? d.respuesta : d.respuesta + d.tolerancia + 1;
      if (v < 0) await page.click('#zona [data-k="−"]');
      for (const k of String(Math.abs(v))) await page.click(`#zona [data-k="${k}"]`);
      return clic('#btn-comprobar');
    }
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
  // forzar un desafío elegido por una condición, en su asignatura y OA
  const forzar = cond => page.evaluate(c => {
    const z = Object.values(window.ES.A.datos.objetivos).flatMap(o => o.desafios.map(x => ({ x, o }))).find(new Function('z', 'return ' + c));
    window.__forzado = z.x; window.Motor.elegirDesafio = () => window.__forzado;
    window.ES.iniciarSesion(z.o.asignatura, z.o.id_objetivo);
    return z.x;
  }, cond);
  // Inglés: el audio se escucha con su botón y el texto se puede ver si la voz falla
  const conAudio = await forzar("z.x.audio && z.x.tipo === 'opcion_multiple'");
  await page.waitForSelector('.audio-en');
  if (await page.locator('#btn-audio-ver').count()) await page.click('#btn-audio-ver');
  const textoAudio = await page.textContent('#texto-audio');
  if (textoAudio.trim() !== conAudio.audio.texto) throw new Error('el texto del audio no coincide');
  await page.screenshot({ path: path.join(salida, 'ingles_audio.png') });
  await responder(page, true);
  await page.waitForSelector('#btn-sig:not([hidden])');
  console.log(`✓ inglés con audio: «${conAudio.audio.texto}» se puede escuchar y ver`);
  // Números enteros: la tecla «−» permite responder un negativo
  const negativo = await forzar("z.x.tipo === 'respuesta_numerica' && z.x.respuesta < 0");
  await page.waitForSelector('#zona [data-k="−"]');
  await responder(page, true);
  await page.waitForSelector('#btn-sig:not([hidden])');
  if (!/Correcto/.test(await page.textContent('#retro'))) throw new Error('no aceptó la respuesta negativa');
  console.log(`✓ respuesta negativa (${negativo.respuesta}) con la tecla «−»`);
  // las asignaturas en la base de un perfil de 6° básico
  await page.evaluate(() => { window.ES.A.ses = null; window.ES.perfil().nivel_escolar = '6_basico'; window.ES.ir('base'); });
  await page.waitForSelector('.asignatura');
  const tarjetas = await page.locator('.asignatura h3').allTextContents();
  console.log('Base de 6° básico:', tarjetas.join(' · '));
  if (tarjetas.length !== 4) throw new Error('la base debía mostrar 4 asignaturas');
  await page.screenshot({ path: path.join(salida, 'base_6basico.png'), fullPage: true });
  // un perfil de 4° medio ve sus cuatro asignaturas con objetivos de su curso
  await page.evaluate(() => { window.ES.A.ses = null; window.ES.guardar(); });
  await page.reload(); // deja el motor sin los desafíos forzados de las pruebas anteriores
  await page.waitForSelector('.asignatura');
  await page.evaluate(() => { window.ES.perfil().nivel_escolar = '4_medio'; window.ES.ir('base'); });
  await page.waitForSelector('.asignatura');
  const medio = await page.locator('.asignatura').evaluateAll(els => els.map(e => `${e.querySelector('h3').textContent} (${(e.querySelector('.oa strong') || {}).textContent || '-'})`));
  console.log('Base de 4° medio:', medio.join(' · '));
  if (medio.length !== 4 || medio.some(t => !/4° medio/.test(t))) throw new Error('la base de 4° medio debía mostrar objetivos de 4° medio en las 4 asignaturas');
  if (!medio.some(t => t.startsWith('Lengua y Literatura')) || !medio.some(t => t.startsWith('Ciencias para la Ciudadanía'))) throw new Error('faltan los nombres de asignatura de media');
  await page.click('[data-jugar="matematica"]');
  await page.waitForSelector('#zona');
  await responder(page, true);
  await page.waitForSelector('#btn-sig:not([hidden])');
  console.log('✓ desafío de 4° medio:', await page.textContent('.reto-cab .nota'));
  await page.evaluate(() => { window.ES.A.ses = null; window.ES.perfil().nivel_escolar = '6_basico'; });
  // los tres mundos: cada uno se elige, dibuja su avatar y vende sus propias mejoras
  await page.evaluate(() => { window.ES.perfil().monedas += 300; window.ES.guardar(); });
  for (const mundo of ['heroes', 'plataformas']) {
    await page.evaluate(() => window.ES.ir('mundos'));
    await page.waitForSelector('canvas.vista-mundo');
    await page.click(`button[data-mundo="${mundo}"]`);
    await page.waitForSelector('.asignatura');
    await page.click('#principal [data-ir="taller"]');
    await page.waitForSelector('.taller-escena');
    if (mundo === 'heroes') await page.click('[data-color="0"]');
    for (let k = 0; k < 2; k++) await page.click('.espacio button[data-mejorar]:not([disabled])');
    await page.waitForTimeout(300);
    const estado = await page.evaluate(m => ({ avatar: window.ES.perfil().avatares[m], estilo: window.ES.perfil().estilo }), mundo);
    if (Object.values(estado.avatar).filter(v => v > 0).length < 1) throw new Error(mundo + ': no se compró ninguna mejora');
    await page.screenshot({ path: path.join(salida, `taller_${mundo}.png`) });
    console.log(`✓ mundo ${mundo}: avatar ${JSON.stringify(estado.avatar)}${mundo === 'heroes' ? ', colores ' + estado.estilo.heroes : ''}`);
  }
  await page.evaluate(() => window.ES.ir('mundos'));
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(salida, 'mundos.png'), fullPage: true });
  console.log('Errores de consola:', errores.length ? errores.join('\n') : 'ninguno');
  await browser.close();
  if (errores.length) process.exit(1);
})().catch(e => { console.error(e); process.exit(1); });
