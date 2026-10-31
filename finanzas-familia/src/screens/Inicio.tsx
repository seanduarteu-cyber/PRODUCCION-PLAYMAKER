import { useState } from 'react';
import { Campo, Icon } from '../components/ui';
import { fmtCodigo, mensajeError, normalizarCodigo } from '../data/backend';
import { crearFamiliaCifrada } from '../data/familias';
import { VISTA_PREVIA } from '../data/config';
import { useApp, type EstadoFamilia } from '../data/store';
import { compartirTexto, copiarTexto } from '../lib/compartir';
import { claveValida, fmtClave, guardarClave, normalizarClave } from '../lib/crypto';
import { descartarInvitacion, type InvitacionPendiente } from '../lib/enlace';

export function Logo({ size = 64 }: { size?: number }) {
  return (
    <svg className="logo" viewBox="0 0 512 512" width={size} height={size} aria-hidden="true">
      <rect width="512" height="512" rx="112" fill="#0e7458" />
      <path d="M256 92 418 222c6 5 9 12 9 19v161c0 13-11 24-24 24H109c-13 0-24-11-24-24V241c0-7 3-14 9-19z" fill="#ffffff" />
      <rect x="160" y="300" width="44" height="82" rx="10" fill="#0e7458" />
      <rect x="234" y="258" width="44" height="124" rx="10" fill="#0e7458" />
      <rect x="308" y="214" width="44" height="168" rx="10" fill="#f2b33d" />
    </svg>
  );
}

export function DemoBanner() {
  const { backend } = useApp();
  if (backend.mode !== 'local') return null;
  return (
    <div className="demo-banner">
      {VISTA_PREVIA
        ? 'Vista previa con datos de ejemplo. Lo que registres queda solo en este navegador.'
        : 'Modo demostración: los datos quedan solo en este dispositivo.'}
    </div>
  );
}

// ---------------- Ingreso / registro ----------------
export function Ingreso() {
  const { backend } = useApp();
  const demo = backend.mode === 'local';
  const [modo, setModo] = useState<'entrar' | 'crear' | 'olvide'>(demo ? 'crear' : 'entrar');
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [pass, setPass] = useState('');
  const [err, setErr] = useState('');
  const [info, setInfo] = useState('');
  const [ocupado, setOcupado] = useState(false);

  async function enviar(e: React.FormEvent) {
    e.preventDefault();
    setErr('');
    setInfo('');
    setOcupado(true);
    try {
      if (modo === 'entrar') await backend.signIn(email, pass);
      else if (modo === 'crear') {
        if (!nombre.trim()) throw new Error('Escribe tu nombre.');
        await backend.signUp(nombre, email, pass);
      } else {
        await backend.resetPassword(email);
        setInfo('Te enviamos un correo para crear una nueva contraseña.');
      }
    } catch (e2) {
      setErr(mensajeError(e2));
    } finally {
      setOcupado(false);
    }
  }

  async function google() {
    setErr('');
    try {
      await backend.signInGoogle();
    } catch (e2) {
      setErr(mensajeError(e2));
    }
  }

  return (
    <>
      <DemoBanner />
      <div className="center-page">
        <div className="brand">
          <Logo />
          <h1>Finanzas Familia</h1>
          <p>Gastos, boletas y cuotas de tu familia, en un solo lugar y en privado.</p>
        </div>

        {!demo && modo !== 'olvide' && (
          <>
            <button className="btn block" onClick={google} type="button">
              <svg viewBox="0 0 48 48" width="18" height="18"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z" /><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z" /><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z" /><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z" /></svg>
              Continuar con Google
            </button>
            <div className="divider">o con tu correo</div>
          </>
        )}

        <form className="stack" onSubmit={enviar}>
          {modo === 'crear' && (
            <Campo label="Tu nombre">
              <input className="input" autoComplete="name" value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="Ej: Daniela" />
            </Campo>
          )}
          <Campo label="Correo">
            <input className="input" type="email" autoComplete="email" inputMode="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="tu@correo.cl" required />
          </Campo>
          {!demo && modo !== 'olvide' && (
            <Campo label="Contraseña">
              <input className="input" type="password" autoComplete={modo === 'crear' ? 'new-password' : 'current-password'} value={pass} onChange={(e) => setPass(e.target.value)} minLength={6} required />
            </Campo>
          )}
          {err && <p className="error-text">{err}</p>}
          {info && <div className="alert ok">{info}</div>}
          <button className="btn primary block" disabled={ocupado}>
            {modo === 'entrar' ? 'Entrar' : modo === 'crear' ? 'Crear mi cuenta' : 'Enviar correo'}
          </button>
        </form>

        <div className="stack tight" style={{ alignItems: 'center' }}>
          {modo !== 'entrar' && <button className="link" onClick={() => setModo('entrar')}>Ya tengo cuenta: entrar</button>}
          {modo !== 'crear' && <button className="link" onClick={() => setModo('crear')}>Soy nuevo: crear cuenta</button>}
          {!demo && modo === 'entrar' && <button className="link muted" onClick={() => setModo('olvide')}>Olvidé mi contraseña</button>}
        </div>
      </div>
    </>
  );
}

