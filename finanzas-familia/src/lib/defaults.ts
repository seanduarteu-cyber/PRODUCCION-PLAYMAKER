import type { Categoria, Settings, Tipo } from './types';

export const CATEGORIA_CUOTAS = 'cuotas';
export const SIN_CATEGORIA = '__sin__';

const cat = (id: string, nombre: string, tipo: Tipo): Categoria => ({ id, nombre, tipo, presupuesto: null });

export const CATEGORIAS_BASE: Categoria[] = [
  cat('arriendo', 'Arriendo / dividendo', 'Esencial'),
  cat('luz', 'Luz', 'Esencial'),
  cat('agua', 'Agua', 'Esencial'),
  cat('gas', 'Gas', 'Esencial'),
  cat('internet', 'Internet', 'Esencial'),
  cat('celular', 'Celular', 'Esencial'),
  cat('supermercado', 'Supermercado', 'Esencial'),
  cat('frutas', 'Frutas y verduras', 'Esencial'),
  cat('carnes', 'Carnes', 'Esencial'),
  cat('transporte', 'Transporte / bencina', 'Esencial'),
  cat('salud', 'Salud y farmacia', 'Esencial'),
  cat('educacion', 'Educación', 'Esencial'),
  cat('hijos', 'Cuidado de hijos / dependientes', 'Esencial'),
  cat(CATEGORIA_CUOTAS, 'Cuotas de deudas', 'Deudas'),
  cat('comida-fuera', 'Comida fuera / delivery', 'Prescindible'),
  cat('suscripciones', 'Suscripciones y apps', 'Prescindible'),
  cat('ropa', 'Ropa y calzado', 'Prescindible'),
  cat('ocio', 'Panoramas y ocio', 'Prescindible'),
  cat('otros', 'Otros gastos', 'Prescindible'),
  cat('emergencia', 'Fondo de emergencia', 'Ahorro'),
  cat('pago-extra', 'Pago extra a deudas', 'Ahorro'),
];

export function settingsIniciales(): Settings {
  return {
    categorias: CATEGORIAS_BASE.map((c) => ({ ...c })),
    ingresosFijos: [
      { id: 'sueldo-1', nombre: 'Sueldo principal', monto: 0 },
      { id: 'sueldo-2', nombre: 'Sueldo pareja / secundario', monto: 0 },
      { id: 'aportes', nombre: 'Aportes, pensiones o subsidios', monto: 0 },
    ],
    metas: { Esencial: 0.6, Deudas: 0.2, Prescindible: 0.1, Ahorro: 0.1 },
    mediosPago: ['Efectivo', 'Débito', 'Crédito', 'Transferencia'],
  };
}

export const CLAVES = [
  'Presupuesta a principio de mes: asigna cada peso antes de gastarlo.',
  'Paga primero lo Esencial y las cuotas mínimas de deudas.',
  "Recorta 'Prescindible' primero: cada peso liberado va a deudas o ahorro.",
  'Meta 1: fondo de emergencia de 1 mes de gastos esenciales.',
  'Deudas: todo extra a la de mayor tasa (estrategia avalancha).',
  'Anota TODOS los gastos, incluso los pequeños.',
];

export function nuevoId(): string {
  const a = new Uint8Array(10);
  crypto.getRandomValues(a);
  return Array.from(a, (b) => b.toString(36).padStart(2, '0')).join('').slice(0, 16);
}
