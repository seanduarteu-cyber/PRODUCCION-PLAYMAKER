import { useState, type ReactNode } from 'react';
import { Icon } from '../components/ui';
import { useApp, useFamilia } from '../data/store';
import { Exportar } from './Exportar';
import { FamiliaPagina } from './FamiliaPagina';
import { Presupuesto } from './Presupuesto';
import { Privacidad } from './Privacidad';
import { Encabezado } from './Shell';

type Pagina = 'presupuesto' | 'familia' | 'exportar' | 'privacidad' | null;

export function Mas() {
  const f = useFamilia();
  const { backend, user } = useApp();
  const [pagina, setPagina] = useState<Pagina>(null);
  const volver = () => setPagina(null);

  if (pagina === 'presupuesto') return <Presupuesto onBack={volver} />;
  if (pagina === 'familia') return <FamiliaPagina onBack={volver} />;
  if (pagina === 'exportar') return <Exportar onBack={volver} />;
  if (pagina === 'privacidad') return <Privacidad onBack={volver} />;

  const item = (p: Pagina, icono: ReactNode, t: string, s: string) => (
    <button className="item" onClick={() => setPagina(p)}>
      <span className="icono" style={{ color: 'var(--accent)' }}><span style={{ width: 22, height: 22, display: 'block' }}>{icono}</span></span>
      <span className="grow"><div className="t">{t}</div><div className="s">{s}</div></span>
      <span style={{ width: 18, color: 'var(--muted)' }}>{Icon.chevron}</span>
    </button>
  );

  return (
    <>
      <Encabezado conMes={false} />
      <div className="content">
        <div className="card flush list">
          {item('presupuesto', Icon.pie, 'Presupuesto y categorías', 'Montos mensuales, ingresos fijos y metas')}
          {item('familia', Icon.users, 'Familia y miembros', `${f.members.length} ${f.members.length === 1 ? 'miembro' : 'miembros'} · invitar a tu pareja`)}
          {item('exportar', Icon.download, 'Descargar Excel o PDF', 'Informe del mes o del año · importar tu planilla')}
          {item('privacidad', Icon.shield, 'Privacidad y seguridad', 'Cómo se protegen tus datos')}
        </div>
        <div className="card flush list">
          <div className="item" style={{ cursor: 'default' }}>
            <span className="avatar">{user?.nombre.slice(0, 1).toUpperCase()}</span>
            <span className="grow"><div className="t">{user?.nombre}</div><div className="s">{user?.email}</div></span>
          </div>
          <button className="item" onClick={() => { if (confirm('¿Cerrar sesión en este teléfono?')) backend.signOut(); }}>
            <span className="icono"><span style={{ width: 22, height: 22, display: 'block' }}>{Icon.logout}</span></span>
            <span className="grow t">Cerrar sesión</span>
          </button>
        </div>
        <p className="muted tiny" style={{ textAlign: 'center' }}>Finanzas Familia · v1.0 · {backend.mode === 'local' ? 'modo demostración' : `datos cifrados en ${backend.mode === 'supabase' ? 'Supabase' : 'Firebase'}`}</p>
      </div>
    </>
  );
}
