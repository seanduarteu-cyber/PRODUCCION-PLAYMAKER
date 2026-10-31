import { useEffect, useMemo, useState } from 'react';
import { Campo, CategoriaSelect, Cargando, Icon, MontoInput, Seg, Sheet, Vacio } from '../components/ui';
import { useApp, useFamilia } from '../data/store';
import { nombreCategoria, pagadoBoleta, resumenBoletas, saldoBoleta, situacionBoleta } from '../lib/calc';
import { fmtCLP, fmtFecha, hoy } from '../lib/format';
import { comprimirFoto } from '../lib/imagen';
import type { Boleta } from '../lib/types';
import { Encabezado } from './Shell';

type Filtro = 'pendientes' | 'pagadas' | 'todas';

export function Boletas() {
  const f = useFamilia();
  const [filtro, setFiltro] = useState<Filtro>('pendientes');
  const [ver, setVer] = useState<string | null>(null);
  const [nueva, setNueva] = useState(false);
  const h = hoy();
  const res = resumenBoletas(f.boletas, h);

  const lista = useMemo(() => {
    const xs = f.boletas.filter((b) =>
      filtro === 'todas' ? true : filtro === 'pendientes' ? b.estado === 'pendiente' : b.estado !== 'pendiente');
    return xs.sort((a, b) => (filtro === 'pendientes' ? a.vencimiento.localeCompare(b.vencimiento) : b.vencimiento.localeCompare(a.vencimiento)));
  }, [f.boletas, filtro]);

  const boleta = ver ? f.boletas.find((b) => b.id === ver) : null;

  return (
    <>
      <Encabezado conMes={false} derecha={<button className="btn sm primary" onClick={() => setNueva(true)}>{Icon.plus} Boleta</button>} />
      <div className="content">
        <div className="kpis" style={{ gridTemplateColumns: '1fr 1fr 1fr' }}>
          <div className="kpi"><div className="k">Pendiente</div><div className="v num">{fmtCLP(res.pendiente)}</div></div>
          <div className={'kpi' + (res.vencido ? ' danger' : '')}><div className="k">Vencido</div><div className="v num">{fmtCLP(res.vencido)}</div></div>
          <div className={'kpi' + (res.vencidas ? ' danger' : '')}><div className="k">N° vencidas</div><div className="v num">{res.vencidas}</div></div>
        </div>
        <Seg opciones={[['pendientes', 'Por pagar'], ['pagadas', 'Pagadas'], ['todas', 'Todas']]} valor={filtro} onChange={setFiltro} />
        <p className="muted tiny">Anota cada boleta al llegar. Si no la pagas, sigue apareciendo “por pagar” en los meses siguientes. Si llega una nueva que incluye el saldo anterior o haces un convenio, marca la antigua como traspasada.</p>

        {f.cargando ? <Cargando /> : lista.length === 0 ? (
          <Vacio icono="📬" texto={filtro === 'pendientes' ? 'No hay boletas por pagar. ¡Bien!' : 'No hay boletas aquí.'}>
            <button className="btn soft" onClick={() => setNueva(true)}>{Icon.plus} Agregar boleta</button>
          </Vacio>
        ) : (
          <div className="card flush list">
            {lista.map((b) => {
              const s = situacionBoleta(b, h);
              const saldo = saldoBoleta(b);
              return (
                <button key={b.id} className="item" onClick={() => setVer(b.id)}>
                  <span className="grow">
                    <div className="t ellipsis">{nombreCategoria(f.settings, b.categoriaId)}{b.detalle ? ` · ${b.detalle}` : ''}</div>
                    <div className="s">Vence {fmtFecha(b.vencimiento)}{b.adjuntoId ? ' · 📎' : ''}</div>
                    <span className={'badge ' + s.nivel} style={{ marginTop: 4, whiteSpace: 'normal' }}>{s.texto}</span>
                  </span>
                  <span className="stack tight" style={{ alignItems: 'flex-end', gap: 0 }}>
                    <span className="num m">{fmtCLP(b.estado === 'pendiente' ? saldo : b.monto)}</span>
                    {b.estado === 'pendiente' && saldo !== b.monto && <span className="tiny muted num">de {fmtCLP(b.monto)}</span>}
                  </span>
                </button>
              );
            })}
          </div>
        )}
      </div>
      {nueva && <BoletaForm onClose={() => setNueva(false)} />}
      {boleta && <BoletaDetalle boleta={boleta} onClose={() => setVer(null)} />}
    </>
  );
}

