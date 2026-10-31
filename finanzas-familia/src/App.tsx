import { useEffect, useState } from 'react';
import { Cargando } from './components/ui';
import type { Backend } from './data/backend';
import { VISTA_PREVIA } from './data/config';
import { AppProvider, cargarBackend, FamiliaProvider, useApp } from './data/store';
import { descartarInvitacion, invitacionPendiente } from './lib/enlace';
import { ClaveCreada, EstadoFamiliaView, Ingreso, NuevaContrasena, SinFamilia } from './screens/Inicio';
import { Shell } from './screens/Shell';

export default function App() {
  const [backend, setBackend] = useState<Backend | null>(null);
  const [err, setErr] = useState('');
  useEffect(() => {
    cargarBackend()
      .then(async (b) => {
        if (VISTA_PREVIA && b.mode === 'local') {
          const { sembrarEjemplo } = await import('./data/semilla');
          await sembrarEjemplo(b).catch((e) => console.error('semilla', e));
        }
        setBackend(b);
      })
      .catch((e) => setErr(String(e?.message || e)));
  }, []);
  if (err) return <div className="center-page"><p className="error-text">No se pudo iniciar: {err}</p></div>;
  if (!backend) return <div className="center-page"><Cargando /></div>;
  return (
    <AppProvider backend={backend}>
      <Raiz />
      <Avisos />
    </AppProvider>
  );
}

function Raiz() {
  const { backend, user, families, familyId, elegirFamilia } = useApp();
  const [recuperando, setRecuperando] = useState(false);
  useEffect(() => backend.onRecuperacion?.(() => setRecuperando(true)), [backend]);
  const [claveNueva, setClaveNueva] = useState<{ id: string; clave: string; nombre: string } | null>(null);
  const [agregando, setAgregando] = useState(false);
  const [creando, setCreando] = useState(false);
  const [invitacion, setInvitacion] = useState(invitacionPendiente);

  if (user === undefined) return <div className="center-page"><Cargando /></div>;
  if (recuperando && user) return <NuevaContrasena onListo={() => setRecuperando(false)} />;
  if (!user) return <Ingreso />;
  if (families === undefined) return <div className="center-page"><Cargando /></div>;

  if (claveNueva) {
    return <ClaveCreada nombre={claveNueva.nombre} clave={claveNueva.clave} onListo={() => {
      elegirFamilia(claveNueva.id);
      setClaveNueva(null);
      setAgregando(false);
      setCreando(false);
      descartarInvitacion();
      setInvitacion(null);
    }} />;
  }

  if (creando || !families.length || !familyId || agregando || invitacion) {
    const cerrar = () => {
      setInvitacion(null);
      setAgregando(false);
    };
    return (
      <SinFamilia
        invitacion={invitacion}
        onCreando={setCreando}
        onCreada={setClaveNueva}
        onUnido={cerrar}
        onCancelar={families.length ? () => { descartarInvitacion(); cerrar(); } : undefined}
      />
    );
  }

  return (
    <FamiliaProvider key={familyId} familyId={familyId} renderEstado={(e) => <EstadoFamiliaView estado={e} />}>
      <Shell agregarFamilia={() => setAgregando(true)} />
    </FamiliaProvider>
  );
}

function Avisos() {
  const { avisos } = useApp();
  return (
    <div className="toasts" aria-live="polite">
      {avisos.map((a) => <div key={a.id} className={'toast ' + a.tipo}>{a.texto}</div>)}
    </div>
  );
}
