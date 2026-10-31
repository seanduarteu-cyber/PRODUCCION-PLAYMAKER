import { useMemo, useState } from 'react';
import { Barra, Campo, Cargando, EMOJI_TIPO, MontoInput, Seg, Sheet } from '../components/ui';
import { useApp, useFamilia } from '../data/store';
import { montoIngresoFijo, resumenBoletas, resumenMes, type FilaCategoria } from '../lib/calc';
import { CLAVES } from '../lib/defaults';
import { fmtCLP, fmtFecha, fmtPct, hoy, mesDe, nombreMes, primerDia } from '../lib/format';
import type { Ingreso, IngresoFijo } from '../lib/types';
import { Encabezado, useNav } from './Shell';

export function Resumen() {
  const f = useFamilia();
  const { irA } = useNav();
  const r = useMemo(() => resumenMes({
    settings: f.settings, mes: f.mes, gastos: f.gastos, ingresos: f.ingresos, boletas: f.boletas, deudas: f.deudas,
  }), [f.settings, f.mes, f.gastos, f.ingresos, f.boletas, f.deudas]);
  const bol = resumenBoletas(f.boletas, hoy());
  const [verTodas, setVerTodas] = useState(false);

  if (f.cargando) return <><Encabezado /><Cargando /></>;

  const filas = r.filas.filter((x) => verTodas || x.presupuestado || x.total);
  const nivelSaldo = r.estado.nivel === 'muted' ? '' : r.estado.nivel;

  return (
    <>
      <Encabezado />
      <div className="content">
        <div className="card hero">
          <div className="row between">
            <span className="muted small">Saldo proyectado a fin de mes</span>
            <span className={'badge ' + nivelSaldo}>{r.estado.texto}</span>
          </div>
          <div className={'big num ' + (r.saldoProyectado < 0 ? 'neg' : '')}>{fmtCLP(r.saldoProyectado)}</div>
          <p className="muted small">
            Ingresos {fmtCLP(r.ingresos)} − gasto esperado {fmtCLP(r.totales.esperado)}
          </p>
        </div>

        <div className="kpis">
          <div className="kpi"><div className="k">Ya pagado</div><div className="v num">{fmtCLP(r.totales.pagado)}</div></div>
          <div className={'kpi' + (r.totales.porPagar ? ' warn' : '')}><div className="k">Por pagar (boletas)</div><div className="v num">{fmtCLP(r.totales.porPagar)}</div></div>
          <div className="kpi"><div className="k">Saldo hoy</div><div className={'v num ' + (r.saldoHoy < 0 ? 'neg' : '')}>{fmtCLP(r.saldoHoy)}</div></div>
          <div className="kpi"><div className="k">Cuotas del mes</div><div className="v num">{fmtCLP(r.cuotas.pagado)} <span className="muted small">/ {fmtCLP(r.cuotas.total)}</span></div></div>
        </div>

        {bol.vencidas > 0 && (
          <button className="alert danger" style={{ border: 0, textAlign: 'left', cursor: 'pointer' }} onClick={() => irA('boletas')}>
            <span>⚠️</span>
            <span><b>{bol.vencidas} {bol.vencidas === 1 ? 'boleta vencida' : 'boletas vencidas'}</b> por {fmtCLP(bol.vencido)}. Pide el monto actualizado antes de pagar.</span>
          </button>
        )}
        {r.cuotas.pendientes.length > 0 && (
          <button className="alert warn" style={{ border: 0, textAlign: 'left', cursor: 'pointer' }} onClick={() => irA('cuotas')}>
            <span>📅</span>
            <span><b>{r.cuotas.pendientes.length} {r.cuotas.pendientes.length === 1 ? 'cuota pendiente' : 'cuotas pendientes'}</b> en {nombreMes(f.mes).toLowerCase()} por {fmtCLP(r.cuotas.total - r.cuotas.pagado)}.</span>
          </button>
        )}

        <Ingresos total={r.ingresos} />

        <div className="card">
          <div className="card-title"><h2>Distribución del gasto esperado</h2></div>
          <div className="stack">
            {r.distribucion.map((d) => (
              <div key={d.tipo} className="stack tight">
                <div className="row between">
                  <span>{EMOJI_TIPO[d.tipo]} {d.tipo}</span>
                  <span className="row" style={{ gap: 8 }}>
                    <span className="num small">{fmtCLP(d.esperado)}</span>
                    <span className={'badge ' + (d.fuera ? 'warn' : 'ok')}>{fmtPct(d.pct)}</span>
                  </span>
                </div>
                <Barra valor={d.pct} max={1} marca={d.meta} />
                <span className="tiny muted">Meta {fmtPct(d.meta)} del ingreso · {d.estado}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card flush">
          <div className="card-title" style={{ padding: '14px 14px 0' }}>
            <h2>Por categoría</h2>
            <button className="link small" onClick={() => setVerTodas(!verTodas)}>{verTodas ? 'Solo con movimiento' : 'Ver todas'}</button>
          </div>
          <div className="list">
            {filas.length === 0 && <p className="muted small" style={{ padding: 14 }}>Aún no hay presupuesto ni gastos este mes.</p>}
            {filas.map((x) => <FilaCat key={x.categoria.id} f={x} onClick={() => irA('gastos', { categoria: x.categoria.id })} />)}
          </div>
          <div className="row between" style={{ padding: '12px 14px', borderTop: '1px solid var(--border)', fontWeight: 700 }}>
            <span>Total</span>
            <span className="num">{fmtCLP(r.totales.total)} <span className="muted small">/ {fmtCLP(r.totales.presupuestado)}</span></span>
          </div>
        </div>

        <div className="card">
          <div className="stack tight small">
            <div className="row between"><span className="muted">Ingreso − presupuestado</span><span className={'num ' + (r.ingresoMenosPresupuestado < 0 ? 'neg' : '')}>{fmtCLP(r.ingresoMenosPresupuestado)}</span></div>
            <div className="row between"><span className="muted">Boletas atrasadas de meses anteriores</span><span className="num">{fmtCLP(r.atrasadas)}</span></div>
            <div className="row between"><span className="muted">Gasto en ítems sin presupuesto</span><span className="num">{fmtCLP(r.sinPresupuesto)}</span></div>
          </div>
        </div>

        <details className="card">
          <summary style={{ cursor: 'pointer', fontWeight: 650 }}>Claves estratégicas</summary>
          <ol style={{ margin: '10px 0 0', paddingLeft: 20 }} className="small stack tight">
            {CLAVES.map((c) => <li key={c}>{c}</li>)}
          </ol>
        </details>
      </div>
    </>
  );
}

function FilaCat({ f, onClick }: { f: FilaCategoria; onClick: () => void }) {
  const p = f.presupuestado;
  return (
    <button className="item" onClick={onClick} style={{ flexDirection: 'column', alignItems: 'stretch', gap: 6 }}>
      <div className="row between">
        <span className="t ellipsis">{f.categoria.nombre}</span>
        <span className="num m">{fmtCLP(f.total)}{p != null && <span className="muted small" style={{ fontWeight: 400 }}> / {fmtCLP(p)}</span>}</span>
      </div>
      <Barra valor={f.total} max={p ?? 0} />
      <div className="row between tiny muted">
        <span>
          {f.porPagar > 0 ? `Pagado ${fmtCLP(f.pagado)} · por pagar ${fmtCLP(f.porPagar)}` : f.cuotas > 0 ? `Incluye cuotas ${fmtCLP(f.cuotas)}` : f.categoria.tipo}
        </span>
        <span className={f.diferencia != null && f.diferencia < 0 ? 'neg' : ''}>
          {f.diferencia == null ? 'Sin presupuesto' : f.diferencia >= 0 ? `Quedan ${fmtCLP(f.diferencia)}` : `Excedido ${fmtCLP(-f.diferencia)}`}
        </span>
      </div>
    </button>
  );
}

// ---------------- Ingresos ----------------
function Ingresos({ total }: { total: number }) {
  const f = useFamilia();
  const [fijo, setFijo] = useState<IngresoFijo | null>(null);
  const [extra, setExtra] = useState<Ingreso | 'nuevo' | null>(null);
  const extras = f.ingresos.filter((i) => mesDe(i.fecha) === f.mes).sort((a, b) => a.fecha.localeCompare(b.fecha));
  return (
    <div className="card flush">
      <div className="card-title" style={{ padding: '14px 14px 0' }}>
        <h2>Ingresos de {nombreMes(f.mes).toLowerCase()}</h2>
        <span className="num" style={{ fontWeight: 700 }}>{fmtCLP(total)}</span>
      </div>
      <div className="list">
        {f.settings.ingresosFijos.map((i) => {
          const m = montoIngresoFijo(i, f.mes);
          const ajustado = i.ajustes && f.mes in i.ajustes;
          return (
            <button key={i.id} className="item" onClick={() => setFijo(i)}>
              <span className="grow">
                <div className="t">{i.nombre}</div>
                <div className="s">{ajustado ? 'Monto distinto solo este mes' : 'Fijo mensual'}</div>
              </span>
              <span className={'num m ' + (m ? '' : 'muted')}>{fmtCLP(m)}</span>
            </button>
          );
        })}
        {extras.map((i) => (
          <button key={i.id} className="item" onClick={() => setExtra(i)}>
            <span className="grow">
              <div className="t">{i.descripcion || 'Ingreso extra'}</div>
              <div className="s">{fmtFecha(i.fecha)} · {i.creadoPorNombre}</div>
            </span>
            <span className="num m pos">{fmtCLP(i.monto)}</span>
          </button>
        ))}
        <div className="item" style={{ cursor: 'default' }}>
          <button className="link" onClick={() => setExtra('nuevo')}>+ Agregar ingreso extra (bono, venta…)</button>
        </div>
      </div>
      {fijo && <IngresoFijoSheet ingreso={fijo} onClose={() => setFijo(null)} />}
      {extra && <IngresoExtraSheet ingreso={extra === 'nuevo' ? null : extra} onClose={() => setExtra(null)} />}
    </div>
  );
}

function IngresoFijoSheet({ ingreso, onClose }: { ingreso: IngresoFijo; onClose: () => void }) {
  const f = useFamilia();
  const { error, avisar } = useApp();
  const [alcance, setAlcance] = useState<'mes' | 'siempre'>(ingreso.ajustes && f.mes in ingreso.ajustes ? 'mes' : 'siempre');
  const [monto, setMonto] = useState<number | null>(montoIngresoFijo(ingreso, f.mes));

  async function guardar() {
    const ingresosFijos = f.settings.ingresosFijos.map((i) => {
      if (i.id !== ingreso.id) return i;
      const ajustes = { ...(i.ajustes || {}) };
      if (alcance === 'mes') return { ...i, ajustes: { ...ajustes, [f.mes]: monto || 0 } };
      delete ajustes[f.mes];
      return { ...i, monto: monto || 0, ajustes };
    });
    try {
      await f.acciones.guardarSettings({ ...f.settings, ingresosFijos });
      avisar('Ingreso actualizado');
      onClose();
    } catch (e) {
      error(e);
    }
  }

  return (
    <Sheet titulo={ingreso.nombre} onClose={onClose} pie={<button className="btn primary" onClick={guardar}>Guardar</button>}>
      <MontoInput value={monto} onChange={setMonto} grande autoFocus />
      <Seg opciones={[['siempre', 'Todos los meses'], ['mes', `Solo ${nombreMes(f.mes).toLowerCase()}`]]} valor={alcance} onChange={setAlcance} />
      <p className="muted small">
        {alcance === 'siempre'
          ? `Cambia el monto mensual habitual (hoy ${fmtCLP(ingreso.monto)}).`
          : 'Úsalo si este mes recibiste un monto distinto (bono, licencia, sueldo variable).'}
      </p>
      <p className="muted tiny">Para agregar o renombrar ingresos fijos ve a Más › Presupuesto.</p>
    </Sheet>
  );
}

function IngresoExtraSheet({ ingreso, onClose }: { ingreso: Ingreso | null; onClose: () => void }) {
  const f = useFamilia();
  const { error } = useApp();
  const defFecha = f.mes === mesDe(hoy()) ? hoy() : primerDia(f.mes);
  const [fecha, setFecha] = useState(ingreso?.fecha ?? defFecha);
  const [desc, setDesc] = useState(ingreso?.descripcion ?? '');
  const [monto, setMonto] = useState<number | null>(ingreso?.monto ?? null);

  async function guardar() {
    if (!monto) return;
    try {
      await f.acciones.guardarIngreso({ ...(ingreso || {}), fecha, descripcion: desc.trim(), monto });
      onClose();
    } catch (e) {
      error(e);
    }
  }

  return (
    <Sheet titulo={ingreso ? 'Ingreso extra' : 'Nuevo ingreso extra'} onClose={onClose} pie={
      <>
        {ingreso && <button className="btn danger" onClick={() => { if (confirm('¿Eliminar este ingreso?')) { f.acciones.eliminarIngreso(ingreso); onClose(); } }}>Eliminar</button>}
        <button className="btn primary" disabled={!monto} onClick={guardar}>Guardar</button>
      </>
    }>
      <MontoInput value={monto} onChange={setMonto} grande autoFocus={!ingreso} />
      <Campo label="Descripción"><input className="input" value={desc} onChange={(e) => setDesc(e.target.value)} placeholder="Bono, venta, devolución…" /></Campo>
      <Campo label="Fecha"><input className="input" type="date" value={fecha} onChange={(e) => e.target.value && setFecha(e.target.value)} /></Campo>
    </Sheet>
  );
}