export function BoletaForm({ boleta, onClose }: { boleta?: Boleta; onClose: () => void }) {
  const f = useFamilia();
  const { error, avisar } = useApp();
  const [monto, setMonto] = useState<number | null>(boleta?.monto ?? null);
  const [vencimiento, setVencimiento] = useState(boleta?.vencimiento ?? hoy());
  const [categoriaId, setCategoriaId] = useState(boleta?.categoriaId ?? '');
  const [detalle, setDetalle] = useState(boleta?.detalle ?? '');
  const [foto, setFoto] = useState<string | null>(null);
  const [fotoCambiada, setFotoCambiada] = useState(false);
  const [err, setErr] = useState('');

  useEffect(() => {
    if (boleta?.adjuntoId) f.acciones.leerAdjunto(boleta.adjuntoId).then(setFoto).catch(() => undefined);
  }, [boleta?.adjuntoId, f.acciones]);

  async function guardar() {
    if (!monto) return setErr('Ingresa el monto.');
    if (!f.settings.categorias.some((c) => c.id === categoriaId)) return setErr('Elige una categoría.');
    try {
      let adjuntoId = boleta?.adjuntoId;
      if (fotoCambiada) {
        if (adjuntoId) f.acciones.eliminarAdjunto(adjuntoId);
        adjuntoId = foto ? await f.acciones.guardarAdjunto(foto) : undefined;
      }
      await f.acciones.guardarBoleta({ ...(boleta || {}), monto, vencimiento, categoriaId, detalle: detalle.trim(), adjuntoId });
      avisar(boleta ? 'Boleta actualizada' : 'Boleta agregada');
      onClose();
    } catch (e) {
      error(e);
    }
  }

  return (
    <Sheet titulo={boleta ? 'Editar boleta' : 'Nueva boleta'} onClose={onClose} pie={<button className="btn primary" onClick={guardar}>Guardar</button>}>
      <MontoInput value={monto} onChange={setMonto} grande autoFocus={!boleta} />
      <Campo label="Categoría"><CategoriaSelect settings={f.settings} value={categoriaId} onChange={setCategoriaId} /></Campo>
      <Campo label="Detalle"><input className="input" value={detalle} onChange={(e) => setDetalle(e.target.value)} placeholder="Ej: periodo 26-09 al 26-10, N° cliente…" /></Campo>
      <Campo label="Vencimiento"><input className="input" type="date" value={vencimiento} onChange={(e) => e.target.value && setVencimiento(e.target.value)} /></Campo>
      {foto ? (
        <>
          <img className="thumb" src={foto} alt="Foto de la boleta" />
          <button className="btn sm danger" onClick={() => { setFoto(null); setFotoCambiada(true); }}>{Icon.trash} Quitar foto</button>
        </>
      ) : (
        <label className="foto-btn">
          {Icon.camera} Foto de la boleta (opcional)
          <input type="file" accept="image/*" capture="environment" onChange={async (e) => {
            const file = e.target.files?.[0];
            if (!file) return;
            try {
              setFoto(await comprimirFoto(file));
              setFotoCambiada(true);
            } catch (e2) {
              error(e2);
            }
          }} />
        </label>
      )}
      {err && <p className="error-text">{err}</p>}
    </Sheet>
  );
}

