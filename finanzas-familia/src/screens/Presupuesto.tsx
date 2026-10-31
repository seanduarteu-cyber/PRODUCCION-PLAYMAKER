import { useState } from 'react';
import { Campo, EMOJI_TIPO, MontoInput, Sheet, SubPagina } from '../components/ui';
import { useApp, useFamilia } from '../data/store';
import { nuevoId } from '../lib/defaults';
import { fmtCLP, fmtPct } from '../lib/format';
import { TIPOS, type Categoria, type IngresoFijo, type Settings, type Tipo } from '../lib/types';

export function Presupuesto({ onBack }: { onBack: () => void }) {
  const f = useFamilia();
  const { error, avisar } = useApp();
  const [cat, setCat] = useState<Categoria | 'nueva' | null>(null);
  const [ing, setIng] = useState<IngresoFijo | 'nuevo' | null>(null);
  const [metas, setMetas] = useState(false);
  const s = f.settings;

  const guardar = async (ns: Settings, msg = 'Presupuesto actualizado') => {
    try {
      await f.acciones.guardarSettings(ns);
      avisar(msg);
    } catch (e) {
      error(e);
    }
  };

  const totalPres = s.categorias.reduce((a, c) => a + (c.presupuesto || 0), 0);
  const totalIng = s.ingresosFijos.reduce((a, i) => a + i.monto, 0);

  return (
    <SubPagina titulo="Presupuesto" onBack={onBack}>
      <div className="kpis">
        <div className="kpi"><div className="k">Ingresos fijos / mes</div><div className="v num">{fmtCLP(totalIng)}</div></div>
        <div className={'kpi' + (totalPres > totalIng ? ' warn' : '')}><div className="k">Presupuestado / mes</div><div className="v num">{fmtCLP(totalPres)}</div></div>
      </div>
      <p className="muted tiny">Las cuotas de deudas se suman solas a lo presupuestado según su proyección.</p>

      <div className="card flush">
        <div className="card-title" style={{ padding: '14px 14px 0' }}>
          <h2>Ingresos fijos mensuales</h2>
          <button className="link small" onClick={() => setIng('nuevo')}>+ Agregar</button>
        </div>
        <div className="list">
          {s.ingresosFijos.map((i) => (
            <button key={i.id} className="item" onClick={() => setIng(i)}>
              <span className="grow t">{i.nombre}</span>
              <span className="num m">{fmtCLP(i.monto)}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="card">
        <div className="card-title">
          <h2>Metas (% del ingreso)</h2>
          <button className="link small" onClick={() => setMetas(true)}>Editar</button>
        </div>
        <div className="row wrap" style={{ gap: 6 }}>
          {TIPOS.map((t) => <span key={t} className="badge">{EMOJI_TIPO[t]} {t} {fmtPct(s.metas[t] || 0)}</span>)}
        </div>
      </div>

      {TIPOS.map((t) => {
        const cs = s.categorias.filter((c) => c.tipo === t);
        return (
          <div key={t}>
            <div className="group-h"><span>{EMOJI_TIPO[t]} {t}</span><span className="num">{fmtCLP(cs.reduce((a, c) => a + (c.presupuesto || 0), 0))}</span></div>
            <div className="card flush list">
              {cs.length === 0 && <p className="muted small" style={{ padding: 14 }}>Sin categorías.</p>}
              {cs.map((c) => (
                <button key={c.id} className="item" onClick={() => setCat(c)}>
                  <span className="grow t">{c.nombre}</span>
                  <span className={'num ' + (c.presupuesto ? 'm' : 'muted small')}>{c.presupuesto ? fmtCLP(c.presupuesto) : 'Sin presupuesto'}</span>
                </button>
              ))}
            </div>
          </div>
        );
      })}
      <button className="btn soft block" onClick={() => setCat('nueva')}>+ Nueva categoría</button>

      {cat && <CategoriaSheet categoria={cat === 'nueva' ? null : cat} onClose={() => setCat(null)} onSave={(c, borrar) => {
        const otras = s.categorias.filter((x) => x.id !== c.id);
        if (borrar) return guardar({ ...s, categorias: otras }, 'Categoría eliminada');
        const idx = s.categorias.findIndex((x) => x.id === c.id);
        const categorias = idx >= 0 ? s.categorias.map((x) => (x.id === c.id ? c : x)) : [...s.categorias, c];
        return guardar({ ...s, categorias });
      }} />}
      {ing && <IngresoFijoEdit ingreso={ing === 'nuevo' ? null : ing} onClose={() => setIng(null)} onSave={(i, borrar) => {
        const otros = s.ingresosFijos.filter((x) => x.id !== i.id);
        if (borrar) return guardar({ ...s, ingresosFijos: otros }, 'Ingreso eliminado');
        const existe = s.ingresosFijos.some((x) => x.id === i.id);
        return guardar({ ...s, ingresosFijos: existe ? s.ingresosFijos.map((x) => (x.id === i.id ? i : x)) : [...s.ingresosFijos, i] });
      }} />}
      {metas && <MetasSheet onClose={() => setMetas(false)} onSave={(m) => guardar({ ...s, metas: m })} />}
    </SubPagina>
  );
}

function CategoriaSheet({ categoria, onClose, onSave }: { categoria: Categoria | null; onClose: () => void; onSave: (c: Categoria, borrar?: boolean) => void }) {
  const [nombre, setNombre] = useState(categoria?.nombre ?? '');
  const [tipo, setTipo] = useState<Tipo>(categoria?.tipo ?? 'Esencial');
  const [presupuesto, setPresupuesto] = useState<number | null>(categoria?.presupuesto ?? null);
  const listo = () => {
    if (!nombre.trim()) return;
    onSave({ id: categoria?.id ?? nuevoId(), nombre: nombre.trim(), tipo, presupuesto: presupuesto || null });
    onClose();
  };
  return (
    <Sheet titulo={categoria ? 'Editar categoría' : 'Nueva categoría'} onClose={onClose} pie={
      <>
        {categoria && <button className="btn danger" onClick={() => {
          if (confirm('¿Eliminar la categoría? Los gastos que la usan quedarán como “Sin categoría”.')) { onSave(categoria, true); onClose(); }
        }}>Eliminar</button>}
        <button className="btn primary" disabled={!nombre.trim()} onClick={listo}>Guardar</button>
      </>
    }>
      <Campo label="Nombre"><input className="input" value={nombre} onChange={(e) => setNombre(e.target.value)} autoFocus={!categoria} /></Campo>
      <Campo label="Tipo">
        <div className="chips">{TIPOS.map((t) => <button key={t} className={'chip' + (tipo === t ? ' on' : '')} onClick={() => setTipo(t)}>{EMOJI_TIPO[t]} {t}</button>)}</div>
      </Campo>
      <Campo label="Presupuesto mensual" ayuda="Déjalo vacío si no quieres asignar un monto."><MontoInput value={presupuesto} onChange={setPresupuesto} /></Campo>
    </Sheet>
  );
}

function IngresoFijoEdit({ ingreso, onClose, onSave }: { ingreso: IngresoFijo | null; onClose: () => void; onSave: (i: IngresoFijo, borrar?: boolean) => void }) {
  const [nombre, setNombre] = useState(ingreso?.nombre ?? '');
  const [monto, setMonto] = useState<number | null>(ingreso?.monto ?? null);
  return (
    <Sheet titulo={ingreso ? 'Ingreso fijo' : 'Nuevo ingreso fijo'} onClose={onClose} pie={
      <>
        {ingreso && <button className="btn danger" onClick={() => { if (confirm('¿Eliminar este ingreso fijo?')) { onSave(ingreso, true); onClose(); } }}>Eliminar</button>}
        <button className="btn primary" disabled={!nombre.trim()} onClick={() => { onSave({ ajustes: {}, ...(ingreso || {}), id: ingreso?.id ?? nuevoId(), nombre: nombre.trim(), monto: monto || 0 }); onClose(); }}>Guardar</button>
      </>
    }>
      <Campo label="Nombre"><input className="input" value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="Sueldo, pensión, arriendo recibido…" /></Campo>
      <Campo label="Monto mensual"><MontoInput value={monto} onChange={setMonto} grande /></Campo>
    </Sheet>
  );
}

function MetasSheet({ onClose, onSave }: { onClose: () => void; onSave: (m: Record<Tipo, number>) => void }) {
  const f = useFamilia();
  const [m, setM] = useState<Record<Tipo, string>>(() =>
    Object.fromEntries(TIPOS.map((t) => [t, String(Math.round((f.settings.metas[t] || 0) * 100))])) as Record<Tipo, string>);
  const suma = TIPOS.reduce((a, t) => a + (parseFloat(m[t]) || 0), 0);
  return (
    <Sheet titulo="Metas por tipo" onClose={onClose} pie={
      <button className="btn primary" onClick={() => { onSave(Object.fromEntries(TIPOS.map((t) => [t, (parseFloat(m[t]) || 0) / 100])) as Record<Tipo, number>); onClose(); }}>Guardar</button>
    }>
      <p className="muted small">Regla sugerida: 60% esencial, 20% deudas, 10% prescindible y 10% ahorro.</p>
      {TIPOS.map((t) => (
        <div key={t} className="row between">
          <span>{EMOJI_TIPO[t]} {t}</span>
          <span className="row" style={{ gap: 6 }}>
            <input className="input num right" style={{ width: 90 }} inputMode="numeric" value={m[t]} onChange={(e) => setM({ ...m, [t]: e.target.value.replace(/[^0-9.,]/g, '') })} />%
          </span>
        </div>
      ))}
      <p className={'small ' + (Math.round(suma) === 100 ? 'muted' : 'neg')}>Suma: {suma}%</p>
    </Sheet>
  );
}
