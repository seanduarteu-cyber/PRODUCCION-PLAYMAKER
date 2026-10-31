import { createContext, useContext, useState, type ReactNode } from 'react';
import { Icon, MesNav, Sheet } from '../components/ui';
import { useApp, useFamilia } from '../data/store';
import { resumenBoletas } from '../lib/calc';
import { hoy } from '../lib/format';
import { Boletas } from './Boletas';
import { Cuotas } from './Cuotas';
import { GastoForm } from './GastoForm';
import { Gastos } from './Gastos';
import { DemoBanner } from './Inicio';
import { Mas } from './Mas';
import { Resumen } from './Resumen';

export type Tab = 'resumen' | 'gastos' | 'boletas' | 'cuotas' | 'mas';

interface NavCtx {
  irA: (t: Tab, opts?: { categoria?: string }) => void;
  filtroCategoria: string;
  setFiltroCategoria: (c: string) => void;
  agregarFamilia: () => void;
}
const Nav = createContext<NavCtx | null>(null);
export const useNav = () => useContext(Nav)!;

export function Shell({ agregarFamilia }: { agregarFamilia: () => void }) {
  const [tab, setTab] = useState<Tab>('resumen');
  const [filtroCategoria, setFiltroCategoria] = useState('');
  const [nuevoGasto, setNuevoGasto] = useState(false);
  const f = useFamilia();
  const vencidas = resumenBoletas(f.boletas, hoy()).vencidas;

  const irA = (t: Tab, opts?: { categoria?: string }) => {
    setFiltroCategoria(opts?.categoria ?? '');
    setTab(t);
    window.scrollTo(0, 0);
  };

  const tabs: [Tab, string, ReactNode, number?][] = [
    ['resumen', 'Resumen', Icon.home],
    ['gastos', 'Gastos', Icon.list],
    ['boletas', 'Boletas', Icon.bill, vencidas],
    ['cuotas', 'Cuotas', Icon.cal],
    ['mas', 'Más', Icon.more],
  ];

  return (
    <Nav.Provider value={{ irA, filtroCategoria, setFiltroCategoria, agregarFamilia }}>
      <DemoBanner />
      <div className="app">
        {tab === 'resumen' && <Resumen />}
        {tab === 'gastos' && <Gastos />}
        {tab === 'boletas' && <Boletas />}
        {tab === 'cuotas' && <Cuotas />}
        {tab === 'mas' && <Mas />}
      </div>
      {(tab === 'resumen' || tab === 'gastos') && (
        <button className="fab" onClick={() => setNuevoGasto(true)}>{Icon.plus} Gasto</button>
      )}
      <div className="tabbar">
        <nav>
          {tabs.map(([t, label, icon, badge]) => (
            <button key={t} className={tab === t ? 'on' : ''} onClick={() => irA(t)} aria-current={tab === t ? 'page' : undefined}>
              {icon}
              {label}
              {!!badge && <span className="dot">{badge}</span>}
            </button>
          ))}
        </nav>
      </div>
      {nuevoGasto && <GastoForm onClose={() => setNuevoGasto(false)} />}
    </Nav.Provider>
  );
}

/** Encabezado con selector de familia y de mes. */
export function Encabezado({ conMes = true, derecha }: { conMes?: boolean; derecha?: ReactNode }) {
  const { family, mes, setMes } = useFamilia();
  const [abierto, setAbierto] = useState(false);
  return (
    <div className="topbar">
      <div className="row between">
        <button className="familia-btn" onClick={() => setAbierto(true)}>
          <span>{family.nombre}</span>
          <span style={{ width: 18, height: 18, display: 'inline-block', color: 'var(--muted)' }}>{Icon.down}</span>
        </button>
        {conMes ? <MesNav mes={mes} setMes={setMes} /> : derecha}
      </div>
      {abierto && <SelectorFamilia onClose={() => setAbierto(false)} />}
    </div>
  );
}

function SelectorFamilia({ onClose }: { onClose: () => void }) {
  const { families, familyId, elegirFamilia } = useApp();
  const { agregarFamilia } = useNav();
  return (
    <Sheet titulo="Mis familias" onClose={onClose}>
      <p className="muted small">Cada familia es un centro de costos separado y privado.</p>
      <div className="card flush list">
        {(families || []).map((f) => (
          <button key={f.id} className="item" onClick={() => { elegirFamilia(f.id); onClose(); }}>
            <span className="icono">🏠</span>
            <span className="grow">
              <div className="t">{f.nombre}</div>
              <div className="s">{f.rol === 'admin' ? 'Administrador' : 'Miembro'}</div>
            </span>
            {f.id === familyId && <span style={{ width: 22, color: 'var(--accent)' }}>{Icon.check}</span>}
          </button>
        ))}
      </div>
      <button className="btn soft block" onClick={() => { onClose(); agregarFamilia(); }}>{Icon.plus} Crear o unirme a otra familia</button>
    </Sheet>
  );
}
