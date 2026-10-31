// Importa la planilla "PRESUPUESTO_CASA" (hojas Presupuesto, Registro, Boletas
// y Deudas) a la familia actual. Todo se procesa en el teléfono.
import ExcelJS from 'exceljs';
import { CATEGORIA_CUOTAS, nuevoId } from './defaults';
import { mesesEntre, normalizar, sumarMeses } from './format';
import type { Boleta, Categoria, Deuda, Gasto, IngresoFijo, MesKey, Settings, Tipo } from './types';
import { TIPOS } from './types';

export interface ResultadoImportacion {
  settings: Settings;
  gastos: Gasto[];
  boletas: Boleta[];
  deudas: Deuda[];
  categoriasNuevas: string[];
  avisos: string[];
}

type Valor = string | number | Date | null;

function valor(c: ExcelJS.Cell | undefined): Valor {
  let v: unknown = c?.value;
  if (v == null) return null;
  if (typeof v === 'object' && !(v instanceof Date)) {
    const o = v as { result?: unknown; richText?: { text: string }[]; text?: string; error?: string };
    if ('result' in o) v = o.result;
    else if (o.richText) v = o.richText.map((t) => t.text).join('');
    else if ('text' in o) v = o.text;
    else if (o.error) return null;
    else return null;
  }
  if (v == null) return null;
  if (v instanceof Date || typeof v === 'number' || typeof v === 'string') return v;
  if (typeof v === 'boolean') return v ? 'Sí' : 'No';
  return null;
}

const texto = (v: Valor) => (v == null ? '' : v instanceof Date ? '' : String(v).trim());
const numero = (v: Valor): number | null => {
  if (typeof v === 'number') return v;
  if (typeof v === 'string') {
    const n = parseFloat(v.replace(/[$\s.]/g, '').replace(',', '.'));
    return Number.isFinite(n) ? n : null;
  }
  return null;
};
const pad = (n: number) => String(n).padStart(2, '0');
function fecha(v: Valor): string | null {
  if (v instanceof Date) return `${v.getUTCFullYear()}-${pad(v.getUTCMonth() + 1)}-${pad(v.getUTCDate())}`;
  if (typeof v === 'number' && v > 20000 && v < 80000) {
    const d = new Date(Date.UTC(1899, 11, 30) + v * 86400000);
    return fecha(d);
  }
  if (typeof v === 'string') {
    const m = v.trim().match(/^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$/);
    if (m) return `${m[3]}-${pad(+m[2])}-${pad(+m[1])}`;
    const iso = v.trim().match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (iso) return `${iso[1]}-${iso[2]}-${iso[3]}`;
  }
  return null;
}

/** Busca la fila cuyo contenido incluye todos los encabezados indicados. */
function buscarEncabezado(ws: ExcelJS.Worksheet, requeridos: string[]): { fila: number; cols: Record<string, number> } | null {
  const req = requeridos.map(normalizar);
  for (let r = 1; r <= Math.min(ws.rowCount, 40); r++) {
    const cols: Record<string, number> = {};
    ws.getRow(r).eachCell({ includeEmpty: false }, (c, col) => {
      const t = normalizar(texto(valor(c)));
      if (t && !(t in cols)) cols[t] = col;
    });
    if (req.every((h) => h in cols)) return { fila: r, cols };
  }
  return null;
}

function hash(s: string): string {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return (h >>> 0).toString(36);
}

