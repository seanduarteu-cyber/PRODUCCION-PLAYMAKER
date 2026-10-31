// Exporta a Excel (.xlsx) con una estructura parecida a la planilla original.
import ExcelJS from 'exceljs';
import {
  etiquetaCuota, nombreCategoria, pagadoBoleta, restanteDeuda, saldoBoleta, situacionBoleta, tipoCategoria,
  totalIngresos, ultimoMesDeuda, type ResumenMes,
} from './calc';
import { hoy, mesDe, nombreMes, nombreMesCorto } from './format';
import { filasIngresos, tituloPeriodo, type DatosInforme } from './informe';
import { TIPOS_DEUDA } from './types';

const CLP = '"$"#,##0;[Red]-"$"#,##0';
const PCT = '0.0%';
const FECHA = 'dd-mm-yyyy';
const VERDE = 'FF0E7458';
const VERDE_SUAVE = 'FFE0F2EA';
const GRIS = 'FFF1F4F2';

const aFecha = (f: string) => {
  if (!f) return null;
  const [y, m, d] = f.split('-').map(Number);
  return new Date(Date.UTC(y, m - 1, d));
};
const aMes = (mes: string) => aFecha(`${mes}-01`);

function encabezado(ws: ExcelJS.Worksheet, fila: number, titulos: string[]) {
  const r = ws.getRow(fila);
  titulos.forEach((t, i) => {
    const c = r.getCell(i + 1);
    c.value = t;
    c.font = { bold: true, color: { argb: 'FFFFFFFF' } };
    c.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: VERDE } };
    c.alignment = { vertical: 'middle', wrapText: true };
  });
  r.height = 30;
}

function titulo(ws: ExcelJS.Worksheet, texto: string, sub?: string) {
  ws.getCell('A1').value = texto;
  ws.getCell('A1').font = { bold: true, size: 16, color: { argb: VERDE } };
  if (sub) {
    ws.getCell('A2').value = sub;
    ws.getCell('A2').font = { italic: true, color: { argb: 'FF5F6D67' } };
  }
}

function anchos(ws: ExcelJS.Worksheet, ws_: number[]) {
  ws_.forEach((w, i) => (ws.getColumn(i + 1).width = w));
}

function formato(ws: ExcelJS.Worksheet, cols: number[], fmt: string, desde: number, hasta: number) {
  for (let r = desde; r <= hasta; r++) for (const c of cols) ws.getRow(r).getCell(c).numFmt = fmt;
}

function hojaResumen(wb: ExcelJS.Workbook, d: DatosInforme, r: ResumenMes, nombreHoja: string) {
  const ws = wb.addWorksheet(nombreHoja, { views: [{ state: 'frozen', ySplit: 4 }] });
  titulo(ws, `Presupuesto familiar · ${d.familia}`, `Mes: ${nombreMes(r.mes)} · generado ${d.generado.toLocaleString('es-CL')}`);

  // Resumen del mes (columna K-L como en la planilla)
  const resumen: [string, number | string, string?][] = [
    ['Ingresos totales', r.ingresos, CLP],
    ['Ya pagado', r.totales.pagado, CLP],
    ['Por pagar (boletas, incl. atrasadas)', r.totales.porPagar, CLP],
    ['Saldo hoy (ingresos − pagado)', r.saldoHoy, CLP],
    ['Gasto esperado del mes', r.totales.esperado, CLP],
    ['SALDO PROYECTADO FIN DE MES', r.saldoProyectado, CLP],
    ['Estado del mes', r.estado.texto],
    ['Boletas atrasadas de meses anteriores', r.atrasadas, CLP],
    ['Gasto en ítems sin presupuesto', r.sinPresupuesto, CLP],
    ['Ingreso − presupuestado', r.ingresoMenosPresupuestado, CLP],
  ];
  encabezado(ws, 4, ['Categoría', 'Tipo', 'Presupuestado', 'Pagado', 'Por pagar (incl. atrasadas)', 'Total del mes', 'Gasto esperado del mes', 'Diferencia', '% del ingreso']);
  let fila = 5;
  for (const f of r.filas) {
    ws.getRow(fila).values = [
      f.categoria.nombre, f.categoria.tipo, f.presupuestado ?? null, f.pagado, f.porPagar, f.total, f.esperado,
      f.diferencia == null ? 'Sin presupuesto' : f.diferencia, f.pctIngreso,
    ];
    fila++;
  }
  const tot = ws.getRow(fila);
  tot.values = ['TOTAL GASTOS', '', r.totales.presupuestado, r.totales.pagado, r.totales.porPagar, r.totales.total, r.totales.esperado,
    r.totales.presupuestado - r.totales.total, r.ingresos ? r.totales.esperado / r.ingresos : 0];
  tot.font = { bold: true };
  tot.eachCell((c) => (c.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: VERDE_SUAVE } }));
  formato(ws, [3, 4, 5, 6, 7, 8], CLP, 5, fila);
  formato(ws, [9], PCT, 5, fila);

  ws.getCell('K4').value = 'RESUMEN DEL MES';
  ws.getCell('K4').font = { bold: true, color: { argb: VERDE } };
  resumen.forEach(([k, v, fmt], i) => {
    const row = 5 + i;
    ws.getCell(`K${row}`).value = k;
    const c = ws.getCell(`L${row}`);
    c.value = v;
    if (fmt) c.numFmt = fmt;
    if (k.startsWith('SALDO')) {
      ws.getCell(`K${row}`).font = { bold: true };
      c.font = { bold: true, color: { argb: (v as number) < 0 ? 'FFBF312A' : 'FF17803D' } };
    }
  });
  const d0 = 5 + resumen.length + 1;
  ws.getRow(d0).getCell(11).value = 'Distribución';
  ['Esperado', '% ingreso', 'Meta %', 'Estado'].forEach((t, i) => (ws.getRow(d0).getCell(12 + i).value = t));
  ws.getRow(d0).font = { bold: true };
  r.distribucion.forEach((x, i) => {
    const row = ws.getRow(d0 + 1 + i);
    row.getCell(11).value = x.tipo;
    row.getCell(12).value = x.esperado;
    row.getCell(12).numFmt = CLP;
    row.getCell(13).value = x.pct;
    row.getCell(13).numFmt = PCT;
    row.getCell(14).value = x.meta;
    row.getCell(14).numFmt = PCT;
    row.getCell(15).value = x.estado;
  });
  ws.getRow(fila + 2).getCell(1).value = 'Gasto esperado = el mayor entre lo presupuestado y lo pagado + por pagar. Saldo proyectado = ingresos − gasto esperado (incluye cuotas de deudas).';
  ws.getRow(fila + 2).getCell(1).font = { italic: true, size: 9, color: { argb: 'FF5F6D67' } };
  anchos(ws, [32, 13, 15, 14, 16, 15, 16, 16, 11, 3, 38, 16, 11, 9, 14]);
}

