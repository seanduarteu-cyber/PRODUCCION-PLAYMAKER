// Panel de fichas en el celular: lista, ficha, ficha técnica, listado, moldes, catálogo, crear y ficha de producción
const { chromium, contexto, revisar } = require('./comun_movil');
const hoy = new Date().toISOString().slice(0, 10), ahora = new Date().toISOString();
const ficha = (i, estado) => ({ id: i, ref: 'COT-36' + (10 + i), proyecto: 'Uniformes temporada 2026', cliente: 'Club Deportivo Universidad Católica Rugby Femenino ' + i, vendedor: "Javiera D'Orival",
  entrega: hoy, entrega_interna: hoy, entrega_cliente: hoy, ventas_id: i, estado, created_at: ahora, confirmado_at: estado === 'confirmado' ? ahora : null, imagenes: [],
  items: [{ prenda: 'camiseta', cant: 22 }, { prenda: 'short', cant: 22 }, { prenda: 'medias', cant: 22 }],
  specs: { camiseta: { deporte: 'Rugby', nombre: 'Diseño titular rojo con franjas', moldes: { Masculino: 'RB-HOMUCC02|101', Femenino: 'RB-MUJU02|111' }, unidades: { Masculino: 12, Femenino: 10 } },
           short: { deporte: 'Rugby', moldes: { Masculino: 'CA-MUJ|105' }, unidades: { Masculino: 22 } } } });
const fichas = [ficha(0, 'confirmado'), ficha(1, 'abierto'), ficha(2, 'confirmado')];
const personas = Array.from({ length: 22 }, (_, i) => ({ id: 'p' + i, ref: 'COT-3610', nombre: 'Persona con nombre bastante largo ' + i, estampado: 'APELLIDOLARGO' + i, numero: String(i + 1),
  calce: i % 2 ? 'Femenino' : 'Masculino', manga: 'Corta', arquero: i === 0, obs: i === 3 ? 'Talla especial, revisar largo de manga y ancho de espalda' : '', tallas: { camiseta: ['S', 'M', 'L', 'XL'][i % 4], short: 'M', medias: '39-42' }, disenos: {}, created_at: ahora }));
const datos = { tablas: {
  fichas_tallas: u => /ref=eq\./.test(u.search) ? fichas.filter(f => u.search.includes(encodeURIComponent(f.ref)) || u.search.includes(f.ref)) : fichas,
  fichas_detalle: personas, fichas_avisos: [], moldes: [], catalogo_tecnico: [{ id: 1, tipo: 'tela', nombre: 'Poliéster dry-fit 140 g' }],
  pedidos: [{ id: 9, cliente: 'Academia de Fútbol Los Leones de Maipú', cot: 'COT-3700', cantidad: 30, fecha: hoy, vendedor: 'Sean Duarte', estado: 'Pagado', created_at: ahora }] } };
(async () => {
  const b = await chromium.launch();
  const ctx = await contexto(b, datos);
  const p = await ctx.newPage(); const errores = []; p.on('pageerror', e => errores.push(e.message)); p.on('dialog', d => d.accept());
  const informe = {};
  const foto = async n => { await p.waitForTimeout(700); informe[n] = await revisar(p); await p.screenshot({ path: 'movil/fichas_' + n + '.png', fullPage: true }); };
  await p.goto('https://panel-fichas-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(1500); await foto('lista');
  for (const ir of ['ventas', 'moldes', 'catalogo', 'crear']) {
    await p.goto('https://panel-fichas-playmaker.netlify.app/'); await p.waitForTimeout(1200);
    const bt = await p.$('[data-ir="' + ir + '"]'); if (!bt) { console.log('sin botón', ir); continue; }
    await bt.click(); await foto(ir);
  }
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3610'); await p.waitForTimeout(1500); await foto('ficha');
  for (const ir of ['tecnica', 'listado-ed', 'editar', 'pdf']) {
    await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3610'); await p.waitForTimeout(1500);
    const bt = await p.$('[data-ir="' + ir + '"]'); if (!bt) { console.log('sin botón', ir); continue; }
    await bt.click(); await foto(ir);
  }
  // catálogo y moldes (desde la ficha técnica)
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3610'); await p.waitForTimeout(1500);
  await p.click('[data-ir="tecnica"]'); await p.waitForTimeout(800);
  if (await p.$('[data-ir="catalogo"]')) { await p.click('[data-ir="catalogo"]'); await foto('catalogo');
    if (await p.$('[data-ir="moldes"]')) { await p.click('[data-ir="moldes"]'); await foto('moldes'); } }
  // pestañas de la ficha
  await p.goto('https://panel-fichas-playmaker.netlify.app/?ref=COT-3610'); await p.waitForTimeout(1500);
  const pest = await p.$$eval('[data-pest]', bs => bs.map(b => b.dataset.pest));
  for (const k of pest) { await p.click('[data-pest="' + k + '"]'); await foto('pest_' + k); }
  for (const [k, v] of Object.entries(informe)) console.log(k.padEnd(14), 'página', v.anchoPagina + '/' + v.ancho, '| recortados', v.cortados.length, v.cortados.slice(0, 4).join(' | '), '| fuera', v.fuera.length, v.fuera.slice(0, 4).join(' | '));
  console.log('errores JS:', errores.join(' | ') || 'ninguno');
  await b.close();
})();