export async function importarPlanilla(buf: ArrayBuffer, actual: Settings, user: { uid: string; nombre: string }): Promise<ResultadoImportacion> {
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const hoja = (nombre: string) => wb.worksheets.find((w) => normalizar(w.name) === normalizar(nombre));
  const avisos: string[] = [];
  const categoriasNuevas: string[] = [];
  const settings: Settings = JSON.parse(JSON.stringify(actual));
  const ahora = Date.now();
  const audit = { creadoPor: user.uid, creadoPorNombre: user.nombre, creadoEn: ahora };
  const usados = new Map<string, number>();
  const idUnico = (pref: string, clave: string) => {
    const base = `imp-${pref}-${hash(clave)}`;
    const n = (usados.get(base) || 0) + 1;
    usados.set(base, n);
    return n === 1 ? base : `${base}-${n}`;
  };

  const porNombre = (nombre: string) => {
    const n = normalizar(nombre);
    return settings.categorias.find((c) => normalizar(c.nombre) === n);
  };
  const esCuotas = (nombre: string) => normalizar(nombre).startsWith('cuotas de deuda');
  const categoriaDe = (nombre: string, tipo: Tipo = 'Prescindible'): string => {
    if (!nombre) return settings.categorias.find((c) => c.id === 'otros')?.id ?? settings.categorias[0].id;
    if (esCuotas(nombre) && settings.categorias.some((c) => c.id === CATEGORIA_CUOTAS)) return CATEGORIA_CUOTAS;
    const c = porNombre(nombre);
    if (c) return c.id;
    const nueva: Categoria = { id: nuevoId(), nombre: nombre.trim(), tipo, presupuesto: null };
    settings.categorias.push(nueva);
    categoriasNuevas.push(nueva.nombre);
    return nueva.id;
  };

  // ---- Presupuesto: categorías, presupuestos e ingresos ----
  const pres = hoja('Presupuesto');
  if (pres) {
    const h = buscarEncabezado(pres, ['GASTOS', 'Tipo', 'Presupuestado']);
    if (h) {
      const cNom = h.cols[normalizar('GASTOS')];
      const cTipo = h.cols[normalizar('Tipo')];
      const cPres = h.cols[normalizar('Presupuestado')];
      for (let r = h.fila + 1; r <= pres.rowCount; r++) {
        const row = pres.getRow(r);
        const nombre = texto(valor(row.getCell(cNom)));
        if (!nombre || normalizar(nombre).startsWith('total')) break;
        const tipoTxt = texto(valor(row.getCell(cTipo)));
        const tipo = (TIPOS.find((t) => normalizar(t) === normalizar(tipoTxt)) ?? 'Prescindible') as Tipo;
        const celdaPres = row.getCell(cPres);
        const esFormula = typeof celdaPres.value === 'object' && celdaPres.value != null && 'formula' in (celdaPres.value as object);
        const monto = esFormula ? null : numero(valor(celdaPres));
        const id = categoriaDe(nombre, tipo);
        const cat = settings.categorias.find((c) => c.id === id)!;
        cat.tipo = id === CATEGORIA_CUOTAS ? 'Deudas' : tipo;
        if (id !== CATEGORIA_CUOTAS) cat.presupuesto = monto && monto > 0 ? Math.round(monto) : null;
      }
    } else avisos.push('No encontré la tabla de gastos en la hoja Presupuesto.');

    const hi = buscarEncabezado(pres, ['INGRESOS', 'Monto mensual']);
    if (hi) {
      const cNom = hi.cols[normalizar('INGRESOS')];
      const cMonto = hi.cols[normalizar('Monto mensual')];
      for (let r = hi.fila + 1; r <= hi.fila + 15; r++) {
        const row = pres.getRow(r);
        const nombre = texto(valor(row.getCell(cNom)));
        if (!nombre || normalizar(nombre).startsWith('total')) break;
        const monto = Math.round(numero(valor(row.getCell(cMonto))) || 0);
        const existe = settings.ingresosFijos.find((i) => normalizar(i.nombre) === normalizar(nombre));
        if (existe) existe.monto = monto;
        else if (monto > 0) settings.ingresosFijos.push({ id: nuevoId(), nombre, monto, ajustes: {} } as IngresoFijo);
      }
    }
  } else avisos.push('No se encontró la hoja Presupuesto (se mantienen tus categorías).');

  // ---- Registro de gastos ----
  const gastos: Gasto[] = [];
  const reg = hoja('Registro');
  if (reg) {
    const h = buscarEncabezado(reg, ['Fecha', 'Categoría', 'Monto']);
    if (h) {
      const c = (k: string) => h.cols[normalizar(k)];
      for (let r = h.fila + 1; r <= reg.rowCount; r++) {
        const row = reg.getRow(r);
        const f = fecha(valor(row.getCell(c('Fecha'))));
        const monto = numero(valor(row.getCell(c('Monto'))));
        if (!f || !monto) continue;
        const cat = texto(valor(row.getCell(c('Categoría'))));
        const desc = c('Descripción') ? texto(valor(row.getCell(c('Descripción')))) : '';
        gastos.push({
          id: idUnico('g', `${f}|${cat}|${desc}|${monto}`), ...audit, fecha: f, categoriaId: categoriaDe(cat), descripcion: desc, monto: Math.round(monto),
        });
      }
    }
  }

  // ---- Boletas ----
  const boletas: Boleta[] = [];
  const bol = hoja('Boletas');
  if (bol) {
    const h = buscarEncabezado(bol, ['Vencimiento', 'Categoría', 'Monto']);
    if (h) {
      const c = (k: string) => h.cols[normalizar(k)];
      for (let r = h.fila + 1; r <= bol.rowCount; r++) {
        const row = bol.getRow(r);
        const venc = fecha(valor(row.getCell(c('Vencimiento'))));
        const monto = numero(valor(row.getCell(c('Monto'))));
        if (!venc || !monto) continue;
        const cat = texto(valor(row.getCell(c('Categoría'))));
        const detalle = c('Detalle') ? texto(valor(row.getCell(c('Detalle')))) : '';
        const pagadaTxt = c('¿Pagada?') ? normalizar(texto(valor(row.getCell(c('¿Pagada?')))) || 'no') : 'no';
        const fPago = c('Fecha de pago') ? fecha(valor(row.getCell(c('Fecha de pago')))) : null;
        const mPago = c('Monto pagado') ? numero(valor(row.getCell(c('Monto pagado')))) : null;
        const categoriaId = categoriaDe(cat);
        const b: Boleta = {
          id: idUnico('b', `${venc}|${cat}|${detalle}|${monto}`), ...audit, vencimiento: venc, categoriaId, detalle, monto: Math.round(monto),
          estado: pagadaTxt === 'si' ? 'pagada' : pagadaTxt.startsWith('traspas') ? 'traspasada' : 'pendiente', pagos: [],
        };
        const pagado = mPago && mPago > 0 ? mPago : b.estado === 'pagada' ? monto : 0;
        if (pagado > 0) {
          const g: Gasto = {
            id: `${b.id}-pago`, ...audit, fecha: fPago || venc, categoriaId, monto: Math.round(pagado),
            descripcion: `Boleta: ${detalle || cat}`, boletaId: b.id,
          };
          gastos.push(g);
          b.pagos.push({ gastoId: g.id, fecha: g.fecha, monto: g.monto });
          if (b.estado === 'pendiente' && pagado >= monto) b.estado = 'pagada';
        }
        boletas.push(b);
      }
    }
  }

  // ---- Deudas: proyección de cuotas ----
  const deudas: Deuda[] = [];
  const deu = hoja('Deudas');
  if (deu) {
    const h = buscarEncabezado(deu, ['Acreedor / Mes']);
    if (h) {
      const cNom = h.cols[normalizar('Acreedor / Mes')];
      const meses: { col: number; mes: MesKey }[] = [];
      deu.getRow(h.fila).eachCell({ includeEmpty: false }, (cell, col) => {
        const f = fecha(valor(cell));
        if (f && col > cNom) meses.push({ col, mes: f.slice(0, 7) });
      });
      for (let r = h.fila + 1; r <= deu.rowCount; r++) {
        const row = deu.getRow(r);
        const nombre = texto(valor(row.getCell(cNom)));
        if (normalizar(nombre).startsWith('total')) break;
        if (!nombre) continue;
        const vals = meses.map((m) => ({ mes: m.mes, v: Math.round(numero(valor(row.getCell(m.col))) || 0) }));
        const conMonto = vals.filter((x) => x.v > 0);
        if (!conMonto.length) continue;
        const primerMes = conMonto[0].mes;
        const ultimoMes = conMonto[conMonto.length - 1].mes;
        const freq = new Map<number, number>();
        conMonto.forEach((x) => freq.set(x.v, (freq.get(x.v) || 0) + 1));
        const montoCuota = [...freq.entries()].sort((a, b) => b[1] - a[1])[0][0];
        const llegaAlFinal = ultimoMes === meses[meses.length - 1].mes && conMonto.length > 1;
        const numCuotas = llegaAlFinal ? null : mesesEntre(primerMes, ultimoMes) + 1;
        const ajustes: Record<MesKey, number> = {};
        for (let m = primerMes; m <= ultimoMes; m = sumarMeses(m, 1)) {
          const v = vals.find((x) => x.mes === m)?.v ?? 0;
          if (v !== montoCuota) ajustes[m] = v;
        }
        deudas.push({
          id: idUnico('d', nombre), ...audit, acreedor: nombre, tipo: normalizar(nombre).includes('convenio') ? 'convenio' : normalizar(nombre).includes('prestamo') ? 'prestamo' : 'otro',
          categoriaId: CATEGORIA_CUOTAS, montoCuota, numCuotas, primerMes, ajustes, pagos: {},
        });
        if (llegaAlFinal) avisos.push(`"${nombre}" tiene cuotas hasta el final de la planilla: quedó sin término. Ajusta el N° de cuotas si corresponde.`);
      }
    }
    // Tabla de deudas con saldo y tasa (si se usó)
    const ht = buscarEncabezado(deu, ['Acreedor', 'Saldo pendiente', 'Cuota mensual']);
    if (ht) {
      const c = (k: string) => ht.cols[normalizar(k)];
      for (let r = ht.fila + 1; r <= ht.fila + 30; r++) {
        const row = deu.getRow(r);
        const nombre = texto(valor(row.getCell(c('Acreedor'))));
        if (!nombre) break;
        const saldo = numero(valor(row.getCell(c('Saldo pendiente')))) || 0;
        const cuota = numero(valor(row.getCell(c('Cuota mensual')))) || 0;
        const tasa = c('Tasa interés mensual') ? numero(valor(row.getCell(c('Tasa interés mensual')))) || 0 : 0;
        const ya = deudas.find((x) => normalizar(x.acreedor) === normalizar(nombre));
        if (ya) {
          if (tasa) ya.tasaMensual = tasa;
          if (saldo) ya.montoTotal = Math.round(saldo);
          continue;
        }
        if (saldo <= 0 && cuota <= 0) continue;
        const hoyMes = new Date().toISOString().slice(0, 7);
        deudas.push({
          id: idUnico('d', nombre), ...audit, acreedor: nombre, tipo: 'credito', categoriaId: CATEGORIA_CUOTAS,
          montoCuota: Math.round(cuota), numCuotas: null, primerMes: hoyMes, ajustes: {}, pagos: {},
          tasaMensual: tasa || undefined, montoTotal: Math.round(saldo) || undefined,
        });
      }
    }
  }

  if (!settings.categorias.some((c) => c.id === CATEGORIA_CUOTAS) && deudas.length) {
    settings.categorias.push({ id: CATEGORIA_CUOTAS, nombre: 'Cuotas de deudas', tipo: 'Deudas', presupuesto: null });
  }
  return { settings, gastos, boletas, deudas, categoriasNuevas, avisos };
}