function hojaAnual(wb: ExcelJS.Workbook, d: DatosInforme) {
  const ws = wb.addWorksheet('Resumen por mes', { views: [{ state: 'frozen', xSplit: 1, ySplit: 4 }] });
  titulo(ws, `Resumen por mes · ${d.familia}`, tituloPeriodo(d));
  encabezado(ws, 4, ['Concepto', ...d.meses.map(nombreMesCorto), 'Total']);
  const filas: [string, (r: ResumenMes) => number][] = [
    ['Ingresos', (r) => r.ingresos],
    ['Presupuestado', (r) => r.totales.presupuestado],
    ['Pagado', (r) => r.totales.pagado],
    ['Por pagar', (r) => r.totales.porPagar],
    ['Gasto esperado', (r) => r.totales.esperado],
    ['Saldo proyectado', (r) => r.saldoProyectado],
    ['Cuotas del mes', (r) => r.cuotas.total],
  ];
  let row = 5;
  for (const [k, fn] of filas) {
    const vals = d.resumenes.map(fn);
    ws.getRow(row).values = [k, ...vals, k === 'Saldo proyectado' ? null : vals.reduce((a, b) => a + b, 0)];
    if (k === 'Saldo proyectado') ws.getRow(row).font = { bold: true };
    row++;
  }
  row++;
  ws.getRow(row).values = ['Pagado por categoría'];
  ws.getRow(row).font = { bold: true, color: { argb: VERDE } };
  row++;
  const cats = d.resumenes[0]?.filas.map((f) => f.categoria) ?? [];
  const extra = d.resumenes.flatMap((r) => r.filas.map((f) => f.categoria)).filter((c) => !cats.some((x) => x.id === c.id));
  for (const c of [...cats, ...extra.filter((c, i, a) => a.findIndex((x) => x.id === c.id) === i)]) {
    const vals = d.resumenes.map((r) => r.filas.find((f) => f.categoria.id === c.id)?.pagado ?? 0);
    if (!vals.some(Boolean)) continue;
    ws.getRow(row).values = [c.nombre, ...vals, vals.reduce((a, b) => a + b, 0)];
    row++;
  }
  formato(ws, d.meses.map((_, i) => i + 2).concat(d.meses.length + 2), CLP, 5, row);
  anchos(ws, [30, ...d.meses.map(() => 13), 15]);
}

