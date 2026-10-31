import { useState } from 'react';
import { Campo, Icon, Seg, SubPagina } from '../components/ui';
import { useApp, useFamilia } from '../data/store';
import { entregarArchivo, puedeCompartirArchivos } from '../lib/compartir';
import { mesActual, nombreMes } from '../lib/format';
import type { ResultadoImportacion } from '../lib/importar';
import { armarInforme, nombreArchivo, tituloPeriodo } from '../lib/informe';
import type { ColeccionNombre, Gasto, Ingreso } from '../lib/types';

type Periodo = 'mes' | 'anio' | 'rango';

export function Exportar({ onBack }: { onBack: () => void }) {
  const f = useFamilia();
  const { error } = useApp();
  const [periodo, setPeriodo] = useState<Periodo>('mes');
  const [mes, setMes] = useState(f.mes);
  const [anio, setAnio] = useState(f.mes.slice(0, 4));
  const [desde, setDesde] = useState(`${f.mes.slice(0, 4)}-01`);
  const [hasta, setHasta] = useState(f.mes);
  const [ocupado, setOcupado] = useState<string | null>(null);
  const compartir = puedeCompartirArchivos();

  const rango = periodo === 'mes' ? { desde: mes, hasta: mes } : periodo === 'anio' ? { desde: `${anio}-01`, hasta: `${anio}-12` } : { desde, hasta };
  const valido = rango.desde <= rango.hasta;

  async function exportar(formato: 'xlsx' | 'pdf', modo: 'descargar' | 'compartir') {
    if (!valido) return;
    setOcupado(formato + modo);
    try {
      const [gastos, ingresos] = await Promise.all([
        f.acciones.leerRango<Gasto>('gastos', rango.desde, rango.hasta),
        f.acciones.leerRango<Ingreso>('ingresos', rango.desde, rango.hasta),
      ]);
      const datos = armarInforme({
        familia: f.family.nombre, ...rango, settings: f.settings, gastos, ingresos, boletas: f.boletas, deudas: f.deudas, members: f.members,
      });
      const blob = formato === 'xlsx'
        ? await (await import('../lib/export-excel')).generarExcel(datos)
        : await (await import('../lib/export-pdf')).generarPdf(datos);
      await entregarArchivo(blob, nombreArchivo(datos, formato), modo);
    } catch (e) {
      error(e);
    } finally {
      setOcupado(null);
    }
  }

  const botones = (formato: 'xlsx' | 'pdf') => (
    <div className="btn-row">
      <button className="btn" disabled={!!ocupado || !valido} onClick={() => exportar(formato, 'descargar')}>
        {Icon.download} {ocupado === formato + 'descargar' ? 'Generando…' : 'Descargar'}
      </button>
      {compartir && (
        <button className="btn" disabled={!!ocupado || !valido} onClick={() => exportar(formato, 'compartir')}>
          {Icon.share} {ocupado === formato + 'compartir' ? 'Generando…' : 'Compartir'}
        </button>
      )}
    </div>
  );

  return (
    <SubPagina titulo="Excel y PDF" onBack={onBack}>
      <div className="card stack">
        <h2>Período</h2>
        <Seg opciones={[['mes', 'Un mes'], ['anio', 'Un año'], ['rango', 'Rango']]} valor={periodo} onChange={setPeriodo} />
        {periodo === 'mes' && <Campo label="Mes"><input className="input" type="month" value={mes} onChange={(e) => e.target.value && setMes(e.target.value)} /></Campo>}
        {periodo === 'anio' && (
          <Campo label="Año">
            <select className="input" value={anio} onChange={(e) => setAnio(e.target.value)}>
              {Array.from({ length: 6 }, (_, i) => String(Number(mesActual().slice(0, 4)) + 1 - i)).map((a) => <option key={a}>{a}</option>)}
            </select>
          </Campo>
        )}
        {periodo === 'rango' && (
          <div className="grid2">
            <Campo label="Desde"><input className="input" type="month" value={desde} onChange={(e) => e.target.value && setDesde(e.target.value)} /></Campo>
            <Campo label="Hasta"><input className="input" type="month" value={hasta} onChange={(e) => e.target.value && setHasta(e.target.value)} /></Campo>
          </div>
        )}
        {!valido && <p className="error-text">“Desde” debe ser anterior a “Hasta”.</p>}
        <p className="muted small">{valido ? tituloPeriodo(rango) : ''}</p>
      </div>

      <div className="card stack">
        <div className="row"><span className="icono">📊</span><div><h3>Excel (.xlsx)</h3><p className="muted small">Presupuesto, registro de gastos, ingresos, boletas y proyección de deudas, como tu planilla.</p></div></div>
        {botones('xlsx')}
      </div>
      <div className="card stack">
        <div className="row"><span className="icono">📄</span><div><h3>PDF</h3><p className="muted small">Informe para imprimir o enviar: resumen, categorías, gastos y boletas pendientes.</p></div></div>
        {botones('pdf')}
      </div>
      <p className="muted tiny">Los archivos se generan en tu teléfono. Recuerda que el archivo descargado no va cifrado: guárdalo con cuidado.</p>

      <Importar />
    </SubPagina>
  );
}

