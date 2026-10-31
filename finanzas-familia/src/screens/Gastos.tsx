import { useMemo, useState } from 'react';
import { Avatar, Cargando, EMOJI_TIPO, Vacio } from '../components/ui';
import { useFamilia } from '../data/store';
import { nombreCategoria } from '../lib/calc';
import { fmtCLP, fmtFechaLarga, nombreMes } from '../lib/format';
import type { Gasto } from '../lib/types';
import { GastoForm } from './GastoForm';
import { Encabezado, useNav } from './Shell';

export function Gastos() {
  const f = useFamilia();
  const { filtroCategoria, setFiltroCategoria } = useNav();
  const [persona, setPersona] = useState('');
  const [busca, setBusca] = useState('');
  const [editar, setEditar] = useState<Gasto | null>(null);

  const lista = useMemo(() => {
    const q = busca.trim().toLowerCase();
    return f.gastos
      .filter((g) => !filtroCategoria || g.categoriaId === filtroCategoria)
      .filter((g) => !persona || g.creadoPor === persona)
      .filter((g) => !q || g.descripcion.toLowerCase().includes(q) || nombreCategoria(f.settings, g.categoriaId).toLowerCase().includes(q))
      .sort((a, b) => b.fecha.localeCompare(a.fecha) || b.creadoEn - a.creadoEn);
  }, [f.gastos, f.settings, filtroCategoria, persona, busca]);

  const porDia = useMemo(() => {
    const m = new Map<string, Gasto[]>();
    for (const g of lista) m.set(g.fecha, [...(m.get(g.fecha) || []), g]);
    return [...m.entries()];
  }, [lista]);

  const total = lista.reduce((s, g) => s + g.monto, 0);
  const tipoDe = (id: string) => f.settings.categorias.find((c) => c.id === id)?.tipo;
  const personas = f.members.length > 1 ? f.members : [];

  return (
    <>
      <Encabezado />
      <div className="content">
        <div className="card">
          <div className="row between">
            <div>
              <div className="muted small">Gastado en {nombreMes(f.mes).toLowerCase()}{filtroCategoria ? ` · ${nombreCategoria(f.settings, filtroCategoria)}` : ''}</div>
              <div className="num" style={{ fontSize: 24, fontWeight: 750 }}>{fmtCLP(total)}</div>
            </div>
            <span className="badge">{lista.length} {lista.length === 1 ? 'registro' : 'registros'}</span>
          </div>
        </div>

        <div className="stack tight">
          <input className="input" type="search" placeholder="Buscar descripción o categoría…" value={busca} onChange={(e) => setBusca(e.target.value)} />
          <div className="chips">
            <select className="chip" value={filtroCategoria} onChange={(e) => setFiltroCategoria(e.target.value)} style={{ appearance: 'auto' }}>
              <option value="">Todas las categorías</option>
              {f.settings.categorias.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
            </select>
            {personas.length > 0 && <button className={'chip' + (!persona ? ' on' : '')} onClick={() => setPersona('')}>Todos</button>}
            {personas.map((m) => (
              <button key={m.uid} className={'chip' + (persona === m.uid ? ' on' : '')} onClick={() => setPersona(m.uid)}>{m.nombre.split(' ')[0]}</button>
            ))}
          </div>
        </div>

        {f.cargando ? <Cargando /> : porDia.length === 0 ? (
          <Vacio icono="🧾" texto={filtroCategoria || persona || busca ? 'No hay gastos con ese filtro.' : 'Aún no hay gastos este mes. Toca “+ Gasto” para registrar el primero.'} />
        ) : porDia.map(([fecha, gs]) => (
          <div key={fecha}>
            <div className="group-h">
              <span>{fmtFechaLarga(fecha)}</span>
              <span className="num">{fmtCLP(gs.reduce((s, g) => s + g.monto, 0))}</span>
            </div>
            <div className="card flush list">
              {gs.map((g) => {
                const tipo = tipoDe(g.categoriaId);
                return (
                  <button key={g.id} className="item" onClick={() => setEditar(g)}>
                    <span className="icono">{tipo ? EMOJI_TIPO[tipo] : '❔'}</span>
                    <span className="grow">
                      <div className="t ellipsis">{g.descripcion || nombreCategoria(f.settings, g.categoriaId)}</div>
                      <div className="s ellipsis">
                        {nombreCategoria(f.settings, g.categoriaId)}
                        {g.medioPago ? ` · ${g.medioPago}` : ''}
                        {g.deudaId ? ' · cuota' : ''}
                        {g.boletaId ? ' · boleta' : ''}
                        {g.adjuntoId ? ' · 📎' : ''}
                      </div>
                    </span>
                    <span className="stack tight" style={{ alignItems: 'flex-end', gap: 2 }}>
                      <span className="num m">{fmtCLP(g.monto)}</span>
                      {f.members.length > 1 && <Avatar nombre={g.creadoPorNombre} sm />}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
      {editar && <GastoForm gasto={editar} onClose={() => setEditar(null)} />}
    </>
  );
}
