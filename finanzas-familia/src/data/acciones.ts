// Operaciones del dominio. Todo se cifra con la llave de la familia antes de
// enviarse al servidor.
import { etiquetaCuota } from '../lib/calc';
import { cifrar, descifrar } from '../lib/crypto';
import { nuevoId } from '../lib/defaults';
import { mesDe, sumarMeses } from '../lib/format';
import type {
  AppUser, Boleta, ColeccionNombre, Deuda, Gasto, Ingreso, MesKey, RawDoc, Settings,
} from '../lib/types';
import type { Backend, WriteOp } from './backend';

type Base = { id: string; creadoPor: string; creadoEn: number };

export interface Contexto {
  backend: Backend;
  familyId: string;
  llave: CryptoKey;
  user: AppUser;
  boletas: Boleta[];
  deudas: Deuda[];
  /** Errores de escritura en segundo plano (sin permiso, etc.) */
  onError: (e: unknown) => void;
}

const COLECCION_CON_MES: Partial<Record<ColeccionNombre, (x: never) => MesKey>> = {
  gastos: (g: Gasto) => mesDe(g.fecha),
  ingresos: (i: Ingreso) => mesDe(i.fecha),
};

export async function aRaw(llave: CryptoKey, coll: ColeccionNombre, obj: Base): Promise<Omit<RawDoc, 'id'>> {
  const { id: _id, ...resto } = obj;
  void _id;
  const mesFn = COLECCION_CON_MES[coll] as ((x: Base) => MesKey) | undefined;
  return { enc: await cifrar(llave, resto), mes: mesFn ? mesFn(obj) : undefined, creadoPor: obj.creadoPor, creadoEn: obj.creadoEn };
}

const cache = new WeakMap<CryptoKey, Map<string, unknown>>();

export async function deRaw<T>(llave: CryptoKey, raw: RawDoc): Promise<T | null> {
  let c = cache.get(llave);
  if (!c) cache.set(llave, (c = new Map()));
  const k = raw.id + ':' + raw.enc;
  if (c.has(k)) return c.get(k) as T;
  try {
    const v = { ...(await descifrar<object>(llave, raw.enc)), id: raw.id } as T;
    c.set(k, v);
    return v;
  } catch {
    return null; // dato dañado o cifrado con otra clave
  }
}

export async function deRaws<T>(llave: CryptoKey, raws: RawDoc[]): Promise<T[]> {
  const out = await Promise.all(raws.map((r) => deRaw<T>(llave, r)));
  return out.filter((x): x is Awaited<T> => x != null) as T[];
}