function hojaRegistro(wb: ExcelJS.Workbook, d: DatosInforme) {
  const ws = wb.addWorksheet('Registro', { views: [{ state: 'frozen', ySplit: 4 }] });
  titulo(ws, 'Registro de gastos', tituloPeriodo(d));
  encabezado(ws, 4, ['Fecha', 'Categoría', 'Tipo', 'Descripción', 'Monto', 'Medio de pago', 'Registrado por', 'Mes', 'Origen']);
  let r = 5;
  for (const g of d.gastos) {
    ws.getRow(r).values = [
      aFecha(g.fecha), nombreCategoria(d.settings, g.categoriaId), tipoCategoria(d.settings, g.categoriaId), g.descripcion, g.monto,
      g.medioPago ?? '', g.creadoPorNombre, aMes(mesDe(g.fecha)), g.boletaId ? 'Pago de boleta' : g.deudaId ? 'Pago de cuota' : '',
    ];
    r++;
  }
  ws.getRow(r).values = ['TOTAL', '', '', '', d.gastos.reduce((s, g) => s + g.monto, 0)];
  ws.getRow(r).font = { bold: true };
  formato(ws, [1], FECHA, 5, r);
  formato(ws, [8], 'mmm-yyyy', 5, r);
  formato(ws, [5], CLP, 5, r);
  if (d.gastos.length) ws.autoFilter = { from: 'A4', to: `I${r - 1}` };
  anchos(ws, [12, 28, 13, 40, 14, 15, 18, 11, 15]);
}

function hojaIngresos(wb: ExcelJS.Workbook, d: DatosInforme) {
  const ws = wb.addWorksheet('Ingresos', { views: [{ state: 'frozen', ySplit: 4 }] });
  titulo(ws, 'Ingresos', tituloPeriodo(d));
  encabezado(ws, 4, ['Mes', 'Tipo', 'Descripción', 'Fecha', 'Monto', 'Registrado por']);
  let r = 5;
  for (const i of filasIngresos(d)) {
    ws.getRow(r).values = [aMes(i.mes), i.tipo, i.descripcion, aFecha(i.fecha), i.monto, i.por];
    r++;
  }
  ws.getRow(r).values = ['TOTAL', '', '', '', d.meses.reduce((s, m) => s + totalIngresos(d.settings, d.ingresos, m), 0)];
  ws.getRow(r).font = { bold: true };
  formato(ws, [1], 'mmm-yyyy', 5, r);
  formato(ws, [4], FECHA, 5, r);
  formato(ws, [5], CLP, 5, r);
  anchos(ws, [11, 8, 34, 12, 14, 18]);
}

function hojaBoletas(wb: ExcelJS.Workbook, d: DatosInforme) {
  const ws = wb.addWorksheet('Boletas', { views: [{ state: 'frozen', ySplit: 4 }] });
  titulo(ws, 'Boletas y cuentas por pagar', `Situación al ${hoy().split('-').reverse().join('-')}`);
  encabezado(ws, 4, ['Vencimiento', 'Categoría', 'Detalle', 'Monto', '¿Pagada?', 'Monto pagado', 'Último pago', 'Saldo pendiente', 'Situación']);
  const h = hoy();
  const bs = [...d.boletas].sort((a, b) => a.vencimiento.localeCompare(b.vencimiento));
  let r = 5;
  for (const b of bs) {
    const ult = [...b.pagos].sort((x, y) => y.fecha.localeCompare(x.fecha))[0];
    ws.getRow(r).values = [
      aFecha(b.vencimiento), nombreCategoria(d.settings, b.categoriaId), b.detalle, b.monto,
      b.estado === 'pagada' ? 'Sí' : b.estado === 'traspasada' ? 'Traspasada' : 'No',
      pagadoBoleta(b) || null, ult ? aFecha(ult.fecha) : null, saldoBoleta(b), situacionBoleta(b, h).texto,
    ];
    if (saldoBoleta(b) > 0 && b.vencimiento < h) ws.getRow(r).getCell(9).font = { color: { argb: 'FFBF312A' }, bold: true };
    r++;
  }
  ws.getRow(r).values = ['TOTAL', '', '', bs.reduce((s, b) => s + b.monto, 0), '', bs.reduce((s, b) => s + pagadoBoleta(b), 0), '', bs.reduce((s, b) => s + saldoBoleta(b), 0)];
  ws.getRow(r).font = { bold: true };
  formato(ws, [1, 7], FECHA, 5, r);
  formato(ws, [4, 6, 8], CLP, 5, r);
  if (bs.length) ws.autoFilter = { from: 'A4', to: `I${r - 1}` };
  anchos(ws, [12, 24, 40, 13, 11, 13, 12, 14, 48]);
}

