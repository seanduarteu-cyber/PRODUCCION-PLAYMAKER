// Cálculos del presupuesto. Replican la lógica de la planilla
// PRESUPUESTO_CASA (hojas Presupuesto, Boletas y Deudas).
import { SIN_CATEGORIA } from './defaults';
import { diasEntre, fmtCLP, mesDe, mesesEntre, sumarMeses } from './format';
import type {
  Boleta, Categoria, Deuda, Fecha, Gasto, Ingreso, IngresoFijo, MesKey, Settings, Tipo,
} from './types';
import { TIPOS } from './types';

export type Nivel = 'ok' | 'warn' | 'danger' | 'muted';

// ---------- Deudas y cuotas ----------

/** Cuota que corresponde pagar en `mes` (0 si no hay). */
export function cuotaDeuda(d: Deuda, mes: MesKey): number {
  if (mes < d.primerMes) return 0;
  if (d.cerradaDesde && mes >= d.cerradaDesde) return 0;
  if (d.ajustes && Object.prototype.hasOwnProperty.call(d.ajustes, mes)) return d.ajustes[mes] || 0;
  const k = mesesEntre(d.primerMes, mes) + 1;
  if (d.numCuotas != null && k > d.numCuotas) return 0;
  return d.montoCuota || 0;
}

/** Número de cuota (1..n) en `mes`, o null si está fuera del plan. */
export function numeroCuota(d: Deuda, mes: MesKey): number | null {
  if (mes < d.primerMes) return null;
  const k = mesesEntre(d.primerMes, mes) + 1;
  if (d.numCuotas != null && k > d.numCuotas) return null;
  return k;
}

export function ultimoMesDeuda(d: Deuda): MesKey | null {
  let fin: MesKey | null = d.numCuotas != null ? sumarMeses(d.primerMes, d.numCuotas - 1) : null;
  if (fin && d.ajustes) {
    for (const [m, v] of Object.entries(d.ajustes)) if (v > 0 && m > fin) fin = m;
  }
  if (d.cerradaDesde) {
    const antes = sumarMeses(d.cerradaDesde, -1);
    if (!fin || antes < fin) fin = antes;
  }
  return fin;
}

export function etiquetaCuota(d: Deuda, mes: MesKey): string {
  const k = numeroCuota(d, mes);
  if (k == null) return '';
  return d.numCuotas != null ? `Cuota ${k} de ${d.numCuotas}` : `Cuota ${k}`;
}

/** Lo que falta pagar desde `desde` (incluido) en adelante. null = sin término. */
export function restanteDeuda(d: Deuda, desde: MesKey): number | null {
  const fin = ultimoMesDeuda(d);
  if (fin == null) return null;
  let total = 0;
  for (let m = desde < d.primerMes ? d.primerMes : desde; m <= fin; m = sumarMeses(m, 1)) {
    const c = cuotaDeuda(d, m);
    const pagado = d.pagos?.[m]?.monto ?? 0;
    total += Math.max(0, c - pagado);
  }
  return total;
}

export function totalCuotasMes(deudas: Deuda[], mes: MesKey): { total: number; pagado: number; pendientes: Deuda[] } {
  let total = 0;
  let pagado = 0;
  const pendientes: Deuda[] = [];
  for (const d of deudas) {
    const c = cuotaDeuda(d, mes);
    const p = d.pagos?.[mes]?.monto ?? 0;
    total += c;
    pagado += p;
    if (c > 0 && !d.pagos?.[mes]) pendientes.push(d);
  }
  return { total, pagado, pendientes };
}

export interface Proyeccion {
  meses: MesKey[];
  filas: { deuda: Deuda; valores: number[]; total: number }[];
  totales: number[];
  total: number;
}

export function proyeccion(deudas: Deuda[], desde: MesKey, n = 12): Proyeccion {
  const meses = Array.from({ length: n }, (_, i) => sumarMeses(desde, i));
  const filas = deudas.map((deuda) => {
    const valores = meses.map((m) => cuotaDeuda(deuda, m));
    return { deuda, valores, total: valores.reduce((a, b) => a + b, 0) };
  }).filter((f) => f.total > 0);
  const totales = meses.map((_, i) => filas.reduce((s, f) => s + f.valores[i], 0));
  return { meses, filas, totales, total: totales.reduce((a, b) => a + b, 0) };
}

/** Meses para pagar un saldo con tasa mensual y cuota fija (NPER). */
export function mesesParaPagar(saldo: number, tasa: number, cuota: number): number | null {
  if (saldo <= 0) return 0;
  if (cuota <= 0) return null;
  if (!tasa) return Math.ceil(saldo / cuota);
  if (cuota <= saldo * tasa) return null; // la cuota no cubre el interés
  return Math.ceil(-Math.log(1 - (tasa * saldo) / cuota) / Math.log(1 + tasa));
}