function Importar() {
  const f = useFamilia();
  const { user, error, avisar } = useApp();
  const [res, setRes] = useState<ResultadoImportacion | null>(null);
  const [ocupado, setOcupado] = useState(false);
  const [presupuesto, setPresupuesto] = useState(true);

  async function leer(file?: File) {
    if (!file || !user) return;
    setOcupado(true);
    try {
      const { importarPlanilla } = await import('../lib/importar');
      setRes(await importarPlanilla(await file.arrayBuffer(), f.settings, user));
    } catch (e) {
      error(new Error('No pude leer el archivo. ¿Es la planilla de presupuesto en formato .xlsx?'));
      console.error(e);
    } finally {
      setOcupado(false);
    }
  }

  async function confirmar() {
    if (!res) return;
    setOcupado(true);
    try {
      const items: { coll: ColeccionNombre; obj: { id: string; creadoPor: string; creadoEn: number } }[] = [
        ...res.gastos.map((obj) => ({ coll: 'gastos' as const, obj })),
        ...res.boletas.map((obj) => ({ coll: 'boletas' as const, obj })),
        ...res.deudas.map((obj) => ({ coll: 'deudas' as const, obj })),
      ];
      // Si no se reemplaza el presupuesto, igual se agregan las categorías nuevas que usan los movimientos.
      const settings = presupuesto ? res.settings : {
        ...f.settings,
        categorias: [...f.settings.categorias, ...res.settings.categorias.filter((c) => !f.settings.categorias.some((x) => x.id === c.id))],
      };
      await f.acciones.importar(items, settings);
      avisar(`Importado: ${res.gastos.length} gastos, ${res.boletas.length} boletas y ${res.deudas.length} deudas`);
      setRes(null);
    } catch (e) {
      error(e);
    } finally {
      setOcupado(false);
    }
  }

  return (
    <div className="card stack">
      <div className="row"><span className="icono">📥</span><div><h3>Importar mi planilla</h3><p className="muted small">Sube tu Excel de presupuesto (hojas Presupuesto, Registro, Boletas y Deudas) para traer tus datos a la app.</p></div></div>
      {!res ? (
        <label className={'btn soft block' + (ocupado ? ' disabled' : '')}>
          {Icon.upload} {ocupado ? 'Leyendo…' : 'Elegir archivo .xlsx'}
          <input type="file" accept=".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" hidden onChange={(e) => leer(e.target.files?.[0])} />
        </label>
      ) : (
        <>
          <div className="alert ok stack tight" style={{ display: 'block' }}>
            <b>Encontré:</b>
            <ul style={{ margin: '6px 0 0', paddingLeft: 18 }}>
              <li>{res.settings.categorias.length} categorías e {res.settings.ingresosFijos.length} ingresos fijos</li>
              <li>{res.gastos.length} gastos (incluye pagos de boletas)</li>
              <li>{res.boletas.length} boletas</li>
              <li>{res.deudas.length} deudas con su proyección{res.deudas.length ? `: ${res.deudas.map((d) => d.acreedor).join(', ')}` : ''}</li>
              {res.categoriasNuevas.length > 0 && <li>Categorías nuevas: {res.categoriasNuevas.join(', ')}</li>}
            </ul>
          </div>
          {res.avisos.map((a) => <div key={a} className="alert warn small">{a}</div>)}
          <label className="check"><input type="checkbox" checked={presupuesto} onChange={(e) => setPresupuesto(e.target.checked)} /> Usar también los montos de presupuesto e ingresos de la planilla</label>
          <p className="muted tiny">Si importas el mismo archivo dos veces, los registros no se duplican (se actualizan). Mes de referencia: {nombreMes(f.mes)}.</p>
          <div className="btn-row">
            <button className="btn" onClick={() => setRes(null)} disabled={ocupado}>Cancelar</button>
            <button className="btn primary" onClick={confirmar} disabled={ocupado}>{ocupado ? 'Importando…' : 'Importar'}</button>
          </div>
        </>
      )}
    </div>
  );
}
