// Crear o editar categorías, también desde los formularios de gasto, boleta y deuda.
import { useState } from 'react';
import { useApp, useFamilia } from '../data/store';
import { nuevoId } from '../lib/defaults';
import { TIPOS, type Categoria, type Tipo } from '../lib/types';
import { Campo, CategoriaSelect, EMOJI_TIPO, MontoInput, Sheet } from './ui';

export function CategoriaSheet({ categoria, onClose, onSave }: { categoria: Categoria | null; onClose: () => void; onSave: (c: Categoria, borrar?: boolean) => void }) {
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
      <Campo label="Nombre">
        <input className="input" value={nombre} onChange={(e) => setNombre(e.target.value)} autoFocus={!categoria} maxLength={60}
          placeholder="Ej: Mascotas, Colegio, Bencina" onKeyDown={(e) => e.key === 'Enter' && listo()} />
      </Campo>
      <Campo label="Tipo">
        <div className="chips">{TIPOS.map((t) => <button key={t} className={'chip' + (tipo === t ? ' on' : '')} onClick={() => setTipo(t)}>{EMOJI_TIPO[t]} {t}</button>)}</div>
      </Campo>
      <Campo label="Presupuesto mensual" ayuda="Opcional. Déjalo vacío si no quieres asignar un monto."><MontoInput value={presupuesto} onChange={setPresupuesto} /></Campo>
    </Sheet>
  );
}

const normalizar = (s: string) => s.trim().toLocaleLowerCase('es').normalize('NFD').replace(/[̀-ͯ]/g, '');

/** Selector de categoría con la opción de crear una nueva ahí mismo. */
export function CategoriaCampo({ value, onChange, label = 'Categoría', ayuda }: {
  value: string; onChange: (id: string) => void; label?: string; ayuda?: string;
}) {
  const f = useFamilia();
  const { error, avisar } = useApp();
  const [nueva, setNueva] = useState(false);

  function crear(c: Categoria) {
    const igual = f.settings.categorias.find((x) => normalizar(x.nombre) === normalizar(c.nombre));
    if (igual) {
      onChange(igual.id);
      avisar(`Ya tenías la categoría “${igual.nombre}”. Quedó elegida.`, 'info');
      return;
    }
    f.acciones.guardarSettings({ ...f.settings, categorias: [...f.settings.categorias, c] })
      .then(() => avisar(`Categoría “${c.nombre}” creada`))
      .catch(error);
    onChange(c.id);
  }

  return (
    <div className="field">
      <div className="field-h">
        <label>{label}</label>
        <button type="button" className="link small" onClick={() => setNueva(true)}>＋ Nueva categoría</button>
      </div>
      <CategoriaSelect settings={f.settings} value={value} onChange={onChange} onNueva={() => setNueva(true)} />
      {ayuda && <div className="help">{ayuda}</div>}
      {nueva && <CategoriaSheet categoria={null} onClose={() => setNueva(false)} onSave={crear} />}
    </div>
  );
}