function BoletaDetalle({ boleta: b, onClose }: { boleta: Boleta; onClose: () => void }) {
  const f = useFamilia();
  const { avisar } = useApp();
  const [modo, setModo] = useState<'ver' | 'pagar' | 'editar'>('ver');
  const [foto, setFoto] = useState<string | null>(null);
  const s = situacionBoleta(b, hoy());
  const saldo = saldoBoleta(b);

  useEffect(() => {
    if (b.adjuntoId) f.acciones.leerAdjunto(b.adjuntoId).then(setFoto).catch(() => undefined);
  }, [b.adjuntoId, f.acciones]);

  if (modo === 'editar') return <BoletaForm boleta={b} onClose={onClose} />;
  if (modo === 'pagar') return <PagoBoleta boleta={b} onClose={onClose} />;

  return (
    <Sheet titulo={nombreCategoria(f.settings, b.categoriaId)} onClose={onClose} pie={
      b.estado === 'pendiente'
        ? <button className="btn primary" onClick={() => setModo('pagar')}>Registrar pago</button>
        : <button className="btn" onClick={() => { f.acciones.cambiarEstadoBoleta(b, 'pendiente'); avisar('Boleta reabierta', 'info'); }}>Volver a pendiente</button>
    }>
      <div className="card stack tight">
        <div className="row between"><span className="muted">Monto</span><span className="num" style={{ fontWeight: 700 }}>{fmtCLP(b.monto)}</span></div>
        <div className="row between"><span className="muted">Pagado</span><span className="num">{fmtCLP(pagadoBoleta(b))}</span></div>
        <div className="row between"><span className="muted">Saldo pendiente</span><span className="num" style={{ fontWeight: 700 }}>{fmtCLP(saldo)}</span></div>
        <div className="row between"><span className="muted">Vencimiento</span><span>{fmtFecha(b.vencimiento)}</span></div>
        {b.detalle && <div className="row between top"><span className="muted">Detalle</span><span className="right" style={{ maxWidth: '65%' }}>{b.detalle}</span></div>}
        <span className={'badge ' + s.nivel} style={{ alignSelf: 'flex-start', whiteSpace: 'normal' }}>{s.texto}</span>
      </div>
      {b.pagos.length > 0 && (
        <div className="stack tight">
          <h3>Pagos</h3>
          <div className="card flush list">
            {b.pagos.map((p) => (
              <div key={p.gastoId} className="item" style={{ cursor: 'default' }}>
                <span className="grow">{fmtFecha(p.fecha)}</span>
                <span className="num m">{fmtCLP(p.monto)}</span>
              </div>
            ))}
          </div>
          <p className="muted tiny">Cada pago aparece también en Gastos. Para deshacer un pago, elimínalo desde Gastos.</p>
        </div>
      )}
      {foto && <img className="thumb" src={foto} alt="Foto de la boleta" />}
      <div className="btn-row">
        <button className="btn sm" onClick={() => setModo('editar')}>Editar</button>
        {b.estado === 'pendiente' && (
          <button className="btn sm" onClick={() => {
            if (confirm('¿Marcar como traspasada? Úsalo si llegó una boleta nueva que incluye este saldo o si hiciste un convenio. Ya no se contará como por pagar.')) {
              f.acciones.cambiarEstadoBoleta(b, 'traspasada');
              onClose();
            }
          }}>Traspasada</button>
        )}
        <button className="btn sm danger" onClick={() => {
          if (confirm('¿Eliminar esta boleta? Los pagos ya registrados se mantienen como gastos.')) {
            f.acciones.eliminarBoleta(b, f.gastos);
            onClose();
          }
        }}>Eliminar</button>
      </div>
    </Sheet>
  );
}

function PagoBoleta({ boleta: b, onClose }: { boleta: Boleta; onClose: () => void }) {
  const f = useFamilia();
  const { error, avisar } = useApp();
  const saldo = saldoBoleta(b);
  const [monto, setMonto] = useState<number | null>(saldo);
  const [fecha, setFecha] = useState(hoy());
  const [medioPago, setMedioPago] = useState('');
  const [cerrar, setCerrar] = useState(false);
  const parcial = (monto || 0) < saldo;

  async function pagar() {
    if (!monto) return;
    try {
      await f.acciones.pagarBoleta(b, { fecha, monto, medioPago: medioPago || undefined, cerrar: !parcial || cerrar });
      avisar(parcial && !cerrar ? `Pago parcial registrado. Faltan ${fmtCLP(saldo - monto)}` : 'Boleta pagada');
      onClose();
    } catch (e) {
      error(e);
    }
  }

  return (
    <Sheet titulo="Registrar pago" onClose={onClose} pie={<button className="btn primary" onClick={pagar} disabled={!monto}>Pagar {monto ? fmtCLP(monto) : ''}</button>}>
      <p className="muted small">{nombreCategoria(f.settings, b.categoriaId)} · saldo {fmtCLP(saldo)}</p>
      <MontoInput value={monto} onChange={setMonto} grande autoFocus />
      <div className="grid2">
        <Campo label="Fecha de pago"><input className="input" type="date" value={fecha} onChange={(e) => e.target.value && setFecha(e.target.value)} /></Campo>
        <Campo label="Medio de pago">
          <select className="input" value={medioPago} onChange={(e) => setMedioPago(e.target.value)}>
            <option value="">—</option>
            {f.settings.mediosPago.map((m) => <option key={m}>{m}</option>)}
          </select>
        </Campo>
      </div>
      {parcial && (
        <div className="stack tight">
          <label className="check"><input type="radio" checked={!cerrar} onChange={() => setCerrar(false)} /> Pago parcial: queda debiendo {fmtCLP(saldo - (monto || 0))}</label>
          <label className="check"><input type="radio" checked={cerrar} onChange={() => setCerrar(true)} /> Pagada (me cobraron menos / descuento)</label>
        </div>
      )}
      <p className="muted tiny">El pago se registra como gasto en la categoría de la boleta.</p>
    </Sheet>
  );
}