// ---------- Boletas ----------

export const pagadoBoleta = (b: Boleta) => (b.pagos || []).reduce((s, p) => s + (p.monto || 0), 0);

export function saldoBoleta(b: Boleta): number {
  if (b.estado !== 'pendiente') return 0;
  return Math.max(0, (b.monto || 0) - pagadoBoleta(b));
}

export function situacionBoleta(b: Boleta, hoyF: Fecha): { texto: string; nivel: Nivel } {
  if (b.estado === 'pagada') return { texto: 'Pagada', nivel: 'ok' };
  if (b.estado === 'traspasada') return { texto: 'Traspasada (boleta nueva o convenio)', nivel: 'muted' };
  const saldo = saldoBoleta(b);
  const partes: string[] = [];
  let nivel: Nivel = 'muted';
  if (pagadoBoleta(b) > 0) {
    partes.push(`Pago parcial: faltan ${fmtCLP(saldo)}`);
    nivel = 'warn';
  }
  const dias = diasEntre(b.vencimiento, hoyF);
  if (dias > 0) {
    partes.push(`VENCIDA hace ${dias} ${dias === 1 ? 'día' : 'días'}: pedir monto actualizado`);
    nivel = 'danger';
  } else if (dias === 0) {
    partes.push('Vence hoy');
    nivel = 'danger';
  } else if (dias >= -5) {
    partes.push(`Vence en ${-dias} ${dias === -1 ? 'día' : 'días'}`);
    if (nivel === 'muted') nivel = 'warn';
  } else if (!partes.length) {
    partes.push('Pendiente');
  }
  return { texto: partes.join(' · '), nivel };
}

export function resumenBoletas(boletas: Boleta[], hoyF: Fecha) {
  let pendiente = 0;
  let vencido = 0;
  let vencidas = 0;
  for (const b of boletas) {
    const s = saldoBoleta(b);
    pendiente += s;
    if (s > 0 && b.vencimiento < hoyF) {
      vencido += s;
      vencidas++;
    }
  }
  return { pendiente, vencido, vencidas };
}

// ---------- Ingresos ----------

export const montoIngresoFijo = (i: IngresoFijo, mes: MesKey) =>
  i.ajustes && Object.prototype.hasOwnProperty.call(i.ajustes, mes) ? i.ajustes[mes] : i.monto || 0;

export function totalIngresos(settings: Settings, ingresos: Ingreso[], mes: MesKey): number {
  const fijos = settings.ingresosFijos.reduce((s, i) => s + montoIngresoFijo(i, mes), 0);
  const extra = ingresos.filter((i) => mesDe(i.fecha) === mes).reduce((s, i) => s + (i.monto || 0), 0);
  return fijos + extra;
}

// ---------- Resumen del mes ----------

export interface FilaCategoria {
  categoria: Categoria;
  /** Presupuesto + cuotas proyectadas; null si no tiene ninguno. */
  presupuestado: number | null;
  cuotas: number;
  pagado: number;
  porPagar: number;
  total: number;
  esperado: number;
  diferencia: number | null;
  pctIngreso: number;
}

export interface Distribucion {
  tipo: Tipo;
  esperado: number;
  pct: number;
  meta: number;
  fuera: boolean;
  estado: string;
}

export interface ResumenMes {
  mes: MesKey;
  ingresos: number;
  filas: FilaCategoria[];
  totales: { presupuestado: number; pagado: number; porPagar: number; total: number; esperado: number };
  saldoHoy: number;
  saldoProyectado: number;
  estado: { texto: string; nivel: Nivel };
  distribucion: Distribucion[];
  atrasadas: number;
  sinPresupuesto: number;
  ingresoMenosPresupuestado: number;
  cuotas: { total: number; pagado: number; pendientes: Deuda[] };
}

/** ¿Este gasto es el pago de una cuota registrada en una deuda vigente? */
export function esPagoDeCuota(g: Gasto, deudasPorId: Map<string, Deuda>): boolean {
  if (!g.deudaId || !g.cuotaMes) return false;
  const d = deudasPorId.get(g.deudaId);
  return !!d && d.pagos?.[g.cuotaMes]?.gastoId === g.id;
}

export function categoriaVirtual(): Categoria {
  return { id: SIN_CATEGORIA, nombre: 'Sin categoría', tipo: 'Prescindible', presupuesto: null };
}

