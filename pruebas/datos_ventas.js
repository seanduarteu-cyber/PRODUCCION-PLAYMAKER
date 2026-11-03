const { fs, path, BASE } = require('./comun_movil');
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
module.exports = datos;
