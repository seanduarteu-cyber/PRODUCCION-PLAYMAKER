import { describe, expect, it } from 'vitest';
import {
  cuotaDeuda, etiquetaCuota, mesesParaPagar, proyeccion, restanteDeuda, resumenBoletas,
  resumenMes, saldoBoleta, situacionBoleta, totalIngresos,
} from '../src/lib/calc';
import { settingsIniciales } from '../src/lib/defaults';
import { mesesEntre, parseMonto, sumarMeses, ultimoDia } from '../src/lib/format';
import type { Boleta, Deuda, Gasto, Settings } from '../src/lib/types';

const audit = { creadoPor: 'u1', creadoPorNombre: 'Ana', creadoEn: 0 };

function settingsEjemplo(): Settings {
  const s = settingsIniciales();
  const presupuestos: Record<string, number> = {
    arriendo: 500000, luz: 80000, agua: 80000, gas: 80000, internet: 26000, celular: 150000,
    supermercado: 300000, frutas: 150000, carnes: 150000, transporte: 50000, salud: 100000,
    educacion: 260000, suscripciones: 15000,
  };
  s.categorias = s.categorias.map((c) => ({ ...c, presupuesto: presupuestos[c.id] ?? null }));
  s.ingresosFijos = [{ id: 'sueldo', nombre: 'Sueldo', monto: 1000000 }];
  return s;
}

const gasto = (id: string, fecha: string, categoriaId: string, monto: number, extra: Partial<Gasto> = {}): Gasto => ({
  id, fecha, categoriaId, monto, descripcion: '', ...audit, ...extra,
});
const boleta = (id: string, vencimiento: string, categoriaId: string, monto: number, extra: Partial<Boleta> = {}): Boleta => ({
  id, vencimiento, categoriaId, monto, detalle: '', estado: 'pendiente', pagos: [], ...audit, ...extra,
});
const deuda = (id: string, montoCuota: number, numCuotas: number | null, primerMes: string, extra: Partial<Deuda> = {}): Deuda => ({
  id, acreedor: id, tipo: 'otro', categoriaId: 'cuotas', montoCuota, numCuotas, primerMes, ajustes: {}, pagos: {}, ...audit, ...extra,
});

const gastos = [gasto('g1', '2026-10-30', 'supermercado', 66000), gasto('g2', '2026-10-30', 'ocio', 17000)];
const boletas = [
  boleta('b1', '2026-11-12', 'luz', 185590),
  boleta('b2', '2026-10-30', 'agua', 232900),
  boleta('b3', '2026-10-21', 'gas', 583169),
];
const deudas = [
  deuda('convenio', 74867, null, '2026-11'),
  deuda('asistente', 50000, 1, '2026-11'),
  deuda('prestamo', 117000, 11, '2026-11'),
  deuda('otro', 1000000, 1, '2026-11'),
];

describe('formato y meses', () => {
  it('suma y resta meses', () => {
    expect(sumarMeses('2026-11', 2)).toBe('2027-01');
    expect(sumarMeses('2026-01', -1)).toBe('2025-12');
    expect(mesesEntre('2026-11', '2027-09')).toBe(10);
    expect(ultimoDia('2028-02')).toBe('2028-02-29');
  });
  it('lee montos en formato chileno', () => {
    expect(parseMonto('$ 1.234.567')).toBe(1234567);
    expect(parseMonto('')).toBe(0);
  });
});

