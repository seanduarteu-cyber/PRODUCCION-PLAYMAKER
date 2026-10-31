import { useEffect, useRef, useState, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { fmtNum, nombreMes, parseMonto, sumarMeses } from '../lib/format';
import type { Categoria, MesKey, Settings, Tipo } from '../lib/types';
import { TIPOS } from '../lib/types';

// ---------------- Íconos ----------------
const p = (d: string) => <path d={d} fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round" />;
export const Icon = {
  home: <svg viewBox="0 0 24 24">{p('M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z')}</svg>,
  list: <svg viewBox="0 0 24 24">{p('M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01')}</svg>,
  bill: <svg viewBox="0 0 24 24">{p('M6 2h12v20l-3-2-3 2-3-2-3 2zM9 7h6M9 11h6M9 15h4')}</svg>,
  cal: <svg viewBox="0 0 24 24">{p('M4 5h16v16H4zM4 10h16M9 3v4M15 3v4')}</svg>,
  more: <svg viewBox="0 0 24 24">{p('M5 12h.01M12 12h.01M19 12h.01')}</svg>,
  plus: <svg viewBox="0 0 24 24">{p('M12 5v14M5 12h14')}</svg>,
  close: <svg viewBox="0 0 24 24">{p('M6 6l12 12M18 6 6 18')}</svg>,
  back: <svg viewBox="0 0 24 24">{p('M15 5l-7 7 7 7')}</svg>,
  chevron: <svg viewBox="0 0 24 24">{p('M9 5l7 7-7 7')}</svg>,
  down: <svg viewBox="0 0 24 24">{p('M6 9l6 6 6-6')}</svg>,
  camera: <svg viewBox="0 0 24 24">{p('M4 8h3l2-3h6l2 3h3v11H4zM12 17a4 4 0 1 0 0-8 4 4 0 0 0 0 8z')}</svg>,
  file: <svg viewBox="0 0 24 24">{p('M14 3H6v18h12V7zM14 3v4h4M9 13h6M9 17h6')}</svg>,
  share: <svg viewBox="0 0 24 24">{p('M12 3v13M7 8l5-5 5 5M5 13v8h14v-8')}</svg>,
  copy: <svg viewBox="0 0 24 24">{p('M9 9h11v11H9zM5 15H4V4h11v1')}</svg>,
  users: <svg viewBox="0 0 24 24">{p('M16 20v-1a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v1M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM22 20v-1a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8')}</svg>,
  lock: <svg viewBox="0 0 24 24">{p('M5 11h14v10H5zM8 11V7a4 4 0 0 1 8 0v4')}</svg>,
  pie: <svg viewBox="0 0 24 24">{p('M21 12A9 9 0 1 1 12 3v9zM15 3.5A9 9 0 0 1 20.5 9H15z')}</svg>,
  upload: <svg viewBox="0 0 24 24">{p('M12 16V4M7 9l5-5 5 5M4 20h16')}</svg>,
  download: <svg viewBox="0 0 24 24">{p('M12 4v12M7 11l5 5 5-5M4 20h16')}</svg>,
  logout: <svg viewBox="0 0 24 24">{p('M15 4h4v16h-4M10 8l-4 4 4 4M6 12h11')}</svg>,
  check: <svg viewBox="0 0 24 24">{p('M5 12l5 5L20 7')}</svg>,
  shield: <svg viewBox="0 0 24 24">{p('M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z')}</svg>,
  trash: <svg viewBox="0 0 24 24">{p('M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3')}</svg>,
};

// ---------------- Botón "atrás" de Android ----------------
// Mientras haya hojas o subpantallas abiertas se mantiene UNA entrada extra en
// el historial. El botón atrás cierra solo la de más arriba (y vuelve a poner
// la entrada si quedan otras). Las operaciones de historial se agrupan después
// del render para no mezclar back() y pushState() en el mismo instante.
const pila: { id: number; cerrar: () => void }[] = [];
let guardia = false;
let ignorar = 0;
let programado = false;
let sec = 0;

function sincronizarHistorial() {
  if (import.meta.env.VITE_VISTA_PREVIA) return;
  if (programado) return;
  programado = true;
  setTimeout(() => {
    programado = false;
    if (ignorar > 0) return; // hay un back() en curso; se vuelve a sincronizar al llegar popstate
    if (pila.length > 0 && !guardia) {
      history.pushState({ ff: true }, '');
      guardia = true;
    } else if (pila.length === 0 && guardia) {
      guardia = false;
      ignorar++;
      history.back();
    }
  }, 0);
}

if (typeof window !== 'undefined') {
  window.addEventListener('popstate', () => {
    if (ignorar > 0) {
      ignorar--;
      sincronizarHistorial();
      return;
    }
    if (!guardia) return;
    guardia = false;
    pila.pop()?.cerrar();
    sincronizarHistorial();
  });
}

export function useBotonAtras(activo: boolean, cerrar: () => void) {
  const ref = useRef(cerrar);
  ref.current = cerrar;
  useEffect(() => {
    if (!activo) return;
    const id = ++sec;
    pila.push({ id, cerrar: () => ref.current() });
    sincronizarHistorial();
    return () => {
      const i = pila.findIndex((x) => x.id === id);
      if (i >= 0) pila.splice(i, 1);
      sincronizarHistorial();
    };
  }, [activo]);
}

// ---------------- Hoja inferior ----------------
export function Sheet({ titulo, onClose, children, pie }: { titulo: ReactNode; onClose: () => void; children: ReactNode; pie?: ReactNode }) {
  useBotonAtras(true, onClose);
  useEffect(() => {
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = prev;
    };
  }, []);
  return createPortal(
    <div className="sheet-bg" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="sheet" role="dialog" aria-modal="true">
        <div className="sheet-h">
          <h2>{titulo}</h2>
          <button className="iconbtn" onClick={onClose} aria-label="Cerrar">{Icon.close}</button>
        </div>
        <div className="sheet-b">{children}</div>
        {pie && <div className="sheet-f">{pie}</div>}
      </div>
    </div>,
    document.body,
  );
}

