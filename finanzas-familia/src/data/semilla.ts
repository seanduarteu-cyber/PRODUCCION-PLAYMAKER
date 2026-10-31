// Datos de EJEMPLO para la vista previa (familia ficticia). Solo se usa en la
// compilación de vista previa (VITE_VISTA_PREVIA) y en modo demostración.
import { cuotaDeuda } from '../lib/calc';
import { claveGuardada, derivarLlave } from '../lib/crypto';
import { hoy, mesActual, sumarMeses } from '../lib/format';
import type { AppUser, Boleta, Deuda, FamilyDoc, Settings } from '../lib/types';
import { crearAcciones } from './acciones';
import type { Backend } from './backend';
import { crearFamiliaCifrada } from './familias';

const LS = 'ff_semilla_v1';

function usuarioActual(backend: Backend): Promise<AppUser | null> {
  return new Promise((res) => {
    let off: (() => void) | null = null;
    off = backend.onAuth((u) => {
      res(u);
      setTimeout(() => off?.(), 0);
    });
  });
}

function leerFamilia(backend: Backend, fid: string): Promise<FamilyDoc> {
  return new Promise((res, rej) => {
    let off: (() => void) | null = null;
    off = backend.watchFamily(fid, (f) => {
      if (f) {
        res(f);
        setTimeout(() => off?.(), 0);
      }
    }, rej);
  });
}

export async function sembrarEjemplo(backend: Backend) {
  try {
    if (localStorage.getItem(LS)) return;
    localStorage.setItem(LS, '1');
  } catch {
    return;
  }
  const mes = mesActual();
  const dia = (d: number, m = mes) => `${m}-${String(d).padStart(2, '0')}`;
  const hoyDia = Number(hoy().slice(8, 10));
  const d = (n: number) => dia(Math.max(1, Math.min(hoyDia, n)));

  await backend.signUp('Ana (ejemplo)', 'ana@ejemplo.cl', 'demo');
  const ana = (await usuarioActual(backend))!;
  const { id: fid, clave } = await crearFamiliaCifrada(backend, ana, 'Familia de ejemplo');
  const inv = await backend.createInvite(ana, { id: fid, nombre: 'Familia de ejemplo' }, 'admin');

  const doc = await leerFamilia(backend, fid);
  const llave = await derivarLlave(claveGuardada(fid) || clave, doc.cifrado.sal);
  const presupuestos: Record<string, number> = {
    arriendo: 450000, luz: 45000, agua: 25000, gas: 35000, internet: 22000, celular: 30000, supermercado: 320000,
    frutas: 80000, carnes: 90000, transporte: 60000, salud: 50000, educacion: 120000, 'comida-fuera': 40000,
    suscripciones: 15000, emergencia: 100000,
  };
  const { settingsIniciales } = await import('../lib/defaults');
  const settings: Settings = settingsIniciales();
  settings.categorias = settings.categorias.map((c) => ({ ...c, presupuesto: presupuestos[c.id] ?? null }));
  settings.ingresosFijos = [
    { id: 'sueldo-1', nombre: 'Sueldo principal', monto: 1250000 },
    { id: 'sueldo-2', nombre: 'Sueldo pareja / secundario', monto: 680000 },
  ];

  const ctx = { backend, familyId: fid, llave, user: ana, boletas: [] as Boleta[], deudas: [] as Deuda[], onError: console.error };
  let acc = crearAcciones(ctx);
  await acc.guardarSettings(settings);

  const g = (fecha: string, categoriaId: string, monto: number, descripcion: string, medioPago?: string) =>
    acc.guardarGasto(acc.nuevoGasto({ fecha, categoriaId, monto, descripcion, medioPago }));
  await g(d(1), 'arriendo', 450000, 'Arriendo depto', 'Transferencia');
  await g(d(2), 'supermercado', 86450, 'Compra del mes', 'Débito');
  await g(d(4), 'transporte', 25000, 'Bencina', 'Débito');
  await g(d(5), 'internet', 22000, 'Plan hogar', 'Débito');
  await g(d(9), 'carnes', 23800, 'Carnicería', 'Efectivo');
  await g(d(12), 'suscripciones', 8990, 'Streaming', 'Crédito');
  await g(d(16), 'salud', 14200, 'Farmacia', 'Débito');
  await g(d(20), 'comida-fuera', 18500, 'Pizza viernes', 'Crédito');

  const en4 = new Date();
  en4.setDate(en4.getDate() + 4);
  const b1 = await acc.guardarBoleta({ vencimiento: hoy(en4), categoriaId: 'luz', detalle: 'Periodo del mes anterior', monto: 41870 });
  const b2 = await acc.guardarBoleta({ vencimiento: d(Math.max(1, hoyDia - 6)), categoriaId: 'agua', detalle: 'Incluye saldo anterior', monto: 31240 });
  const b3 = await acc.guardarBoleta({ vencimiento: d(10), categoriaId: 'gas', detalle: 'Gas cañería', monto: 28900 });
  ctx.boletas = [b1, b2, b3];
  acc = crearAcciones(ctx);
  await acc.pagarBoleta(b3, { fecha: d(8), monto: 28900, medioPago: 'Débito', cerrar: true });

  const tv = await acc.guardarDeuda({
    acreedor: 'Televisor (compra en cuotas)', tipo: 'compra_cuotas', categoriaId: 'otros', montoCuota: 45000, numCuotas: 6,
    primerMes: sumarMeses(mes, -2), montoTotal: 270000,
  });
  const credito = await acc.guardarDeuda({
    acreedor: 'Crédito de consumo', tipo: 'credito', categoriaId: 'cuotas', montoCuota: 85000, numCuotas: 24,
    primerMes: sumarMeses(mes, -5), tasaMensual: 0.018, montoTotal: 1650000,
  });
  const convenio = await acc.guardarDeuda({
    acreedor: 'Convenio agua', tipo: 'convenio', categoriaId: 'cuotas', montoCuota: 18000, numCuotas: 8, primerMes: mes,
  });
  ctx.deudas = [tv, credito, convenio];
  acc = crearAcciones(ctx);
  await acc.pagarCuota(credito, mes, { fecha: d(5), monto: cuotaDeuda(credito, mes), medioPago: 'Transferencia' });

  // La pareja se une con la invitación y registra sus gastos
  await backend.signUp('Pedro (ejemplo)', 'pedro@ejemplo.cl', 'demo');
  const pedro = (await usuarioActual(backend))!;
  await backend.joinFamily(pedro, inv.codigo);
  const accP = crearAcciones({ ...ctx, user: pedro });
  const gp = (fecha: string, categoriaId: string, monto: number, descripcion: string, medioPago?: string) =>
    accP.guardarGasto(accP.nuevoGasto({ fecha, categoriaId, monto, descripcion, medioPago }));
  await gp(d(3), 'frutas', 15600, 'Feria del sábado', 'Efectivo');
  await gp(d(7), 'educacion', 120000, 'Mensualidad jardín', 'Transferencia');
  await gp(d(14), 'supermercado', 42300, 'Reposición semana', 'Débito');
  await gp(d(18), 'celular', 30000, 'Plan móvil', 'Crédito');
  await gp(d(hoyDia), 'frutas', 9800, 'Verdulería', 'Efectivo');
  await accP.guardarIngreso({ fecha: d(15), descripcion: 'Venta bicicleta usada', monto: 60000 });

  await backend.signOut();
  await backend.signIn('ana@ejemplo.cl', 'demo');
}
