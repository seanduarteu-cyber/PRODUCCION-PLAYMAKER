// Sitio del cliente: basta con la talla (sin preguntas de nombre ni número), lista pegada desde Excel con sus columnas,
// cada prenda con su propia lista (el short no se junta con la camiseta), sin paso de arquero y medias por pares por talla.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const HTML = fs.readFileSync(path.resolve(__dirname, '../sistemas/ingreso-fichas/index.html'));
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const TAB = '\t';

async function abrir() {
  const ficha = { id: 1, ref: 'COT-7100', cliente: 'CLUB PRUEBA', proyecto: 'Uniformes', estado: 'abierto', acceso: 'ABC',
    items: [{ prenda: 'camiseta', cant: 10 }, { prenda: 'short', cant: 3 }, { prenda: 'medias', cant: 11 }],
    specs: { camiseta: { deporte: 'Fútbol', moldes: { Masculino: 'FUTHOMU02|18' }, unidades: { Masculino: 10 } },
             short: { moldes: { Masculino: 'FUT-SH|69' }, unidades: { Masculino: 3 } },
             medias: { nombre: 'Medias azules' } },
    imagenes: [{ url: 'https://x.test/m.jpg', prendas: ['medias'], prenda: 'medias', vista: 'Completo' }], created_at: new Date().toISOString() };
  const detalle = [], borrados = [], patches = [];
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await ctx.route('**/*', async r => {
    const req = r.request(), u = new URL(req.url());
    if (u.host === 'ingreso-fichas-playmaker.netlify.app') return r.fulfill({ body: HTML, contentType: 'text/html' });
    if (u.host === 'jvgifibnoigpicwklasw.supabase.co') {
      if (/rpc\/ficha_cliente/.test(u.pathname)) return r.fulfill({ contentType: 'application/json', body: JSON.stringify(ficha) });
      if (/fichas_detalle/.test(u.pathname)) {
        if (req.method() === 'POST') {
          [].concat(JSON.parse(req.postData())).forEach(x => { const i = detalle.findIndex(d => d.id === x.id); if (i >= 0) detalle[i] = x; else detalle.push({ ...x, created_at: new Date().toISOString() }); });
          return r.fulfill({ status: 201, body: '' });
        }
        if (req.method() === 'DELETE') { const m = decodeURIComponent(u.search).match(/id=in\.\((.*)\)/); const ids = m ? m[1].split(',').map(x => x.replace(/"/g, '')) : [];
          ids.forEach(id => { const i = detalle.findIndex(d => d.id === id); if (i >= 0) { detalle.splice(i, 1); borrados.push(id); } }); return r.fulfill({ status: 204, body: '' }); }
        return r.fulfill({ contentType: 'application/json', body: JSON.stringify(detalle) });
      }
      if (/fichas_tallas/.test(u.pathname) && req.method() === 'PATCH') { const bd = JSON.parse(req.postData()); if (bd.specs) { patches.push(bd.specs); ficha.specs = bd.specs; } return r.fulfill({ status: 204, body: '' }); }
      if (/fichas_tallas/.test(u.pathname)) return r.fulfill({ contentType: 'application/json', body: JSON.stringify([ficha]) });
      return r.fulfill({ contentType: 'application/json', body: '[]' });
    }
    if (/fonts/.test(u.host)) return r.fulfill({ body: '' });
    return r.abort();
  });
  const p = await ctx.newPage(); p.errores = []; p.on('pageerror', e => p.errores.push(e.message)); p.on('dialog', d => d.accept());
  await p.goto('https://ingreso-fichas-playmaker.netlify.app/?f=ABC'); await p.waitForTimeout(700);
  await p.click('[data-ir="pedido"]'); await p.waitForTimeout(700);
  return { b, p, ficha, detalle, borrados, patches };
}
const paso = async (p, n) => { await p.click('[data-paso="' + n + '"]'); await p.waitForTimeout(400); };
const filas = p => p.$$eval('[data-fila]', ds => ds.map(d => ({ nom: d.querySelector('.nom').value, num: d.querySelector('.num').value, tal: d.querySelector('.tal').value,
  est: (d.querySelector('.est') || {}).value || '', duda: !!d.classList.contains('duda'), falta: d.classList.contains('falta'), oculta: d.hidden })));

(async () => {
  const { b, p, ficha, detalle, borrados, patches } = await abrir();
  const guia = await p.$eval('.guias a', a => a.getAttribute('href')).catch(() => '');
  ok(guia === 'https://planificacion-playmaker.netlify.app/guias/molde-18.jpg', 'la guía de tallas del molde 18 es la del catálogo, que viene con el sistema');
  // 1 · camiseta: planilla copiada de Excel, con títulos; 2 de 10 sin nombre ni número
  await paso(p, 0);
  ok(!(await p.$('[data-chip="lote_numero"]')) && !(await p.$('[data-chip="lote_estampar"]')), 'no pregunta si llevan número ni nombre estampado');
  const mangas = await p.$$eval('[data-chip="lote_manga"]', bs => bs.map(b => b.dataset.val));
  ok(mangas.join() === 'Corta,Larga', 'camiseta 18 (…02, raglán): manga corta o larga, sin la opción «sin mangas» (' + mangas.join(', ') + ')');
  const excel = ['N°' + TAB + 'Nombre' + TAB + 'Talla', '10' + TAB + 'M. Sepúlveda' + TAB + 'L', '7' + TAB + 'S. Rojas' + TAB + 'M', '4' + TAB + 'L. Pérez' + TAB + 'S',
    '9' + TAB + 'M.Soto' + TAB + 'XL', '11' + TAB + 'Ana María López' + TAB + 'm', '2' + TAB + 'Pía Díaz' + TAB + '2XL', '5' + TAB + 'José Ruiz' + TAB + 'XG',
    '8' + TAB + 'Luis Mena' + TAB + 'L', '' + TAB + '' + TAB + 'M', '' + TAB + '' + TAB + 'S'].join('\n');
  await p.fill('#lote-texto', excel); await p.click('#btn-leer'); await p.waitForTimeout(400);
  const cols = await p.$$eval('[data-col]', ss => ss.map(s => s.value));
  ok(cols.join() === 'numero,nombre,talla', 'columnas reconocidas por su título: ' + cols.join(', '));
  let fs1 = await filas(p);
  ok(fs1.length === 10, '10 filas (la fila de títulos no se carga)');
  ok(fs1[0].nom === 'M. Sepúlveda' && fs1[0].tal === 'L' && fs1[0].num === '10', '«M. Sepúlveda» es el nombre; la talla es la de su columna (L)');
  ok(fs1.map(x => x.tal).join() === 'L,M,S,XL,M,XXL,,L,M,S', 'tallas leídas: ' + fs1.map(x => x.tal || '—').join(','));
  ok(fs1[6].falta && !fs1[6].tal, '«XG» no es talla: esa fila queda marcada para revisar');
  ok(fs1[8].nom === '' && fs1[8].num === '' && !fs1[8].falta, 'fila solo con talla: válida, sin nombre ni número');
  ok(fs1[0].est === 'M. SEPÚLVEDA' && fs1[8].est === '', 'se estampa el nombre de cada fila; la que no tiene, va sin nombre');
  const cont = await p.textContent('#contador');
  ok(/10 personas/.test(cont) && /S: 2/.test(cont) && /M: 3/.test(cont) && /1 sin talla/.test(cont), 'resumen por talla: «' + cont.trim() + '»');
  await p.click('#chk-revisar input'); await p.waitForTimeout(300);
  fs1 = await filas(p);
  ok(fs1.filter(x => !x.oculta).length === 1, 'con «Ver solo las filas para revisar» queda solo la de «XG»');
  await p.click('#btn-guardar-lote'); await p.waitForTimeout(300);
  ok(/sin talla/.test(await p.textContent('.aviso.error')), 'sin talla no deja guardar (es lo único obligatorio)');
  await p.selectOption('[data-fila="6"] .tal', 'XL'); await p.waitForTimeout(200);
  await p.click('#btn-guardar-lote'); await p.waitForTimeout(900);
  ok(!(await p.$('#btn-guardar-arq')) && !/arquero/i.test(await p.innerText('#pmk')), 'no aparece el paso de arqueros o líberos');
  ok(detalle.length === 10 && detalle.every(d => Object.keys(d.tallas).join() === 'camiseta' && !d.arquero), '10 personas guardadas, solo con camiseta');
  ok(detalle.filter(d => !d.nombre && !d.numero).length === 2, 'las 2 sin nombre ni número se guardaron igual');

  // 2 · short: lista escrita; con números que ya están en la camiseta → personas aparte, sin juntarlas
  await paso(p, 1);
  ok(!/se junta/i.test(await p.innerText('#pmk')), 'el short no habla de juntarse con la camiseta');
  await p.fill('#lote-texto', '10 L\n7 M\nM Sepúlveda 4 S'); await p.click('#btn-leer'); await p.waitForTimeout(400);
  const fs2 = await filas(p);
  ok(fs2.map(x => x.num + '/' + x.tal).join() === '10/L,7/M,4/S' && fs2[2].nom === 'M Sepúlveda', 'línea «M Sepúlveda 4 S»: M es inicial y la talla es S');
  ok(!fs2.some(x => x.duda), 'sin dudas en esas líneas');
  await p.click('#btn-guardar-lote'); await p.waitForTimeout(900);
  const shorts = detalle.filter(d => d.tallas.short);
  ok(shorts.length === 3 && shorts.every(d => Object.keys(d.tallas).join() === 'short') && detalle.length === 13, 'el short queda como su propia lista (3 personas nuevas, no se suma a la camiseta)');

  // 3 · ambigüedad marcada
  await paso(p, 1);
  await p.fill('#lote-texto', 'M Rojas 12\nS Pérez 5 M'); await p.click('#btn-leer'); await p.waitForTimeout(400);
  const fs3 = await filas(p);
  ok(fs3[0].duda && fs3[0].tal === 'M', '«M Rojas 12»: ¿talla o inicial? queda marcada para revisar');
  ok(!fs3[1].duda && fs3[1].tal === 'M' && fs3[1].nom === 'S Pérez', '«S Pérez 5 M»: S es inicial, talla M');
  ok(/Agregar esta lista/.test(await p.innerText('#pmk')) && /Reemplazar las 3/.test(await p.innerText('#pmk')), 'si el paso ya tiene personas: agregar o reemplazar');
  await p.click('[data-chip="lote_modo"][data-val="reemplazar"]'); await p.waitForTimeout(200);
  await p.click('[data-fila="0"] [data-ok]'); await p.waitForTimeout(150);
  await p.click('#btn-guardar-lote'); await p.waitForTimeout(900);
  ok(detalle.filter(d => d.tallas.short).length === 2 && borrados.length === 3 && detalle.length === 12, 'reemplazar: quedan las 2 nuevas del short; la camiseta no se toca');

  // 4 · medias: pares por talla, con su montaje
  await paso(p, 2);
  ok(await p.$('[data-md="S"]') && await p.$('[data-md="Adulto"]') && await p.$('[data-md="Infantil"]') && /m\.jpg/.test(await p.innerHTML('.montajes-cli')), 'medias: tallas S, M, L, Adulto e Infantil, con su montaje');
  await p.fill('[data-md="S"]', '4'); await p.fill('[data-md="M"]', '6'); await p.fill('[data-md="Infantil"]', '1');
  ok(/11 pares de 11 · completo/.test(await p.textContent('#md-total')), 'total: ' + (await p.textContent('#md-total')).trim());
  await p.click('#btn-guardar-md'); await p.waitForTimeout(800);
  ok(JSON.stringify((ficha.specs.medias || {}).cantidades) === '{"S":4,"M":6,"Infantil":1}' && ficha.specs.medias.nombre === 'Medias azules', 'se guardan los pares por talla en la ficha (sin borrar su nombre)');
  const pasoMedias = await p.textContent('[data-paso="2"]').catch(() => '');
  ok(/11 de 11 pares/.test(await p.innerText('#pmk')), 'el paso de medias queda listo: 11 de 11 pares');

  // 5 · persona suelta: sin arquero y sin exigir número
  await p.click('#btn-agregar'); await p.waitForTimeout(400);
  ok(!(await p.$('[data-check="arquero"]')) && !(await p.$('[data-prenda="medias"]')), 'persona suelta: sin «arquero» y sin medias (van por cantidad)');
  await p.click('[data-chip="calce"][data-val="Masculino"]'); await p.click('[data-chip="t_camiseta"][data-val="M"]');
  await p.click('#btn-guardar'); await p.waitForTimeout(800);
  ok(detalle.length === 13 && !(await p.$('.aviso.error')), 'se agrega solo con calce y talla');

  // 6 · revisión final: el N° 10 de la camiseta y el del short no son «repetidos»
  await p.screenshot({ path: 'movil/cliente_pedido.png', fullPage: true });
  ok(p.errores.length === 0, 'sin errores JS ' + p.errores.join(' | '));
  await b.close();
  console.log(fallas ? fallas + ' FALLAS' : 'TODO OK'); process.exit(fallas ? 1 : 0);
})();