export function SubPagina({ titulo, onBack, children, accion }: { titulo: string; onBack: () => void; children: ReactNode; accion?: ReactNode }) {
  useBotonAtras(true, onBack);
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  return (
    <>
      <div className="topbar">
        <div className="row between">
          <div className="row" style={{ gap: 4 }}>
            <button className="iconbtn" onClick={onBack} aria-label="Volver" style={{ marginLeft: -10 }}>{Icon.back}</button>
            <h1 style={{ fontSize: 19 }}>{titulo}</h1>
          </div>
          {accion}
        </div>
      </div>
      <div className="content">{children}</div>
    </>
  );
}

// ---------------- Campos ----------------
export function Campo({ label, children, ayuda }: { label: string; children: ReactNode; ayuda?: ReactNode }) {
  return (
    <div className="field">
      <label>{label}</label>
      {children}
      {ayuda && <div className="help">{ayuda}</div>}
    </div>
  );
}

export function MontoInput({ value, onChange, grande, autoFocus, placeholder, id }: {
  value: number | null; onChange: (n: number | null) => void; grande?: boolean; autoFocus?: boolean; placeholder?: string; id?: string;
}) {
  const [txt, setTxt] = useState(value == null || value === 0 ? '' : fmtNum(value));
  const ultimo = useRef(value);
  useEffect(() => {
    if (value !== ultimo.current) {
      ultimo.current = value;
      setTxt(value == null || value === 0 ? '' : fmtNum(value));
    }
  }, [value]);
  return (
    <input
      id={id}
      className={'input num' + (grande ? ' monto-input' : '')}
      inputMode="numeric"
      autoComplete="off"
      placeholder={placeholder ?? '$ 0'}
      autoFocus={autoFocus}
      value={txt ? '$ ' + txt : ''}
      onChange={(e) => {
        const digits = e.target.value.replace(/[^0-9]/g, '');
        const n = digits ? parseMonto(digits) : null;
        ultimo.current = n;
        setTxt(n == null ? '' : fmtNum(n));
        onChange(n);
      }}
    />
  );
}

export function CategoriaSelect({ settings, value, onChange, id }: { settings: Settings; value: string; onChange: (id: string) => void; id?: string }) {
  const grupos = TIPOS.map((t) => [t, settings.categorias.filter((c) => c.tipo === t)] as [Tipo, Categoria[]]).filter(([, cs]) => cs.length);
  const existe = settings.categorias.some((c) => c.id === value);
  return (
    <select id={id} className="input" value={existe ? value : ''} onChange={(e) => onChange(e.target.value)}>
      {!existe && <option value="">Elige una categoría…</option>}
      {grupos.map(([t, cs]) => (
        <optgroup key={t} label={t}>
          {cs.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </optgroup>
      ))}
    </select>
  );
}

export function MesNav({ mes, setMes }: { mes: MesKey; setMes: (m: MesKey) => void }) {
  const ref = useRef<HTMLInputElement>(null);
  return (
    <div className="mesnav">
      <button onClick={() => setMes(sumarMeses(mes, -1))} aria-label="Mes anterior">‹</button>
      <button className="label" onClick={() => ref.current?.showPicker?.()}>
        {nombreMes(mes)}
        <input ref={ref} type="month" value={mes} onChange={(e) => e.target.value && setMes(e.target.value)}
          style={{ position: 'absolute', opacity: 0, width: 1, height: 1, pointerEvents: 'none' }} tabIndex={-1} aria-hidden />
      </button>
      <button onClick={() => setMes(sumarMeses(mes, 1))} aria-label="Mes siguiente">›</button>
    </div>
  );
}

export function Barra({ valor, max, marca }: { valor: number; max: number; marca?: number }) {
  const pct = max > 0 ? Math.min(100, (valor / max) * 100) : valor > 0 ? 100 : 0;
  const nivel = max > 0 && valor > max ? 'danger' : pct >= 90 ? 'warn' : '';
  return (
    <div className="bar">
      <i className={nivel} style={{ width: `${pct}%` }} />
      {marca != null && <b style={{ left: `${Math.min(100, marca * 100)}%` }} />}
    </div>
  );
}

export function Avatar({ nombre, sm }: { nombre: string; sm?: boolean }) {
  const ini = nombre.trim().split(/\s+/).filter((s) => /\p{L}/u.test(s[0] ?? '')).slice(0, 2).map((s) => s[0].toUpperCase()).join('') || '?';
  return <span className={'avatar' + (sm ? ' sm' : '')} title={nombre}>{ini}</span>;
}

export function Vacio({ icono, texto, children }: { icono: string; texto: string; children?: ReactNode }) {
  return (
    <div className="empty">
      <div className="icono">{icono}</div>
      <p>{texto}</p>
      {children}
    </div>
  );
}

export function Cargando() {
  return <div style={{ padding: 40 }}><div className="spinner" /></div>;
}

export function Seg<T extends string>({ opciones, valor, onChange }: { opciones: [T, string][]; valor: T; onChange: (v: T) => void }) {
  return (
    <div className="seg">
      {opciones.map(([v, l]) => <button key={v} className={v === valor ? 'on' : ''} onClick={() => onChange(v)}>{l}</button>)}
    </div>
  );
}

export const EMOJI_TIPO: Record<Tipo, string> = { Esencial: '🏠', Deudas: '💳', Prescindible: '🛍️', Ahorro: '🐷' };
