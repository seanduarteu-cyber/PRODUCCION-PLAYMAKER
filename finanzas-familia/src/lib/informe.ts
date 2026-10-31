// Datos comunes para los informes en Excel y PDF.
import { montoIngresoFijo, proyeccion, resumenMes, type Proyeccion, type ResumenMes } from './calc';
import { mesActual, mesDe, nombreMes, rangoMeses } from './format';
import type { Boleta, Deuda, Gasto, Ingreso, Member, MesKey, Settings } from './types';

export interface DatosInforme {
  familia: string;
  desde: MesKey;
  hasta: MesKey;
  meses: MesKey[];
  settings: Settings;
  gastos: Gasto[];
  ingresos: Ingreso[];
  boletas: Boleta[];
  deudas: Deuda[];
  members: Member[];
  resumenes: ResumenMes[];
  proyeccion: Proyeccion;
  generado: Date;
}

export function armarInforme(a: {
  familia: string; desde: MesKey; hasta: MesKey; settings: Settings; gastos: Gasto[]; ingresos: Ingreso[];
  boletas: Boleta[]; deudas: Deuda[]; members: Member[];
}): DatosInforme {
  const meses = rangoMeses(a.desde, a.hasta);
  const gastos = a.gastos.filter((g) => mesDe(g.fecha) >= a.desde && mesDe(g.fecha) <= a.hasta)
    .sort((x, y) => x.fecha.localeCompare(y.fecha) || x.creadoEn - y.creadoEn);
  const ingresos = a.ingresos.filter((i) => mesDe(i.fecha) >= a.desde && mesDe(i.fecha) <= a.hasta)
    .sort((x, y) => x.fecha.localeCompare(y.fecha));
  const resumenes = meses.map((mes) => resumenMes({ settings: a.settings, mes, gastos, ingresos, boletas: a.boletas, deudas: a.deudas }));
  return {
    ...a, meses, gastos, ingresos, resumenes,
    // La proyección parte en el mes actual si está dentro del período (lo pasado ya no se proyecta).
    proyeccion: proyeccion(a.deudas, inicioProyeccion(a.desde, a.hasta), 12),
    generado: new Date(),
  };
}

function inicioProyeccion(desde: MesKey, hasta: MesKey): MesKey {
  const actual = mesActual();
  if (actual < desde) return desde;
  if (actual > hasta) return desde;
  return actual;
}

export function tituloPeriodo(d: { desde: MesKey; hasta: MesKey }): string {
  if (d.desde === d.hasta) return nombreMes(d.desde);
  if (d.desde.endsWith('-01') && d.hasta.endsWith('-12') && d.desde.slice(0, 4) === d.hasta.slice(0, 4)) return `Año ${d.desde.slice(0, 4)}`;
  return `${nombreMes(d.desde)} a ${nombreMes(d.hasta)}`;
}

export function nombreArchivo(d: DatosInforme, ext: string): string {
  const limpio = d.familia.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Za-z0-9]+/g, '_').replace(/^_|_$/g, '');
  const per = d.desde === d.hasta ? d.desde : `${d.desde}_a_${d.hasta}`;
  return `Finanzas_${limpio || 'Familia'}_${per}.${ext}`;
}

/** Ingresos de cada mes: fijos (con ajustes) + extras. */
export function filasIngresos(d: DatosInforme) {
  const out: { mes: MesKey; tipo: 'Fijo' | 'Extra'; descripcion: string; fecha: string; monto: number; por: string }[] = [];
  for (const mes of d.meses) {
    for (const i of d.settings.ingresosFijos) {
      const m = montoIngresoFijo(i, mes);
      if (m) out.push({ mes, tipo: 'Fijo', descripcion: i.nombre, fecha: '', monto: m, por: '' });
    }
    for (const i of d.ingresos.filter((x) => mesDe(x.fecha) === mes)) {
      out.push({ mes, tipo: 'Extra', descripcion: i.descripcion || 'Ingreso extra', fecha: i.fecha, monto: i.monto, por: i.creadoPorNombre });
    }
  }
  return out;
}