// ---------------- Crear o unirse a una familia ----------------
export function SinFamilia({ onCreando, onCreada, onUnido, invitacion, onCancelar }: {
  onCreando: (si: boolean) => void;
  onCreada: (r: { id: string; clave: string; nombre: string }) => void;
  onUnido: () => void;
  invitacion?: InvitacionPendiente | null;
  onCancelar?: () => void;
}) {
  const { backend, user, elegirFamilia, avisar } = useApp();
  const [modo, setModo] = useState<'crear' | 'unirse'>(invitacion ? 'unirse' : 'crear');
  const [nombre, setNombre] = useState('');
  const [codigo, setCodigo] = useState(invitacion ? fmtCodigo(normalizarCodigo(invitacion.codigo)) : '');
  const [clave, setClave] = useState(invitacion?.clave ? fmtClave(invitacion.clave) : '');
  const [err, setErr] = useState('');
  const [ocupado, setOcupado] = useState(false);

  async function crear(e: React.FormEvent) {
    e.preventDefault();
    if (!user || !nombre.trim()) return;
    setOcupado(true);
    setErr('');
    onCreando(true);
    try {
      const r = await crearFamiliaCifrada(backend, user, nombre);
      onCreada({ ...r, nombre: nombre.trim() });
    } catch (e2) {
      onCreando(false);
      setErr(mensajeError(e2));
    } finally {
      setOcupado(false);
    }
  }

  async function unirse(e: React.FormEvent) {
    e.preventDefault();
    if (!user) return;
    if (normalizarCodigo(codigo).length !== 8) return setErr('El código tiene 8 caracteres (ej: ABCD-2345).');
    if (!claveValida(clave)) return setErr('La clave de la familia tiene 20 caracteres (ej: K7PD-3MXQ-9TRW-HZ2B-6NVC).');
    setOcupado(true);
    setErr('');
    try {
      const f = await backend.joinFamily(user, codigo);
      guardarClave(f.id, normalizarClave(clave));
      descartarInvitacion();
      elegirFamilia(f.id);
      avisar(`Te uniste a "${f.nombre}"`);
      onUnido();
    } catch (e2) {
      setErr(mensajeError(e2));
    } finally {
      setOcupado(false);
    }
  }

  return (
    <>
      <DemoBanner />
      <div className="center-page">
        <div className="brand">
          <Logo size={56} />
          <h1>Hola{user ? `, ${user.nombre.split(' ')[0]}` : ''}</h1>
          <p>Cada familia es un centro de costos privado: solo sus miembros pueden ver sus datos.</p>
        </div>
        <div className="seg">
          <button className={modo === 'crear' ? 'on' : ''} onClick={() => setModo('crear')}>Crear mi familia</button>
          <button className={modo === 'unirse' ? 'on' : ''} onClick={() => setModo('unirse')}>Tengo una invitación</button>
        </div>

        {modo === 'crear' ? (
          <form className="stack" onSubmit={crear}>
            <Campo label="Nombre de la familia" ayuda="Por ejemplo: Casa Duarte, Familia Pérez Soto.">
              <input className="input" value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="Casa …" maxLength={60} autoFocus />
            </Campo>
            {err && <p className="error-text">{err}</p>}
            <button className="btn primary block" disabled={ocupado || !nombre.trim()}>{ocupado ? 'Creando…' : 'Crear familia'}</button>
          </form>
        ) : (
          <form className="stack" onSubmit={unirse}>
            <Campo label="Código de invitación">
              <input className="input num" value={codigo} onChange={(e) => setCodigo(e.target.value.toUpperCase())} placeholder="ABCD-2345" autoCapitalize="characters" autoComplete="off" />
            </Campo>
            <Campo label="Clave de la familia" ayuda="Viene en el mensaje de invitación. Sin ella no se pueden leer los datos cifrados.">
              <input className="input num" value={clave} onChange={(e) => setClave(e.target.value.toUpperCase())} placeholder="XXXX-XXXX-XXXX-XXXX-XXXX" autoCapitalize="characters" autoComplete="off" />
            </Campo>
            {err && <p className="error-text">{err}</p>}
            <button className="btn primary block" disabled={ocupado}>{ocupado ? 'Uniéndome…' : 'Unirme a la familia'}</button>
          </form>
        )}
        <div className="stack tight" style={{ alignItems: 'center' }}>
          {onCancelar && <button className="link" onClick={() => { descartarInvitacion(); onCancelar(); }}>Volver</button>}
          <BotonSalir />
        </div>
      </div>
    </>
  );
}