function hojaDeudas(wb: ExcelJS.Workbook, d: DatosInforme) {
  const ws = wb.addWorksheet('Deudas');
  titulo(ws, 'Control de deudas y cuotas', "Estrategia 'avalancha': cuota mínima en todas y todo extra a la de mayor tasa.");
  encabezado(ws, 4, ['Acreedor', 'Tipo', 'Categoría', 'Cuota mensual', 'N° cuotas', 'Primera cuota', 'Última cuota', 'Tasa mensual', 'Restante', 'Notas']);
  let r = 5;
  const desde = d.proyeccion.meses[0];
  for (const x of d.deudas) {
    const fin = ultimoMesDeuda(x);
    ws.getRow(r).values = [
      x.acreedor, TIPOS_DEUDA[x.tipo], nombreCategoria(d.settings, x.categoriaId), x.montoCuota, x.numCuotas ?? 'Sin término',
      aMes(x.primerMes), fin ? aMes(fin) : null, x.tasaMensual ?? null, restanteDeuda(x, desde) ?? 'Sin término', x.notas ?? '',
    ];
    r++;
  }
  formato(ws, [4, 9], CLP, 5, r);
  formato(ws, [6, 7], 'mmm-yyyy', 5, r);
  formato(ws, [8], PCT, 5, r);

  r += 2;
  ws.getRow(r).getCell(1).value = 'PROYECCIÓN DE CUOTAS';
  ws.getRow(r).getCell(1).font = { bold: true, color: { argb: VERDE } };
  r++;
  const p = d.proyeccion;
  encabezado(ws, r, ['Acreedor / Mes', ...p.meses.map(nombreMesCorto), 'Total período']);
  const ini = ++r;
  for (const f of p.filas) {
    ws.getRow(r).values = [f.deuda.acreedor, ...f.valores, f.total];
    r++;
  }
  ws.getRow(r).values = ['TOTAL CUOTAS DEL MES', ...p.totales, p.total];
  ws.getRow(r).font = { bold: true };
  ws.getRow(r).eachCell((c) => (c.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: VERDE_SUAVE } }));
  formato(ws, p.meses.map((_, i) => i + 2).concat(p.meses.length + 2), CLP, ini, r);
  r++;
  ws.getRow(r).values = ['% del ingreso mensual', ...p.meses.map((m, i) => {
    const ing = totalIngresos(d.settings, d.ingresos, m);
    return ing ? p.totales[i] / ing : 0;
  })];
  formato(ws, p.meses.map((_, i) => i + 2), PCT, r, r);
  p.meses.forEach((m, i) => {
    const ing = totalIngresos(d.settings, d.ingresos, m);
    if (ing && p.totales[i] / ing > 0.3) ws.getRow(r).getCell(i + 2).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFCEFD9' } };
  });
  r += 2;
  ws.getRow(r).getCell(1).value = 'Si un mes supera ~30% del ingreso, prepárate con anticipación.';
  ws.getRow(r).getCell(1).font = { italic: true, size: 9 };

  // Cuotas pagadas en el período
  r += 2;
  ws.getRow(r).getCell(1).value = 'CUOTAS PAGADAS EN EL PERÍODO';
  ws.getRow(r).getCell(1).font = { bold: true, color: { argb: VERDE } };
  r++;
  encabezado(ws, r, ['Acreedor', 'Cuota', 'Mes de la cuota', 'Fecha de pago', 'Monto']);
  const ini2 = ++r;
  for (const x of d.deudas) {
    for (const [mes, pago] of Object.entries(x.pagos || {}).sort()) {
      if (mes < d.desde || mes > d.hasta) continue;
      ws.getRow(r).values = [x.acreedor, etiquetaCuota(x, mes), aMes(mes), aFecha(pago.fecha), pago.monto];
      r++;
    }
  }
  formato(ws, [3], 'mmm-yyyy', ini2, r);
  formato(ws, [4], FECHA, ini2, r);
  formato(ws, [5], CLP, ini2, r);
  anchos(ws, [32, 18, 22, ...Array(p.meses.length).fill(12), 14]);
  ws.getColumn(2).width = 18;
}

export async function generarExcel(d: DatosInforme): Promise<Blob> {
  const wb = new ExcelJS.Workbook();
  wb.creator = 'Finanzas Familia';
  wb.created = d.generado;
  if (d.meses.length === 1) {
    hojaResumen(wb, d, d.resumenes[0], 'Presupuesto');
  } else {
    hojaAnual(wb, d);
    for (const r of d.resumenes.slice(-24)) hojaResumen(wb, d, r, `Mes ${nombreMesCorto(r.mes)}`);
  }
  hojaRegistro(wb, d);
  hojaIngresos(wb, d);
  hojaBoletas(wb, d);
  hojaDeudas(wb, d);
  wb.eachSheet((ws) => (ws.properties.tabColor = { argb: GRIS }));
  const buf = await wb.xlsx.writeBuffer();
  return new Blob([buf], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
}
