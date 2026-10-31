import type { Fecha, MesKey } from './types';

const clp = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 });
const num = new Intl.NumberFormat('es-CL', { maximumFractionDigits: 0 });
const pct = new Intl.NumberFormat('es-CL', { style: 'percent', maximumFractionDigits: 1 });

export const fmtCLP = (n: number) => {
  const r = Math.round(n || 0);
  return (r < 0 ? '-' : '') + clp.format(Math.abs(r));
};
export const fmtNum = (n: number) => num.format(Math.round(n || 0));
export const fmtPct = (n: number) => pct.format(Number.isFinite(n) ? n : 0);

/** Convierte "$ 1.234.567" o "1234567" a número. */
export function parseMonto(s: string): number {
  const neg = s.trim().startsWith('-');
  const digits = s.replace(/[^0-9]/g, '');
  if (!digits) return 0;
  const n = parseInt(digits, 10);
  return neg ? -n : n;
}

const pad = (n: number) => String(n).padStart(2, '0');

export function hoy(d: Date = new Date()): Fecha {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

export function mesDe(fecha: Fecha): MesKey {
  return fecha.slice(0, 7);
}

export function mesActual(d: Date = new Date()): MesKey {
  return mesDe(hoy(d));
}

export function sumarMeses(mes: MesKey, n: number): MesKey {
  const [y, m] = mes.split('-').map(Number);
  const total = y * 12 + (m - 1) + n;
  return `${Math.floor(total / 12)}-${pad((total % 12) + 1)}`;
}

/** Meses desde a hasta b (b - a). */
export function mesesEntre(a: MesKey, b: MesKey): number {
  const [ya, ma] = a.split('-').map(Number);
  const [yb, mb] = b.split('-').map(Number);
  return (yb * 12 + mb) - (ya * 12 + ma);
}

export function rangoMeses(desde: MesKey, hasta: MesKey): MesKey[] {
  const out: MesKey[] = [];
  for (let m = desde; m <= hasta; m = sumarMeses(m, 1)) out.push(m);
  return out;
}

export function primerDia(mes: MesKey): Fecha {
  return `${mes}-01`;
}

export function ultimoDia(mes: MesKey): Fecha {
  const [y, m] = mes.split('-').map(Number);
  const d = new Date(y, m, 0).getDate();
  return `${mes}-${pad(d)}`;
}

const MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
const MESES_CORTO = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
const DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];

const cap = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

export function nombreMes(mes: MesKey): string {
  const [y, m] = mes.split('-').map(Number);
  return `${cap(MESES[m - 1])} ${y}`;
}

export function nombreMesCorto(mes: MesKey): string {
  const [y, m] = mes.split('-').map(Number);
  return `${cap(MESES_CORTO[m - 1])} ${String(y).slice(2)}`;
}

export function fmtFecha(f: Fecha): string {
  if (!f) return '';
  const [y, m, d] = f.split('-');
  return `${d}-${m}-${y}`;
}

export function fmtFechaLarga(f: Fecha): string {
  const [y, m, d] = f.split('-').map(Number);
  const date = new Date(y, m - 1, d);
  return `${cap(DIAS[date.getDay()])} ${d} de ${MESES[m - 1]}`;
}

/** Días entre dos fechas (b - a). */
export function diasEntre(a: Fecha, b: Fecha): number {
  const [ya, ma, da] = a.split('-').map(Number);
  const [yb, mb, db] = b.split('-').map(Number);
  return Math.round((Date.UTC(yb, mb - 1, db) - Date.UTC(ya, ma - 1, da)) / 86400000);
}

export function normalizar(s: string): string {
  return s.normalize('NFD').replace(/[̀-ͯ]/g, '').trim().toLowerCase().replace(/\s+/g, ' ');
}
