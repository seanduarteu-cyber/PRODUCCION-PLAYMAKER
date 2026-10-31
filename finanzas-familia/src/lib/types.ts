// Modelo de datos de la app. Cada familia (centro de costos) guarda sus datos
// por separado: nadie fuera de la familia puede leerlos (ver firestore.rules).

export type Tipo = 'Esencial' | 'Deudas' | 'Prescindible' | 'Ahorro';
export const TIPOS: Tipo[] = ['Esencial', 'Deudas', 'Prescindible', 'Ahorro'];

export type Rol = 'admin' | 'miembro';

/** 'YYYY-MM' */
export type MesKey = string;
/** 'YYYY-MM-DD' (fecha local, sin zona horaria) */
export type Fecha = string;

export interface Categoria {
  id: string;
  nombre: string;
  tipo: Tipo;
  /** Monto mensual presupuestado. null = sin presupuesto. */
  presupuesto: number | null;
}

export interface IngresoFijo {
  id: string;
  nombre: string;
  /** Monto mensual habitual */
  monto: number;
  /** Cambios puntuales para un mes específico */
  ajustes?: Record<MesKey, number>;
}

export interface Settings {
  categorias: Categoria[];
  ingresosFijos: IngresoFijo[];
  /** Meta de % del ingreso por tipo (ej: Esencial 0.6) */
  metas: Record<Tipo, number>;
  mediosPago: string[];
}

/** Familia ya descifrada en el dispositivo. */
export interface Family {
  id: string;
  nombre: string;
  creadoPor: string;
  creadoEn: number;
  settings: Settings;
}

/** Cómo se guarda la familia en el servidor (settings cifrados). */
export interface FamilyDoc {
  id: string;
  nombre: string;
  creadoPor: string;
  creadoEn: number;
  cifrado: { v: 1; sal: string; verificador: string };
  settingsEnc: string;
}

/**
 * Cómo se guarda cada registro en el servidor: todo el contenido va cifrado en
 * `enc`. Solo quedan visibles el mes (para filtrar), quién lo creó y cuándo.
 */
export interface RawDoc {
  id: string;
  enc: string;
  mes?: MesKey;
  creadoPor: string;
  creadoEn: number;
}

export interface FamilyRef {
  id: string;
  nombre: string;
  rol: Rol;
}

export interface Member {
  uid: string;
  nombre: string;
  email: string | null;
  rol: Rol;
  unidoEn: number;
}

export interface Invite {
  codigo: string;
  familyId: string;
  familyNombre: string;
  rol: Rol;
  creadoPor: string;
  expira: number;
  usadoPor?: string;
}

interface Auditable {
  id: string;
  creadoPor: string;
  creadoPorNombre: string;
  creadoEn: number;
}

/** Todo el dinero que sale (incluye pagos de boletas y de cuotas). */
export interface Gasto extends Auditable {
  fecha: Fecha;
  categoriaId: string;
  descripcion: string;
  monto: number;
  medioPago?: string;
  /** Si es el pago de una cuota */
  deudaId?: string;
  cuotaMes?: MesKey;
  /** Si es el pago (total o parcial) de una boleta */
  boletaId?: string;
  adjuntoId?: string;
}

/** Ingresos adicionales del mes (bonos, ventas, etc.). */
export interface Ingreso extends Auditable {
  fecha: Fecha;
  descripcion: string;
  monto: number;
}

export interface PagoBoleta {
  gastoId: string;
  fecha: Fecha;
  monto: number;
}

export type EstadoBoleta = 'pendiente' | 'pagada' | 'traspasada';

/** Boletas y cuentas por pagar (luz, agua, gas, colegio...). */
export interface Boleta extends Auditable {
  vencimiento: Fecha;
  categoriaId: string;
  detalle: string;
  monto: number;
  estado: EstadoBoleta;
  pagos: PagoBoleta[];
  adjuntoId?: string;
}

export type TipoDeuda = 'compra_cuotas' | 'credito' | 'convenio' | 'prestamo' | 'otro';

export const TIPOS_DEUDA: Record<TipoDeuda, string> = {
  compra_cuotas: 'Compra en cuotas',
  credito: 'Crédito / tarjeta',
  convenio: 'Convenio de pago',
  prestamo: 'Préstamo personal',
  otro: 'Otro',
};

export interface PagoCuota {
  gastoId: string;
  fecha: Fecha;
  monto: number;
}

/** Deudas y pagos en cuotas futuras. Genera la proyección mes a mes. */
export interface Deuda extends Auditable {
  acreedor: string;
  tipo: TipoDeuda;
  categoriaId: string;
  montoCuota: number;
  /** null = sin término definido */
  numCuotas: number | null;
  primerMes: MesKey;
  /** Cuota distinta en un mes específico (cuotas variables, UF...). */
  ajustes: Record<MesKey, number>;
  /** Desde este mes ya no se cobran cuotas (deuda pagada/cerrada). */
  cerradaDesde?: MesKey;
  tasaMensual?: number;
  montoTotal?: number;
  notas?: string;
  pagos: Record<MesKey, PagoCuota>;
}

export interface Adjunto {
  id: string;
  dataUrl: string;
  creadoPor: string;
  creadoEn: number;
}

export type ColeccionNombre = 'gastos' | 'ingresos' | 'boletas' | 'deudas' | 'adjuntos';

export interface AppUser {
  uid: string;
  nombre: string;
  email: string | null;
}
