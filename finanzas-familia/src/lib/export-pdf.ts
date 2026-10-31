// Informe en PDF (A4) para imprimir o enviar.
import { jsPDF } from 'jspdf';
import autoTable, { type RowInput } from 'jspdf-autotable';
import { nombreCategoria, saldoBoleta, situacionBoleta } from './calc';
import { fmtCLP, fmtFecha, fmtPct, hoy, nombreMes, nombreMesCorto } from './format';
import { filasIngresos, tituloPeriodo, type DatosInforme } from './informe';

const VERDE: [number, number, number] = [14, 116, 88];
const ROJO: [number, number, number] = [191, 49, 42];
const GRIS: [number, number, number] = [95, 109, 103];

// La fuente estándar del PDF no tiene el signo menos tipográfico.
const $ = (n: number) => fmtCLP(n).replace(/−/g, '-').replace(/ /g, ' ');
const pct = (n: number) => fmtPct(n).replace(/ /g, ' ');

export async function generarPdf(d: DatosInforme): Promise<Blob> {
  const doc = new jsPDF({ unit: 'pt', format: 'a4' });
  const W = doc.internal.pageSize.getWidth();
  const M = 40;
  let y = M;

  const nuevaPaginaSiFalta = (alto: number) => {
    if (y + alto > doc.internal.pageSize.getHeight() - M) {
      doc.addPage();
      y = M;
    }
  };
  const seccion = (t: string) => {
    nuevaPaginaSiFalta(60);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(12);
    doc.setTextColor(...VERDE);
    doc.text(t, M, y);
    doc.setTextColor(0);
    y += 8;
  };
  const tabla = (head: string[], body: RowInput[], opts: { foot?: RowInput[]; derecha?: number[]; tam?: number } = {}) => {
    autoTable(doc, {
      startY: y,
      head: [head],
      body,
      foot: opts.foot,
      margin: { left: M, right: M },
      styles: { fontSize: opts.tam ?? 8.5, cellPadding: 3.5, overflow: 'linebreak' },
      headStyles: { fillColor: VERDE, textColor: 255, fontStyle: 'bold' },
      footStyles: { fillColor: [224, 242, 234], textColor: 20, fontStyle: 'bold' },
      alternateRowStyles: { fillColor: [246, 248, 247] },
      columnStyles: Object.fromEntries((opts.derecha ?? []).map((i) => [i, { halign: 'right' }])),
      showFoot: 'lastPage',
    });
    y = (doc as unknown as { lastAutoTable: { finalY: number } }).lastAutoTable.finalY + 18;
  };

  // Portada / encabezado
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(20);
  doc.setTextColor(...VERDE);
  doc.text('Finanzas Familia', M, y + 6);
  doc.setFontSize(13);
  doc.setTextColor(0);
  y += 28;
  doc.text(`${d.familia} · ${tituloPeriodo(d)}`, M, y);
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(...GRIS);
  y += 14;
  doc.text(`Generado el ${fmtFecha(hoy())} a las ${d.generado.toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit' })}`, M, y);
  doc.setTextColor(0);
  y += 22;

  // Resumen por mes (si hay más de uno)
  if (d.meses.length > 1) {
    seccion('Resumen por mes');
    tabla(['Mes', 'Ingresos', 'Pagado', 'Por pagar', 'Gasto esperado', 'Saldo proyectado', 'Estado'],
      d.resumenes.map((r) => [nombreMes(r.mes), $(r.ingresos), $(r.totales.pagado), $(r.totales.porPagar), $(r.totales.esperado), $(r.saldoProyectado), r.estado.texto]),
      {
        derecha: [1, 2, 3, 4, 5],
        foot: [['Total', $(d.resumenes.reduce((s, r) => s + r.ingresos, 0)), $(d.resumenes.reduce((s, r) => s + r.totales.pagado, 0)), '', $(d.resumenes.reduce((s, r) => s + r.totales.esperado, 0)), '', '']],
      });
  }

  // Detalle de cada mes (último mes primero si son muchos)
  const detalles = d.meses.length > 3 ? d.resumenes.slice(-1) : d.resumenes;
  for (const r of detalles) {
    seccion(`Presupuesto de ${nombreMes(r.mes).toLowerCase()}`);
    // tarjetas
    nuevaPaginaSiFalta(70);
    const kpis: [string, number][] = [
      ['Ingresos', r.ingresos], ['Ya pagado', r.totales.pagado], ['Por pagar', r.totales.porPagar], ['Gasto esperado', r.totales.esperado],
    ];
    const cw = (W - 2 * M - 3 * 8) / 4;
    kpis.forEach(([k, v], i) => {
      const x = M + i * (cw + 8);
      doc.setFillColor(241, 244, 242);
      doc.roundedRect(x, y, cw, 40, 5, 5, 'F');
      doc.setFontSize(8);
      doc.setTextColor(...GRIS);
      doc.text(k, x + 8, y + 14);
      doc.setFontSize(11.5);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(0);
      doc.text($(v), x + 8, y + 31);
      doc.setFont('helvetica', 'normal');
    });
    y += 54;
    doc.setFontSize(11);
    doc.setFont('helvetica', 'bold');
    doc.text('Saldo proyectado a fin de mes: ', M, y);
    const tw = doc.getTextWidth('Saldo proyectado a fin de mes: ');
    doc.setTextColor(...(r.saldoProyectado < 0 ? ROJO : VERDE));
    doc.text(`${$(r.saldoProyectado)}  (${r.estado.texto})`, M + tw, y);
    doc.setTextColor(0);
    doc.setFont('helvetica', 'normal');
    y += 14;

    const filas = r.filas.filter((f) => f.presupuestado || f.total);
    tabla(['Categoría', 'Tipo', 'Presupuestado', 'Pagado', 'Por pagar', 'Diferencia'],
      filas.map((f) => [
        f.categoria.nombre, f.categoria.tipo, f.presupuestado == null ? '-' : $(f.presupuestado), $(f.pagado), f.porPagar ? $(f.porPagar) : '-',
        { content: f.diferencia == null ? 'Sin presupuesto' : $(f.diferencia), styles: { textColor: f.diferencia != null && f.diferencia < 0 ? ROJO : 20 } },
      ]),
      { derecha: [2, 3, 4, 5], foot: [['Total', '', $(r.totales.presupuestado), $(r.totales.pagado), $(r.totales.porPagar), $(r.totales.presupuestado - r.totales.total)]] });

    tabla(['Distribución', 'Gasto esperado', '% del ingreso', 'Meta', 'Estado'],
      r.distribucion.map((x) => [x.tipo, $(x.esperado), pct(x.pct), pct(x.meta), x.estado]), { derecha: [1, 2, 3] });
  }

  // Ingresos
  const ing = filasIngresos(d);
  if (ing.length) {
    seccion('Ingresos');
    tabla(['Mes', 'Tipo', 'Descripción', 'Fecha', 'Monto'],
      ing.map((i) => [nombreMesCorto(i.mes), i.tipo, i.descripcion, i.fecha ? fmtFecha(i.fecha) : '', $(i.monto)]),
      { derecha: [4], foot: [['Total', '', '', '', $(ing.reduce((s, i) => s + i.monto, 0))]] });
  }

  // Gastos
  seccion(`Gastos registrados (${d.gastos.length})`);
  tabla(['Fecha', 'Categoría', 'Descripción', 'Por', 'Monto'],
    d.gastos.map((g) => [fmtFecha(g.fecha), nombreCategoria(d.settings, g.categoriaId), g.descripcion, g.creadoPorNombre.split(' ')[0], $(g.monto)]),
    { derecha: [4], tam: 8, foot: [['Total', '', '', '', $(d.gastos.reduce((s, g) => s + g.monto, 0))]] });

  // Boletas pendientes
  const h = hoy();
  const pend = d.boletas.filter((b) => saldoBoleta(b) > 0).sort((a, b) => a.vencimiento.localeCompare(b.vencimiento));
  if (pend.length) {
    seccion('Boletas por pagar');
    tabla(['Vencimiento', 'Categoría', 'Detalle', 'Saldo', 'Situación'],
      pend.map((b) => {
        const s = situacionBoleta(b, h);
        return [fmtFecha(b.vencimiento), nombreCategoria(d.settings, b.categoriaId), b.detalle, $(saldoBoleta(b)),
          { content: s.texto, styles: { textColor: s.nivel === 'danger' ? ROJO : 20 } }];
      }),
      { derecha: [3], foot: [['Total', '', '', $(pend.reduce((s, b) => s + saldoBoleta(b), 0)), '']] });
  }

  // Proyección de cuotas
  const p = d.proyeccion;
  if (p.filas.length) {
    seccion('Proyección de cuotas');
    const meses = p.meses.slice(0, 12);
    tabla(['Acreedor', ...meses.map(nombreMesCorto)],
      p.filas.map((f) => [f.deuda.acreedor, ...f.valores.slice(0, 12).map((v) => (v ? $(v).replace('$', '') : '-'))]),
      { derecha: meses.map((_, i) => i + 1), tam: 6.5, foot: [['Total', ...p.totales.slice(0, 12).map((v) => $(v).replace('$', ''))]] });
  }

  // Pie de página
  const n = doc.getNumberOfPages();
  for (let i = 1; i <= n; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setTextColor(...GRIS);
    doc.text(`${d.familia} · ${tituloPeriodo(d)}`, M, doc.internal.pageSize.getHeight() - 20);
    doc.text(`Página ${i} de ${n}`, W - M, doc.internal.pageSize.getHeight() - 20, { align: 'right' });
  }
  return doc.output('blob');
}