function BotonSalir() {
  const { backend } = useApp();
  return <button className="link muted" onClick={() => backend.signOut()}>Cerrar sesión</button>;
}

// ---------------- Clave recién creada ----------------
export function ClaveCreada({ nombre, clave, onListo }: { nombre: string; clave: string; onListo: () => void }) {
  const { avisar } = useApp();
  const [ok, setOk] = useState(false);
  return (
    <div className="center-page">
      <div className="brand">
        <div className="icono" style={{ width: 56, height: 56, color: 'var(--accent)' }}>{Icon.shield}</div>
        <h1>Clave de “{nombre}”</h1>
        <p>Tus datos se cifran en el teléfono con esta clave antes de subirse a la nube. Nadie sin la clave puede leerlos, ni siquiera quien administra la app.</p>
      </div>
      <div className="clave-box">{fmtClave(clave)}</div>
      <div className="btn-row">
        <button className="btn" onClick={async () => avisar((await copiarTexto(fmtClave(clave))) ? 'Clave copiada' : 'No se pudo copiar', 'info')}>{Icon.copy} Copiar</button>
        <button className="btn" onClick={() => compartirTexto(`Clave de la familia "${nombre}": ${fmtClave(clave)}`, 'Clave de la familia')}>{Icon.share} Guardar</button>
      </div>
      <div className="alert warn">
        <div><b>Guárdala en un lugar seguro</b> (foto, nota o papel). La necesitarás para entrar desde otro teléfono. Si se pierde en todos los teléfonos, los datos no se pueden recuperar. Las invitaciones a tu familia la incluyen automáticamente.</div>
      </div>
      <label className="check"><input type="checkbox" checked={ok} onChange={(e) => setOk(e.target.checked)} /> Ya guardé la clave</label>
      <button className="btn primary block" disabled={!ok} onClick={onListo}>Continuar</button>
    </div>
  );
}

// ---------------- Estados de la familia ----------------
export function EstadoFamiliaView({ estado }: { estado: EstadoFamilia }) {
  const { backend, user, elegirFamilia, families, familyId } = useApp();
  const [clave, setClave] = useState('');
  const [err, setErr] = useState('');
  const [ocupado, setOcupado] = useState(false);

  if (estado.paso === 'cargando') {
    return <div className="center-page"><div className="spinner" /></div>;
  }
  const otras = (families || []).filter((f) => f.id !== familyId);

  if (estado.paso === 'sin-acceso') {
    return (
      <div className="center-page">
        <div className="brand">
          <div className="icono">{Icon.lock}</div>
          <h1>Sin acceso</h1>
          <p>Ya no eres miembro de esta familia o fue eliminada.</p>
        </div>
        <button className="btn primary block" onClick={async () => {
          if (user && familyId) await backend.forgetFamily(user, familyId);
          elegirFamilia(null);
        }}>Continuar</button>
      </div>
    );
  }

  if (estado.paso !== 'bloqueada') return null;
  const { doc, desbloquear } = estado;
  return (
    <>
      <DemoBanner />
      <div className="center-page">
        <div className="brand">
          <div className="icono" style={{ width: 56, height: 56, color: 'var(--accent)' }}>{Icon.lock}</div>
          <h1>{doc.nombre}</h1>
          <p>Ingresa la clave de la familia para ver los datos en este teléfono. Te la puede enviar otro miembro desde Más › Familia.</p>
        </div>
        <form className="stack" onSubmit={async (e) => {
          e.preventDefault();
          if (!claveValida(clave)) return setErr('La clave tiene 20 caracteres.');
          setOcupado(true);
          setErr('');
          const ok = await desbloquear(normalizarClave(clave));
          setOcupado(false);
          if (!ok) setErr('La clave no corresponde a esta familia.');
        }}>
          <Campo label="Clave de la familia">
            <input className="input num" value={clave} onChange={(e) => setClave(e.target.value.toUpperCase())} placeholder="XXXX-XXXX-XXXX-XXXX-XXXX" autoCapitalize="characters" autoComplete="off" autoFocus />
          </Campo>
          {err && <p className="error-text">{err}</p>}
          <button className="btn primary block" disabled={ocupado}>{ocupado ? 'Verificando…' : 'Desbloquear'}</button>
        </form>
        <div className="stack tight" style={{ alignItems: 'center' }}>
          {otras.map((f) => <button key={f.id} className="link" onClick={() => elegirFamilia(f.id)}>Ir a {f.nombre}</button>)}
          <BotonSalir />
        </div>
      </div>
    </>
  );
}