export function resumenMes(args: {
  settings: Settings;
  mes: MesKey;
  gastos: Gasto[];
  ingresos: Ingreso[];
  boletas: Boleta[];
  deudas: Deuda[];
}): ResumenMes {
  const { settings, mes, gastos, ingresos, boletas, deudas } = args;
  const totalIng = totalIngresos(settings, ingresos, mes);
  const cats = [...settings.categorias];
  const ids = new Set(cats.map((c) => c.id));
  const deudasPorId = new Map(deudas.map((d) => [d.id, d]));

  const catDe = (id: string) => (ids.has(id) ? id : SIN_CATEGORIA);
  const pagado = new Map<string, number>();
  const porPagar = new Map<string, number>();
  const cuotas = new Map<string, number>();
  const add = (m: Map<string, number>, k: string, v: number) => m.set(k, (m.get(k) || 0) + v);

  for (const g of gastos) {
    if (mesDe(g.fecha) !== mes) continue;
    if (esPagoDeCuota(g, deudasPorId)) continue; // se cuenta en el mes de la cuota (abajo)
    add(pagado, catDe(g.categoriaId), g.monto || 0);
  }
  for (const d of deudas) {
    const c = catDe(d.categoriaId);
    add(cuotas, c, cuotaDeuda(d, mes));
    const p = d.pagos?.[mes];
    if (p) add(pagado, c, p.monto || 0);
  }
  let atrasadas = 0;
  for (const b of boletas) {
    const s = saldoBoleta(b);
    if (!s) continue;
    const mb = mesDe(b.vencimiento);
    if (mb <= mes) add(porPagar, catDe(b.categoriaId), s);
    if (mb < mes) atrasadas += s;
  }
  const usados = [...pagado.keys(), ...porPagar.keys(), ...cuotas.keys()];
  if (usados.includes(SIN_CATEGORIA)) cats.push(categoriaVirtual());

  const filas: FilaCategoria[] = cats.map((categoria) => {
    const cu = cuotas.get(categoria.id) || 0;
    const presupuestado = categoria.presupuesto == null && !cu ? null : (categoria.presupuesto || 0) + cu;
    const pg = pagado.get(categoria.id) || 0;
    const pp = porPagar.get(categoria.id) || 0;
    const total = pg + pp;
    const esperado = Math.max(presupuestado || 0, total);
    return {
      categoria,
      presupuestado,
      cuotas: cu,
      pagado: pg,
      porPagar: pp,
      total,
      esperado,
      diferencia: presupuestado == null ? null : presupuestado - total,
      pctIngreso: totalIng ? esperado / totalIng : 0,
    };
  });

  const sum = (f: (x: FilaCategoria) => number) => filas.reduce((s, x) => s + f(x), 0);
  const totales = {
    presupuestado: sum((f) => f.presupuestado || 0),
    pagado: sum((f) => f.pagado),
    porPagar: sum((f) => f.porPagar),
    total: sum((f) => f.total),
    esperado: sum((f) => f.esperado),
  };
  const saldoProyectado = totalIng - totales.esperado;
  let estado: { texto: string; nivel: Nivel };
  if (totalIng === 0) estado = { texto: 'Ingresa tus ingresos', nivel: 'muted' };
  else if (saldoProyectado < 0) estado = { texto: 'Déficit', nivel: 'danger' };
  else if (saldoProyectado < totalIng * 0.05) estado = { texto: 'Ajustado (<5%)', nivel: 'warn' };
  else estado = { texto: 'Superávit', nivel: 'ok' };

  const distribucion: Distribucion[] = TIPOS.map((tipo) => {
    const esperado = filas.filter((f) => f.categoria.tipo === tipo).reduce((s, f) => s + f.esperado, 0);
    const pct = totalIng ? esperado / totalIng : 0;
    const meta = settings.metas?.[tipo] ?? 0;
    const fuera = tipo === 'Ahorro' ? pct < meta : pct > meta;
    return { tipo, esperado, pct, meta, fuera, estado: fuera ? (tipo === 'Ahorro' ? 'Bajo la meta' : 'Sobre la meta') : 'OK' };
  });

  return {
    mes,
    ingresos: totalIng,
    filas,
    totales,
    saldoHoy: totalIng - totales.pagado,
    saldoProyectado,
    estado,
    distribucion,
    atrasadas,
    sinPresupuesto: filas.filter((f) => !f.presupuestado).reduce((s, f) => s + f.total, 0),
    ingresoMenosPresupuestado: totalIng - totales.presupuestado,
    cuotas: totalCuotasMes(deudas, mes),
  };
}

export function nombreCategoria(settings: Settings, id: string): string {
  return settings.categorias.find((c) => c.id === id)?.nombre ?? 'Sin categoría';
}

export function tipoCategoria(settings: Settings, id: string): Tipo | '' {
  return settings.categorias.find((c) => c.id === id)?.tipo ?? '';
}
