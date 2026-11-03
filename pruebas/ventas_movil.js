// Ventas en el celular: cada vista y el detalle del pedido, con pedidos, abonos con comprobantes, gastos y proveedores
const { chromium, contexto, revisar, fs, path, BASE } = require('./comun_movil');
const PNG = fs.readFileSync(path.join(BASE, 'produccion/icon-192.png')).toString('base64');
const PDF = Buffer.from('%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 200 200]/Parent 2 0 R>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF').toString('base64');
const hoy = new Date().toISOString().slice(0, 10);
const VEND = ["Javiera D'Orival", 'Sean Duarte', 'Silvia Urbina', 'Antonia Hermosilla'];
const pedidos = Array.from({ length: 14 }, (_, i) => ({
  id: i + 1, cot: 'COT-36' + String(10 + i), cliente: ['Club Deportivo Universidad Católica Rugby Femenino', 'Colegio San Ignacio El Bosque', 'Academia de Fútbol Los Leones de Maipú', 'Rama Básquetbol'][i % 4],
  fecha: hoy, estado: ['Pagado', 'Abono parcial', 'Pendiente de pago'][i % 3], vendedor: VEND[i % 4], canal: ['Directo', 'Heat', 'Web'][i % 3], tipo_venta: 'Uniformes', cantidad: 20 + i,
  disenador: 'José Galdames', total: 1250000 + i * 1000, neto: 1050420, saldo: i % 3 === 0 ? 0 : 450000, descuento_pct: i % 2 ? 5 : 0,
  abonos: [{ monto: 800000, fecha: hoy, metodo: 'Transferencia electrónica', comp64: PNG, compMime: 'image/png', compName: 'transferencia_banco_estado_' + i + '.png' },
           { monto: 200000, fecha: hoy, metodo: 'Depósito bancario', comp64: PDF, compMime: 'application/pdf', compName: 'deposito.pdf' }],
  docs: [{ tipo: 'FACTURA', ndoc: '10' + i }], observaciones: [{ autor: 'Sean Duarte', texto: 'Cliente pide entrega antes del torneo, confirmar tallas con la profesora encargada.', fecha: new Date().toISOString() }],
  created_at: new Date().toISOString()
}));
const gastos = Array.from({ length: 6 }, (_, i) => ({ id: i + 1, fecha: hoy, descripcion: 'Compra de tela poliéster dry-fit para producción de noviembre ' + i, categoria: 'Insumos', proveedor: 'Textiles del Sur SpA', metodo_pago: 'Transferencia', monto: 350000 + i * 1000 }));
const datos = { tablas: { pedidos, gastos, proveedores: [{ id: 1, nombre: 'Textiles del Sur SpA', rut: '76.123.456-7' }] } };
(async () => {
  const b = await chromium.launch();
  const ctx = await contexto(b, datos);
  const p = await ctx.newPage(); const errores = []; p.on('pageerror', e => errores.push(e.message)); p.on('dialog', d => d.accept());
  await p.goto('https://ventas-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(2500);
  const informe = {};
  for (const v of ['dashboard', 'pedidos', 'cobranza', 'facturacion', 'gastos', 'flujo', 'comisiones', 'nuevo']) {
    await p.evaluate(v => showView(v), v); await p.waitForTimeout(500);
    informe[v] = await revisar(p);
    await p.screenshot({ path: 'movil/ventas_' + v + '.png', fullPage: true });
  }
  await p.evaluate(() => showView('pedidos')); await p.evaluate(() => verDetalle(1)); await p.waitForTimeout(400);
  informe.detalle = await revisar(p);
  await p.screenshot({ path: 'movil/ventas_detalle.png' });
  await p.evaluate(() => { const m = document.querySelector('#modal-overlay .modal'); m.scrollTop = m.scrollHeight; }); await p.waitForTimeout(200);
  await p.screenshot({ path: 'movil/ventas_detalle_abajo.png' });
  // comprobantes: la imagen se ve en pantalla y se cierra
  await p.click('#modal-body a[download]'); await p.waitForTimeout(400);
  const visor = await p.evaluate(() => { const v = document.querySelector('.comp-visor'); const i = v && v.querySelector('img'); return v ? { img: !!(i && i.naturalWidth), ancho: v.getBoundingClientRect().width } : null; });
  console.log('visor imagen:', JSON.stringify(visor));
  await p.screenshot({ path: 'movil/ventas_comprobante.png' });
  await p.click('.comp-visor button'); await p.waitForTimeout(200);
  console.log('visor cerrado:', !(await p.$('.comp-visor')));
  await p.click('#modal-body tr:nth-child(2) a[download]'); await p.waitForTimeout(400);
  console.log('visor pdf:', await p.evaluate(() => !!document.querySelector('.comp-visor iframe') && !!document.querySelector('.comp-visor a[target]')));
  await p.click('.comp-visor button');
  for (const [k, v] of Object.entries(informe)) console.log(k.padEnd(12), 'página', v.anchoPagina + '/' + v.ancho, '| recortados', v.cortados.length, v.cortados.slice(0, 5).join(' | '), '| fuera', v.fuera.length, v.fuera.slice(0, 4).join(' | '));
  console.log('errores JS:', errores.join(' | ') || 'ninguno');
  await b.close();
})();
