import { useMemo, useState } from 'react';
import { Campo, CategoriaSelect, Cargando, Icon, MontoInput, Sheet, Vacio } from '../components/ui';
import { useApp, useFamilia } from '../data/store';
import {
  cuotaDeuda, etiquetaCuota, mesesParaPagar, proyeccion, restanteDeuda, totalIngresos, ultimoMesDeuda,
} from '../lib/calc';
import { CATEGORIA_CUOTAS } from '../lib/defaults';
import { fmtCLP, fmtFecha, fmtPct, hoy, mesActual, nombreMes, nombreMesCorto, sumarMeses } from '../lib/format';
import { TIPOS_DEUDA, type Deuda, type MesKey, type TipoDeuda } from '../lib/types';
import { Encabezado } from './Shell';

export function Cuotas() {
  const f = useFamilia();
  const { avisar } = useApp();
  const [editar, setEditar] = useState<Deuda | 'nueva' | null>(null);
  const [pagar, setPagar] = useState<Deuda | null>(null);
  const mes = f.mes;
  const ingresos = totalIngresos(f.settings, f.ingresos, mes);

  const delMes = useMemo(() => f.deudas
    .map((d) => ({ d, cuota: cuotaDeuda(d, mes), pago: d.pagos?.[mes] }))
    .filter((x) => x.cuota > 0 || x.pago)
    .sort((a, b) => Number(!!a.pago) - Number(!!b.pago) || b.cuota - a.cuota), [f.deudas, mes]);
  const total = delMes.reduce((s, x) => s + x.cuota, 0);
  const pagado = delMes.reduce((s, x) => s + (x.pago?.monto || 0), 0);
  const pendientes = delMes.filter((x) => !x.pago && x.cuota > 0);
  const pct = ingresos ? total / ingresos : 0;

  const proy = useMemo(() => proyeccion(f.deudas, mes, 12), [f.deudas, mes]);
  const vigentes = useMemo(() => {
    const actual = mesActual();
    return f.deudas
      .map((d) => ({ d, restante: restanteDeuda(d, actual), fin: ultimoMesDeuda(d) }))
      .sort((a, b) => (b.d.tasaMensual || 0) - (a.d.tasaMensual || 0) || (b.restante ?? Infinity) - (a.restante ?? Infinity));
  }, [f.deudas]);
  const conTasa = vigentes.filter((x) => (x.d.tasaMensual || 0) > 0 && (x.restante ?? 1) > 0);
  const deudaTotal = vigentes.reduce((s, x) => s + (x.restante || 0), 0);

  async function pagarTodas() {
    if (!confirm(`¿Marcar ${pendientes.length} cuotas como pagadas hoy por ${fmtCLP(total - pagado)}?`)) return;
    for (const x of pendientes) await f.acciones.pagarCuota(x.d, mes, { fecha: hoy(), monto: x.cuota });
    avisar('Cuotas pagadas');
  }

  return (
    <>
      <Encabezado />
      <div className="content">
        <div className="kpis">
          <div className="kpi"><div className="k">Cuotas del mes</div><div className="v num">{fmtCLP(total)}</div></div>
          <div className={'kpi' + (pct > 0.3 ? ' warn' : '')}><div className="k">% del ingreso</div><div className="v num">{fmtPct(pct)}</div></div>
          <div className="kpi"><div className="k">Pagado</div><div className="v num">{fmtCLP(pagado)}</div></div>
          <div className="kpi"><div className="k">Deuda total restante</div><div className="v num">{fmtCLP(deudaTotal)}</div></div>
        </div>
        {pct > 0.3 && <div className="alert warn">Las cuotas superan el 30% del ingreso de este mes. Conviene evaluar renegociar o consolidar.</div>}

        {f.cargando ? <Cargando /> : (
          <>
            <div className="card flush">
              <div className="card-title" style={{ padding: '14px 14px 0' }}>
                <h2>Cuotas de {nombreMes(mes).toLowerCase()}</h2>
                {pendientes.length > 1 && <button className="link small" onClick={pagarTodas}>Pagar todas</button>}
              </div>
              <div className="list">
                {delMes.length === 0 && <p className="muted small" style={{ padding: 14 }}>No hay cuotas este mes.</p>}
                {delMes.map(({ d, cuota, pago }) => (
                  <div key={d.id} className="item" style={{ cursor: 'default' }}>
                    <span className="grow" onClick={() => setEditar(d)} style={{ cursor: 'pointer' }}>
                      <div className="t ellipsis">{d.acreedor}</div>
                      <div className="s">{etiquetaCuota(d, mes) || TIPOS_DEUDA[d.tipo]}{pago ? ` · pagada ${fmtFecha(pago.fecha)}` : ''}</div>
                    </span>
                    <span className="num m">{fmtCLP(pago?.monto ?? cuota)}</span>
                    {pago ? (
                      <button className="btn sm" title="Deshacer pago" onClick={() => {
                        if (confirm('¿Deshacer el pago de esta cuota? Se eliminará el gasto asociado.')) f.acciones.deshacerPagoCuota(d, mes);
                      }}><span style={{ color: 'var(--ok)', width: 18 }}>{Icon.check}</span></button>
                    ) : (
                      <button className="btn sm soft" onClick={() => setPagar(d)}>Pagar</button>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <div className="card flush">
              <div className="card-title" style={{ padding: '14px 14px 0' }}>
                <h2>Deudas y compras en cuotas</h2>
                <button className="link small" onClick={() => setEditar('nueva')}>+ Agregar</button>
              </div>
              <div className="list">
                {vigentes.length === 0 && (
                  <Vacio icono="💳" texto="Agrega créditos, convenios, préstamos o compras en cuotas para ver cuánto pagarás cada mes." />
                )}
                {vigentes.map(({ d, restante, fin }) => {
                  const prioridad = conTasa.findIndex((x) => x.d.id === d.id);
                  return (
                    <button key={d.id} className="item" onClick={() => setEditar(d)}>
                      <span className="grow">
                        <div className="t ellipsis">{d.acreedor}</div>
                        <div className="s">
                          {TIPOS_DEUDA[d.tipo]} · {fmtCLP(d.montoCuota)}/mes · {fin ? `termina ${nombreMesCorto(fin).toLowerCase()}` : 'sin término'}
                        </div>
                        {prioridad >= 0 && <span className={'badge ' + (prioridad === 0 ? 'danger' : '')} style={{ marginTop: 4 }}>Prioridad {prioridad + 1} · tasa {fmtPct(d.tasaMensual || 0)}</span>}
                      </span>
                      <span className="stack tight" style={{ alignItems: 'flex-end', gap: 0 }}>
                        <span className="num m">{restante == null ? '—' : fmtCLP(restante)}</span>
                        <span className="tiny muted">{restante == null ? 'sin término' : restante === 0 ? 'pagada' : 'restante'}</span>
                      </span>
                    </button>
                  );
                })}
              </div>
              {conTasa.length > 1 && <p className="muted tiny" style={{ padding: '0 14px 12px' }}>Estrategia avalancha: paga la cuota mínima en todas y todo dinero extra a la de Prioridad 1 (mayor tasa).</p>}
            </div>

            {proy.filas.length > 0 && (
              <div className="card">
                <div className="card-title"><h2>Proyección de cuotas</h2><span className="muted tiny">12 meses</span></div>
                <div className="tabla-wrap">
                  <table className="tabla">
                    <thead>
                      <tr><th>Acreedor</th>{proy.meses.map((m) => <th key={m}>{nombreMesCorto(m)}</th>)}<th>Total</th></tr>
                    </thead>
                    <tbody>
                      {proy.filas.map((r) => (
                        <tr key={r.deuda.id}>
                          <td className="ellipsis" style={{ maxWidth: 130 }}>{r.deuda.acreedor}</td>
                          {r.valores.map((v, i) => <td key={i} className="num">{v ? fmtCLP(v) : '–'}</td>)}
                          <td className="num">{fmtCLP(r.total)}</td>
                        </tr>
                      ))}
                      <tr className="total">
                        <td>Total</td>
                        {proy.totales.map((v, i) => {
                          const ing = totalIngresos(f.settings, [], proy.meses[i]);
                          return <td key={i} className={'num' + (ing && v / ing > 0.3 ? ' alto' : '')}>{fmtCLP(v)}</td>;
                        })}
                        <td className="num">{fmtCLP(proy.total)}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <p className="muted tiny" style={{ marginTop: 8 }}>Resaltado: meses en que las cuotas superan ~30% del ingreso fijo. Prepárate con anticipación.</p>
              </div>
            )}
          </>
        )}
      </div>
      {editar && <DeudaForm deuda={editar === 'nueva' ? undefined : editar} onClose={() => setEditar(null)} />}
      {pagar && <PagoCuota deuda={pagar} mes={mes} onClose={() => setPagar(null)} />}
    </>
  );
}

function PagoCuota({ deuda, mes, onClose }: { deuda: Deuda; mes: MesKey; onClose: () => void }) {
  const f = useFamilia();
  const { error, avisar } = useApp();
  const [monto, setMonto] = useState<number | null>(cuotaDeuda(deuda, mes));
  const [fecha, setFecha] = useState(hoy());
  const [medioPago, setMedioPago] = useState('');
  return (
    <Sheet titulo={`Pagar cuota · ${deuda.acreedor}`} onClose={onClose} pie={
      <button className="btn primary" disabled={!monto} onClick={async () => {
        try {
          await f.acciones.pagarCuota(deuda, mes, { fecha, monto: monto || 0, medioPago: medioPago || undefined });
          avisar('Cuota pagada');
          onClose();
        } catch (e) {
          error(e);
        }
      }}>Registrar pago</button>
    }>
      <p className="muted small">{etiquetaCuota(deuda, mes)} de {nombreMes(mes).toLowerCase()}</p>
      <MontoInput value={monto} onChange={setMonto} grande />
      <div className="grid2">
        <Campo label="Fecha de pago"><input className="input" type="date" value={fecha} onChange={(e) => e.target.value && setFecha(e.target.value)} /></Campo>
        <Campo label="Medio de pago">
          <select className="input" value={medioPago} onChange={(e) => setMedioPago(e.target.value)}>
            <option value="">—</option>
            {f.settings.mediosPago.map((m) => <option key={m}>{m}</option>)}
          </select>
        </Campo>
      </div>
      <p className="muted tiny">Se registra como gasto y se cuenta en el mes de la cuota.</p>
    </Sheet>
  );
}

function DeudaForm({ deuda, onClose }: { deuda?: Deuda; onClose: () => void }) {
  const f = useFamilia();
  const { error, avisar } = useApp();
  const [acreedor, setAcreedor] = useState(deuda?.acreedor ?? '');
  const [tipo, setTipo] = useState<TipoDeuda>(deuda?.tipo ?? 'credito');
  const [categoriaId, setCategoriaId] = useState(deuda?.categoriaId ?? (f.settings.categorias.some((c) => c.id === CATEGORIA_CUOTAS) ? CATEGORIA_CUOTAS : ''));
  const [montoCuota, setMontoCuota] = useState<number | null>(deuda?.montoCuota ?? null);
  const [sinTermino, setSinTermino] = useState(deuda ? deuda.numCuotas == null : false);
  const [numCuotas, setNumCuotas] = useState<number>(deuda?.numCuotas ?? 12);
  const [primerMes, setPrimerMes] = useState(deuda?.primerMes ?? f.mes);
  const [tasa, setTasa] = useState(deuda?.tasaMensual ? String(+(deuda.tasaMensual * 100).toFixed(3)) : '');
  const [saldo, setSaldo] = useState<number | null>(deuda?.montoTotal ?? null);
  const [notas, setNotas] = useState(deuda?.notas ?? '');
  const [ajustes, setAjustes] = useState<Record<MesKey, number>>(deuda?.ajustes ?? {});
  const [cerradaDesde, setCerradaDesde] = useState(deuda?.cerradaDesde ?? '');
  const [ajMes, setAjMes] = useState(f.mes);
  const [ajMonto, setAjMonto] = useState<number | null>(null);
  const [err, setErr] = useState('');

  const tasaNum = tasa ? parseFloat(tasa.replace(',', '.')) / 100 : 0;
  const nper = saldo && montoCuota ? mesesParaPagar(saldo, tasaNum, montoCuota) : undefined;

  async function guardar() {
    if (!acreedor.trim()) return setErr('Escribe el nombre (acreedor o compra).');
    if (!montoCuota) return setErr('Ingresa el valor de la cuota.');
    if (!f.settings.categorias.some((c) => c.id === categoriaId)) return setErr('Elige una categoría.');
    try {
      await f.acciones.guardarDeuda({
        ...(deuda || {}),
        acreedor: acreedor.trim(), tipo, categoriaId, montoCuota, numCuotas: sinTermino ? null : Math.max(1, numCuotas), primerMes,
        tasaMensual: tasaNum || undefined, montoTotal: saldo || undefined, notas: notas.trim() || undefined, ajustes,
        cerradaDesde: cerradaDesde || undefined,
      });
      avisar(deuda ? 'Deuda actualizada' : 'Deuda agregada');
      onClose();
    } catch (e) {
      error(e);
    }
  }

  return (
    <Sheet titulo={deuda ? 'Editar deuda / cuotas' : 'Nueva deuda o compra en cuotas'} onClose={onClose} pie={
      <>
        {deuda && <button className="btn danger" onClick={() => {
          if (confirm('¿Eliminar esta deuda y su proyección? Los pagos ya registrados se mantienen como gastos.')) {
            f.acciones.eliminarDeuda(deuda);
            onClose();
          }
        }}>Eliminar</button>}
        <button className="btn primary" onClick={guardar}>Guardar</button>
      </>
    }>
      <Campo label="Acreedor o compra"><input className="input" value={acreedor} onChange={(e) => setAcreedor(e.target.value)} placeholder="Ej: Convenio agua, Tarjeta, Préstamo tío" /></Campo>
      <div className="grid2">
        <Campo label="Tipo">
          <select className="input" value={tipo} onChange={(e) => setTipo(e.target.value as TipoDeuda)}>
            {Object.entries(TIPOS_DEUDA).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </Campo>
        <Campo label="Valor cuota"><MontoInput value={montoCuota} onChange={setMontoCuota} /></Campo>
      </div>
      <div className="grid2">
        <Campo label="Primera cuota"><input className="input" type="month" value={primerMes} onChange={(e) => e.target.value && setPrimerMes(e.target.value)} /></Campo>
        <Campo label="N° de cuotas">
          <input className="input num" type="number" inputMode="numeric" min={1} disabled={sinTermino} value={sinTermino ? '' : numCuotas} onChange={(e) => setNumCuotas(parseInt(e.target.value || '0', 10))} />
        </Campo>
      </div>
      <label className="check"><input type="checkbox" checked={sinTermino} onChange={(e) => setSinTermino(e.target.checked)} /> Sin término definido (se cobra cada mes)</label>
      {!sinTermino && montoCuota && numCuotas > 0 && (
        <p className="muted small">Última cuota: {nombreMes(sumarMeses(primerMes, numCuotas - 1))} · total {fmtCLP(montoCuota * numCuotas)}</p>
      )}
      <Campo label="Categoría del presupuesto" ayuda="Las cuotas se suman a lo presupuestado de esta categoría cada mes.">
        <CategoriaSelect settings={f.settings} value={categoriaId} onChange={setCategoriaId} />
      </Campo>

      <details className="card">
        <summary style={{ cursor: 'pointer', fontWeight: 600 }}>Más opciones (tasa, saldo, cuotas variables)</summary>
        <div className="stack" style={{ marginTop: 12 }}>
          <div className="grid2">
            <Campo label="Tasa interés mensual %"><input className="input num" inputMode="decimal" value={tasa} onChange={(e) => setTasa(e.target.value)} placeholder="Ej: 2,5" /></Campo>
            <Campo label="Saldo / monto total"><MontoInput value={saldo} onChange={setSaldo} /></Campo>
          </div>
          {nper !== undefined && (
            <p className="small">{nper == null ? <span className="neg">La cuota no cubre el interés: la deuda no baja.</span> : `Con esta cuota y tasa se paga en ~${nper} meses (interés del mes: ${fmtCLP((saldo || 0) * tasaNum)}).`}</p>
          )}
          <Campo label="Notas"><textarea className="input" value={notas} onChange={(e) => setNotas(e.target.value)} /></Campo>

          <div className="stack tight">
            <div className="label muted small" style={{ fontWeight: 600 }}>Cuota distinta en un mes (UF, variable, fin de crédito = 0)</div>
            {Object.entries(ajustes).sort().map(([m, v]) => (
              <div key={m} className="row between small">
                <span>{nombreMes(m)}</span>
                <span className="row"><span className="num">{fmtCLP(v)}</span>
                  <button className="iconbtn" aria-label="Quitar" onClick={() => { const a = { ...ajustes }; delete a[m]; setAjustes(a); }}>{Icon.close}</button>
                </span>
              </div>
            ))}
            <div className="row">
              <input className="input" type="month" value={ajMes} onChange={(e) => setAjMes(e.target.value)} style={{ flex: 1.2 }} />
              <div style={{ flex: 1 }}><MontoInput value={ajMonto} onChange={setAjMonto} placeholder="$ cuota" /></div>
              <button className="btn sm" onClick={() => { if (ajMes) { setAjustes({ ...ajustes, [ajMes]: ajMonto || 0 }); setAjMonto(null); } }}>Agregar</button>
            </div>
          </div>

          <Campo label="Deuda pagada / cerrada desde" ayuda="Si la pagaste antes de tiempo, desde este mes ya no se proyectan cuotas.">
            <input className="input" type="month" value={cerradaDesde} onChange={(e) => setCerradaDesde(e.target.value)} />
          </Campo>
        </div>
      </details>
      {err && <p className="error-text">{err}</p>}
    </Sheet>
  );
}