export function crearAcciones(ctx: Contexto) {
  const { backend, familyId, llave, user } = ctx;

  const audit = () => ({ creadoPor: user.uid, creadoPorNombre: user.nombre, creadoEn: Date.now() });
  const set = async (coll: ColeccionNombre, obj: Base): Promise<WriteOp> => ({ op: 'set', coll, id: obj.id, data: await aRaw(llave, coll, obj) });
  const del = (coll: ColeccionNombre, id: string): WriteOp => ({ op: 'delete', coll, id });
  // No se espera la confirmación del servidor: Firestore muestra el cambio al
  // instante y lo sincroniza cuando haya internet.
  const commit = (ops: WriteOp[]) => {
    backend.commit(familyId, ops).catch(ctx.onError);
  };

  const boletaPorId = (id?: string) => (id ? ctx.boletas.find((b) => b.id === id) : undefined);
  const deudaPorId = (id?: string) => (id ? ctx.deudas.find((d) => d.id === id) : undefined);

  const pagadoDe = (b: Boleta) => b.pagos.reduce((s, p) => s + p.monto, 0);
  /** Si ya se pagó todo, queda como pagada. */
  function recalcularEstado(b: Boleta): Boleta {
    if (b.estado === 'pendiente' && b.monto > 0 && pagadoDe(b) >= b.monto) return { ...b, estado: 'pagada' };
    return b;
  }

  /** Mantiene sincronizada la boleta / deuda enlazada cuando cambia un gasto. */
  async function opsEnlace(g: Gasto, eliminar: boolean): Promise<WriteOp[]> {
    const ops: WriteOp[] = [];
    const b = boletaPorId(g.boletaId);
    if (b) {
      const pagos = b.pagos.filter((p) => p.gastoId !== g.id);
      if (!eliminar) pagos.push({ gastoId: g.id, fecha: g.fecha, monto: g.monto });
      let nb: Boleta = { ...b, pagos };
      if (eliminar && b.estado === 'pagada' && pagadoDe(nb) < b.monto) nb.estado = 'pendiente';
      nb = recalcularEstado(nb);
      ops.push(await set('boletas', nb));
    }
    const d = deudaPorId(g.deudaId);
    if (d && g.cuotaMes) {
      const pagos = { ...d.pagos };
      if (eliminar) delete pagos[g.cuotaMes];
      else pagos[g.cuotaMes] = { gastoId: g.id, fecha: g.fecha, monto: g.monto };
      const nd: Deuda = { ...d, pagos };
      ops.push(await set('deudas', nd));
    }
    return ops;
  }

  async function guardarSettings(settings: Settings) {
    await backend.updateFamily(familyId, { settingsEnc: await cifrar(llave, settings) });
  }

  return {
    guardarSettings,
    renombrarFamilia: (nombre: string) => backend.updateFamily(familyId, { nombre }),

    nuevoGasto(datos: Omit<Gasto, 'id' | 'creadoPor' | 'creadoPorNombre' | 'creadoEn'>): Gasto {
      return { ...datos, id: nuevoId(), ...audit() };
    },
    async guardarGasto(g: Gasto) {
      commit([await set('gastos', g), ...(await opsEnlace(g, false))]);
    },
    async eliminarGasto(g: Gasto) {
      const ops = [del('gastos', g.id), ...(await opsEnlace(g, true))];
      if (g.adjuntoId) ops.push(del('adjuntos', g.adjuntoId));
      commit(ops);
    },

    async guardarIngreso(i: Omit<Ingreso, 'id' | 'creadoPor' | 'creadoPorNombre' | 'creadoEn'> & Partial<Ingreso>) {
      const obj: Ingreso = { ...audit(), id: nuevoId(), ...i } as Ingreso;
      commit([await set('ingresos', obj)]);
    },
    eliminarIngreso: (i: Ingreso) => commit([del('ingresos', i.id)]),

    async guardarBoleta(b: Omit<Boleta, 'id' | 'creadoPor' | 'creadoPorNombre' | 'creadoEn' | 'pagos' | 'estado'> & Partial<Boleta>) {
      const obj = recalcularEstado({ ...audit(), id: nuevoId(), pagos: [], estado: 'pendiente', ...b } as Boleta);
      commit([await set('boletas', obj)]);
      return obj;
    },
    async eliminarBoleta(b: Boleta, gastos: Gasto[]) {
      // Los pagos ya hechos se mantienen como gastos, sin el enlace.
      const ops: WriteOp[] = [del('boletas', b.id)];
      for (const g of gastos.filter((x) => x.boletaId === b.id)) {
        const { boletaId: _b, ...resto } = g;
        void _b;
        ops.push(await set('gastos', resto as Gasto));
      }
      if (b.adjuntoId) ops.push(del('adjuntos', b.adjuntoId));
      commit(ops);
    },
    async pagarBoleta(b: Boleta, p: { fecha: string; monto: number; medioPago?: string; cerrar: boolean }) {
      const g: Gasto = {
        id: nuevoId(), ...audit(), fecha: p.fecha, categoriaId: b.categoriaId, monto: p.monto,
        descripcion: `Boleta: ${b.detalle || 'sin detalle'}`, medioPago: p.medioPago, boletaId: b.id,
      };
      let nb: Boleta = { ...b, pagos: [...b.pagos, { gastoId: g.id, fecha: g.fecha, monto: g.monto }] };
      if (p.cerrar) nb.estado = 'pagada';
      nb = recalcularEstado(nb);
      commit([await set('gastos', g), await set('boletas', nb)]);
    },
    async cambiarEstadoBoleta(b: Boleta, estado: Boleta['estado']) {
      commit([await set('boletas', recalcularEstado({ ...b, estado }))]);
    },

    async guardarDeuda(d: Omit<Deuda, 'id' | 'creadoPor' | 'creadoPorNombre' | 'creadoEn' | 'pagos' | 'ajustes'> & Partial<Deuda>) {
      const obj = { ...audit(), id: nuevoId(), pagos: {}, ajustes: {}, ...d } as Deuda;
      commit([await set('deudas', obj)]);
      return obj;
    },
    eliminarDeuda: (d: Deuda) => commit([del('deudas', d.id)]),
    async pagarCuota(d: Deuda, mes: MesKey, p: { fecha: string; monto: number; medioPago?: string }) {
      const etiqueta = etiquetaCuota(d, mes);
      const g: Gasto = {
        id: nuevoId(), ...audit(), fecha: p.fecha, categoriaId: d.categoriaId, monto: p.monto, medioPago: p.medioPago,
        descripcion: `${etiqueta ? etiqueta + ' · ' : ''}${d.acreedor}`, deudaId: d.id, cuotaMes: mes,
      };
      const nd: Deuda = { ...d, pagos: { ...d.pagos, [mes]: { gastoId: g.id, fecha: g.fecha, monto: g.monto } } };
      commit([await set('gastos', g), await set('deudas', nd)]);
    },
    async deshacerPagoCuota(d: Deuda, mes: MesKey) {
      const p = d.pagos[mes];
      if (!p) return;
      const pagos = { ...d.pagos };
      delete pagos[mes];
      const nd: Deuda = { ...d, pagos };
      commit([del('gastos', p.gastoId), await set('deudas', nd)]);
    },
    /** Compra con tarjeta en N cuotas: crea el plan de cuotas futuras. */
    async compraEnCuotas(c: {
      descripcion: string; categoriaId: string; total: number; numCuotas: number; valorCuota: number; primerMes: MesKey; medioPago?: string;
    }) {
      const ajustes: Record<MesKey, number> = {};
      const ultimo = c.total - c.valorCuota * (c.numCuotas - 1);
      if (c.numCuotas > 1 && ultimo !== c.valorCuota && ultimo > 0 && Math.abs(ultimo - c.valorCuota) < c.valorCuota) {
        ajustes[sumarMeses(c.primerMes, c.numCuotas - 1)] = ultimo;
      }
      const d: Deuda = {
        id: nuevoId(), ...audit(), acreedor: c.descripcion, tipo: 'compra_cuotas', categoriaId: c.categoriaId,
        montoCuota: c.valorCuota, numCuotas: c.numCuotas, primerMes: c.primerMes, ajustes, pagos: {},
        montoTotal: c.total, notas: c.medioPago ? `Pagado con ${c.medioPago}` : undefined,
      };
      commit([await set('deudas', d)]);
      return d;
    },

    async guardarAdjunto(dataUrl: string): Promise<string> {
      const obj = { id: nuevoId(), dataUrl, creadoPor: user.uid, creadoEn: Date.now() };
      commit([await set('adjuntos', obj)]);
      return obj.id;
    },
    async leerAdjunto(id: string): Promise<string | null> {
      const raw = await backend.getDoc(familyId, 'adjuntos', id);
      if (!raw) return null;
      return (await deRaw<{ dataUrl: string }>(llave, raw))?.dataUrl ?? null;
    },
    eliminarAdjunto: (id: string) => commit([del('adjuntos', id)]),

    /** Escritura masiva (importación). */
    async importar(items: { coll: ColeccionNombre; obj: Base }[], settings?: Settings) {
      const ops = await Promise.all(items.map((x) => set(x.coll, x.obj)));
      if (settings) await guardarSettings(settings);
      await backend.commit(familyId, ops);
    },

    async leerRango<T>(coll: ColeccionNombre, desde: MesKey, hasta: MesKey): Promise<T[]> {
      return deRaws<T>(llave, await backend.getCollection(familyId, coll, { desde, hasta }));
    },
  };
}

export type Acciones = ReturnType<typeof crearAcciones>;