describe('resumen del mes (igual que la planilla)', () => {
  const settings = settingsEjemplo();

  it('octubre: pagado, por pagar, gasto esperado y saldo proyectado', () => {
    const r = resumenMes({ settings, mes: '2026-10', gastos, ingresos: [], boletas, deudas });
    expect(r.ingresos).toBe(1000000);
    expect(r.totales.presupuestado).toBe(1941000);
    expect(r.totales.pagado).toBe(83000);
    expect(r.totales.porPagar).toBe(816069);
    expect(r.totales.esperado).toBe(2614069);
    expect(r.saldoProyectado).toBe(1000000 - 2614069);
    expect(r.estado.nivel).toBe('danger');
    const agua = r.filas.find((f) => f.categoria.id === 'agua')!;
    expect(agua.esperado).toBe(232900);
    expect(agua.diferencia).toBe(80000 - 232900);
    const ocio = r.filas.find((f) => f.categoria.id === 'ocio')!;
    expect(ocio.presupuestado).toBeNull();
    expect(r.sinPresupuesto).toBe(17000);
    const esencial = r.distribucion.find((d) => d.tipo === 'Esencial')!;
    expect(esencial.fuera).toBe(true);
  });

  it('noviembre: cuotas proyectadas entran en lo presupuestado y las boletas atrasadas se arrastran', () => {
    const r = resumenMes({ settings, mes: '2026-11', gastos, ingresos: [], boletas, deudas });
    const cuotas = r.filas.find((f) => f.categoria.id === 'cuotas')!;
    expect(cuotas.presupuestado).toBe(1241867);
    expect(r.cuotas.total).toBe(1241867);
    expect(r.totales.porPagar).toBe(185590 + 232900 + 583169);
    expect(r.atrasadas).toBe(232900 + 583169);
  });

  it('un pago de cuota se cuenta en el mes de la cuota, no en el de la fecha', () => {
    const pago = gasto('gp', '2026-10-31', 'cuotas', 117000, { deudaId: 'prestamo', cuotaMes: '2026-11' });
    const ds = deudas.map((d) => d.id === 'prestamo'
      ? { ...d, pagos: { '2026-11': { gastoId: 'gp', fecha: '2026-10-31', monto: 117000 } } }
      : d);
    const oct = resumenMes({ settings, mes: '2026-10', gastos: [...gastos, pago], ingresos: [], boletas, deudas: ds });
    expect(oct.totales.pagado).toBe(83000);
    const nov = resumenMes({ settings, mes: '2026-11', gastos: [pago], ingresos: [], boletas, deudas: ds });
    expect(nov.filas.find((f) => f.categoria.id === 'cuotas')!.pagado).toBe(117000);
    expect(nov.cuotas.pendientes.map((d) => d.id)).not.toContain('prestamo');
  });

  it('gastos con categoría eliminada aparecen en "Sin categoría"', () => {
    const r = resumenMes({ settings, mes: '2026-10', gastos: [gasto('x', '2026-10-02', 'borrada', 5000)], ingresos: [], boletas: [], deudas: [] });
    expect(r.filas.at(-1)!.categoria.nombre).toBe('Sin categoría');
    expect(r.totales.pagado).toBe(5000);
  });

  it('ingresos fijos con ajuste puntual + ingresos extra', () => {
    const s = settingsEjemplo();
    s.ingresosFijos[0].ajustes = { '2026-12': 1500000 };
    const extra = [{ id: 'i', fecha: '2026-12-15', descripcion: 'Bono', monto: 200000, ...audit }];
    expect(totalIngresos(s, extra, '2026-12')).toBe(1700000);
    expect(totalIngresos(s, extra, '2026-11')).toBe(1000000);
  });
});

describe('deudas y cuotas', () => {
  it('proyección de 14 meses coincide con la hoja Deudas', () => {
    const p = proyeccion(deudas, '2026-11', 14);
    expect(p.totales[0]).toBe(1241867);
    expect(p.totales.slice(1, 11)).toEqual(Array(10).fill(191867));
    expect(p.totales.slice(11)).toEqual([74867, 74867, 74867]);
    expect(p.total).toBe(3385138);
  });

  it('ajustes y cierre anticipado', () => {
    const d = deuda('d', 100, 12, '2026-01', { ajustes: { '2026-03': 150 }, cerradaDesde: '2026-06' });
    expect(cuotaDeuda(d, '2025-12')).toBe(0);
    expect(cuotaDeuda(d, '2026-03')).toBe(150);
    expect(cuotaDeuda(d, '2026-05')).toBe(100);
    expect(cuotaDeuda(d, '2026-06')).toBe(0);
    expect(restanteDeuda(d, '2026-04')).toBe(200);
    expect(etiquetaCuota(d, '2026-02')).toBe('Cuota 2 de 12');
  });

  it('restante descuenta cuotas pagadas y es null si no tiene término', () => {
    const d = deuda('d', 117000, 11, '2026-11', { pagos: { '2026-11': { gastoId: 'g', fecha: '2026-11-05', monto: 117000 } } });
    expect(restanteDeuda(d, '2026-11')).toBe(117000 * 10);
    expect(restanteDeuda(deudas[0], '2026-11')).toBeNull();
  });

  it('meses para pagar (NPER)', () => {
    expect(mesesParaPagar(1000, 0, 100)).toBe(10);
    expect(mesesParaPagar(1000, 0.02, 10)).toBeNull();
    expect(mesesParaPagar(100000, 0.02, 10000)).toBe(12);
  });
});

describe('boletas', () => {
  it('pago parcial, vencidas y traspasadas', () => {
    const b = boleta('b', '2026-10-21', 'gas', 583169, { pagos: [{ gastoId: 'g', fecha: '2026-10-25', monto: 83169 }] });
    expect(saldoBoleta(b)).toBe(500000);
    const s = situacionBoleta(b, '2026-10-31');
    expect(s.nivel).toBe('danger');
    expect(s.texto).toContain('VENCIDA hace 10 días');
    expect(s.texto).toContain('Pago parcial');
    expect(saldoBoleta({ ...b, estado: 'traspasada' })).toBe(0);
    expect(situacionBoleta(boleta('c', '2026-11-03', 'luz', 1), '2026-10-31').texto).toBe('Vence en 3 días');
    const r = resumenBoletas(boletas, '2026-10-31');
    expect(r.pendiente).toBe(185590 + 232900 + 583169);
    expect(r.vencidas).toBe(2);
    expect(r.vencido).toBe(232900 + 583169);
  });
});
