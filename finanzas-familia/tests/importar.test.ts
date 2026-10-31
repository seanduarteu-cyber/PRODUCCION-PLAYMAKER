import ExcelJS from 'exceljs';
import { describe, expect, it } from 'vitest';
import { resumenMes } from '../src/lib/calc';
import { settingsIniciales } from '../src/lib/defaults';
import { importarPlanilla } from '../src/lib/importar';

const d = (y: number, m: number, day: number) => new Date(Date.UTC(y, m - 1, day));

/** Planilla sintética con la misma estructura que PRESUPUESTO_CASA. */
async function planilla(): Promise<ArrayBuffer> {
  const wb = new ExcelJS.Workbook();
  const p = wb.addWorksheet('Presupuesto');
  p.getCell('A1').value = 'Presupuesto Familiar Mensual';
  p.getRow(4).values = ['INGRESOS', 'Monto mensual'];
  p.getRow(5).values = ['Sueldo principal', 900000];
  p.getRow(6).values = ['Sueldo pareja / secundario', 300000];
  p.getRow(7).values = ['TOTAL INGRESOS', { formula: 'SUM(B5:B6)', result: 1200000 }];
  p.getRow(11).values = ['GASTOS', 'Tipo', 'Presupuestado', 'Pagado'];
  p.getRow(12).values = ['Arriendo / dividendo', 'Esencial', 400000];
  p.getRow(13).values = ['supermercado', 'Esencial', 250000];
  p.getRow(14).values = ['Mascotas', 'Prescindible', 30000];
  p.getRow(15).values = ['Cuotas de deudas (según proyección)', 'Deudas', { formula: 'X', result: 0 }];
  p.getRow(16).values = ['TOTAL GASTOS'];

  const r = wb.addWorksheet('Registro');
  r.getRow(4).values = ['Fecha', 'Categoría', 'Descripción', 'Monto', 'Mes'];
  r.getRow(5).values = [d(2026, 10, 3), 'supermercado', 'compra semana', 45000];
  r.getRow(6).values = [d(2026, 10, 3), 'supermercado', 'compra semana', 45000];
  r.getRow(7).values = [d(2026, 10, 9), 'Veterinario', 'vacuna', 20000];

  const b = wb.addWorksheet('Boletas');
  b.getRow(4).values = ['Vencimiento', 'Categoría', 'Detalle', 'Monto', '¿Pagada?', 'Mes', 'Fecha de pago', 'Monto pagado'];
  b.getRow(5).values = [d(2026, 10, 15), 'Luz', 'octubre', 50000, 'Sí', null, d(2026, 10, 14), null];
  b.getRow(6).values = [d(2026, 10, 20), 'Agua', 'octubre', 30000, 'No', null, d(2026, 10, 18), 10000];
  b.getRow(7).values = [d(2026, 9, 20), 'Gas', 'septiembre', 40000, 'Traspasada'];

  const de = wb.addWorksheet('Deudas');
  de.getRow(4).values = ['Acreedor', 'Saldo pendiente', 'Tasa interés mensual', 'Cuota mensual'];
  de.getRow(5).values = ['Tarjeta de crédito', 500000, 0.025, 60000];
  de.getRow(13).values = ['Acreedor / Mes', d(2026, 11, 1), d(2026, 12, 1), d(2027, 1, 1), d(2027, 2, 1)];
  de.getRow(14).values = ['Convenio luz', 20000, 20000, 25000, 0];
  de.getRow(15).values = ['Crédito auto', 100000, 100000, 100000, 100000];
  de.getRow(16).values = [null, 0, 0, 0, 0];
  de.getRow(17).values = ['TOTAL CUOTAS DEL MES'];
  return (await wb.xlsx.writeBuffer()) as ArrayBuffer;
}

describe('importar planilla', () => {
  it('lee presupuesto, ingresos, gastos, boletas y deudas', async () => {
    const r = await importarPlanilla(await planilla(), settingsIniciales(), { uid: 'u1', nombre: 'Sean' });
    const cat = (n: string) => r.settings.categorias.find((c) => c.nombre === n);
    expect(cat('Arriendo / dividendo')?.presupuesto).toBe(400000);
    expect(cat('Supermercado')?.presupuesto).toBe(250000);
    expect(cat('Mascotas')?.tipo).toBe('Prescindible');
    expect(r.categoriasNuevas).toEqual(['Mascotas', 'Veterinario']);
    expect(r.settings.ingresosFijos.find((i) => i.nombre === 'Sueldo principal')?.monto).toBe(900000);

    // gastos: 3 del registro (ids distintos aunque se repitan) + 2 pagos de boletas
    expect(r.gastos).toHaveLength(5);
    expect(new Set(r.gastos.map((g) => g.id)).size).toBe(5);

    const luz = r.boletas.find((b) => b.detalle === 'octubre' && b.monto === 50000)!;
    expect(luz.estado).toBe('pagada');
    expect(luz.pagos[0]).toMatchObject({ fecha: '2026-10-14', monto: 50000 });
    const agua = r.boletas.find((b) => b.monto === 30000)!;
    expect(agua.estado).toBe('pendiente');
    expect(agua.pagos[0].monto).toBe(10000);
    expect(r.boletas.find((b) => b.monto === 40000)!.estado).toBe('traspasada');

    const conv = r.deudas.find((x) => x.acreedor === 'Convenio luz')!;
    expect(conv).toMatchObject({ primerMes: '2026-11', montoCuota: 20000, numCuotas: 3, ajustes: { '2027-01': 25000 } });
    const auto = r.deudas.find((x) => x.acreedor === 'Crédito auto')!;
    expect(auto.numCuotas).toBeNull();
    expect(r.avisos.some((a) => a.includes('Crédito auto'))).toBe(true);
    const tarjeta = r.deudas.find((x) => x.acreedor === 'Tarjeta de crédito')!;
    expect(tarjeta).toMatchObject({ montoCuota: 60000, tasaMensual: 0.025, montoTotal: 500000 });

    // el resumen de octubre usa todo lo importado
    const res = resumenMes({ settings: r.settings, mes: '2026-10', gastos: r.gastos, ingresos: [], boletas: r.boletas, deudas: r.deudas });
    expect(res.ingresos).toBe(1200000);
    expect(res.totales.pagado).toBe(45000 * 2 + 20000 + 50000 + 10000);
    expect(res.totales.porPagar).toBe(20000);
  });

  it('importar dos veces no duplica (mismos ids)', async () => {
    const buf = await planilla();
    const a = await importarPlanilla(buf, settingsIniciales(), { uid: 'u1', nombre: 'Sean' });
    const b = await importarPlanilla(buf, settingsIniciales(), { uid: 'u1', nombre: 'Sean' });
    expect(a.gastos.map((g) => g.id)).toEqual(b.gastos.map((g) => g.id));
    expect(a.deudas.map((g) => g.id)).toEqual(b.deudas.map((g) => g.id));
  });
});
