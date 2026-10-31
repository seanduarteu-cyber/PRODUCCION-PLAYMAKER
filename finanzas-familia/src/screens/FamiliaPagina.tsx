import { useState } from 'react';
import { Avatar, Campo, Icon, Seg, Sheet, SubPagina } from '../components/ui';
import { DIAS_INVITACION, fmtCodigo, mensajeError } from '../data/backend';
import { useApp, useFamilia } from '../data/store';
import { compartirTexto, copiarTexto } from '../lib/compartir';
import { fmtClave } from '../lib/crypto';
import { textoInvitacion } from '../lib/enlace';
import type { Invite, Member, Rol } from '../lib/types';
import { useNav } from './Shell';

export function FamiliaPagina({ onBack }: { onBack: () => void }) {
  const f = useFamilia();
  const { backend, user, avisar, error, elegirFamilia } = useApp();
  const { agregarFamilia } = useNav();
  const [invitar, setInvitar] = useState(false);
  const [verClave, setVerClave] = useState(false);
  const [miembro, setMiembro] = useState<Member | null>(null);
  const [nombre, setNombre] = useState<string | null>(null);
  const admins = f.members.filter((m) => m.rol === 'admin').length;

  return (
    <SubPagina titulo="Familia" onBack={onBack}>
      <div className="card">
        <div className="row between">
          <div>
            <div className="muted small">Centro de costos</div>
            <h2 style={{ fontSize: 20 }}>{f.family.nombre}</h2>
          </div>
          {f.esAdmin && <button className="btn sm" onClick={() => setNombre(f.family.nombre)}>Renombrar</button>}
        </div>
      </div>

      <div className="card flush">
        <div className="card-title" style={{ padding: '14px 14px 0' }}>
          <h2>Miembros</h2>
          {f.esAdmin && <button className="link small" onClick={() => setInvitar(true)}>+ Invitar</button>}
        </div>
        <div className="list">
          {f.members.map((m) => (
            <button key={m.uid} className="item" onClick={() => f.esAdmin && m.uid !== user?.uid && setMiembro(m)} style={{ cursor: f.esAdmin && m.uid !== user?.uid ? 'pointer' : 'default' }}>
              <Avatar nombre={m.nombre} />
              <span className="grow">
                <div className="t">{m.nombre}{m.uid === user?.uid ? ' (tú)' : ''}</div>
                <div className="s ellipsis">{m.email}</div>
              </span>
              <span className={'badge ' + (m.rol === 'admin' ? 'accent' : '')}>{m.rol === 'admin' ? 'Administrador' : 'Miembro'}</span>
            </button>
          ))}
        </div>
      </div>
      {f.esAdmin ? (
        <button className="btn primary block" onClick={() => setInvitar(true)}>{Icon.share} Invitar a mi pareja o familiar</button>
      ) : (
        <p className="muted small">Solo un administrador puede invitar nuevos miembros.</p>
      )}
      <p className="muted tiny">Todos los miembros pueden registrar gastos, boletas y cuotas. Los administradores además invitan, cambian roles y quitan miembros.</p>

      <div className="card stack">
        <div className="row"><span style={{ width: 22, color: 'var(--accent)' }}>{Icon.shield}</span><h3>Clave de la familia</h3></div>
        <p className="small muted">Con ella se cifran los datos. Se necesita para abrir la familia en otro teléfono.</p>
        {verClave ? <div className="clave-box" style={{ fontSize: 18 }}>{fmtClave(f.clave)}</div> : <button className="btn" onClick={() => setVerClave(true)}>Mostrar clave</button>}
        {verClave && (
          <button className="btn sm" onClick={async () => avisar((await copiarTexto(fmtClave(f.clave))) ? 'Clave copiada' : 'No se pudo copiar', 'info')}>{Icon.copy} Copiar</button>
        )}
      </div>

      <div className="card flush list">
        <button className="item" onClick={() => agregarFamilia()}>
          <span className="icono">➕</span><span className="grow"><div className="t">Crear o unirme a otra familia</div><div className="s">Cada una con sus datos separados</div></span>
        </button>
        <button className="item" onClick={() => {
          if (confirm('¿Bloquear esta familia en este teléfono? Para volver a verla tendrás que ingresar la clave.')) f.bloquear();
        }}>
          <span className="icono">🔒</span><span className="grow"><div className="t">Bloquear en este teléfono</div><div className="s">Olvida la clave guardada aquí</div></span>
        </button>
        <button className="item" onClick={async () => {
          if (f.esAdmin && admins === 1 && f.members.length > 1) return avisar('Antes de salir, nombra a otro administrador.', 'error');
          if (!confirm(`¿Salir de "${f.family.nombre}"? Dejarás de ver sus datos.`)) return;
          try {
            if (user) await backend.leaveFamily(user, f.family.id);
            elegirFamilia(null);
          } catch (e) {
            error(e);
          }
        }}>
          <span className="icono">🚪</span><span className="grow"><div className="t neg">Salir de esta familia</div></span>
        </button>
      </div>

      {invitar && <InvitarSheet onClose={() => setInvitar(false)} />}
      {miembro && <MiembroSheet m={miembro} onClose={() => setMiembro(null)} />}
      {nombre != null && (
        <Sheet titulo="Renombrar familia" onClose={() => setNombre(null)} pie={
          <button className="btn primary" disabled={!nombre.trim()} onClick={async () => {
            try {
              await f.acciones.renombrarFamilia(nombre.trim());
              setNombre(null);
            } catch (e) {
              error(e);
            }
          }}>Guardar</button>
        }>
          <Campo label="Nombre"><input className="input" value={nombre} onChange={(e) => setNombre(e.target.value)} maxLength={60} autoFocus /></Campo>
        </Sheet>
      )}
    </SubPagina>
  );
}

function InvitarSheet({ onClose }: { onClose: () => void }) {
  const f = useFamilia();
  const { backend, user, avisar } = useApp();
  const [rol, setRol] = useState<Rol>('admin');
  const [inv, setInv] = useState<Invite | null>(null);
  const [err, setErr] = useState('');
  const [ocupado, setOcupado] = useState(false);

  async function generar() {
    if (!user) return;
    setOcupado(true);
    setErr('');
    try {
      setInv(await backend.createInvite(user, { id: f.family.id, nombre: f.family.nombre }, rol));
    } catch (e) {
      setErr(mensajeError(e));
    } finally {
      setOcupado(false);
    }
  }

  const texto = inv ? textoInvitacion(f.family.nombre, inv.codigo, f.clave) : '';

  return (
    <Sheet titulo="Invitar a la familia" onClose={onClose}>
      {!inv ? (
        <>
          <p className="small">Se genera un código de un solo uso por persona, válido por {DIAS_INVITACION} días. El mensaje incluye la clave de la familia: envíalo solo por un canal privado (WhatsApp, en persona).</p>
          <Campo label="Rol del invitado">
            <Seg opciones={[['admin', 'Administrador'], ['miembro', 'Miembro']]} valor={rol} onChange={setRol} />
          </Campo>
          <p className="muted tiny">{rol === 'admin' ? 'Ideal para tu pareja: puede hacer todo, incluso invitar.' : 'Puede registrar y ver todo, pero no invitar ni quitar miembros.'}</p>
          {err && <p className="error-text">{err}</p>}
          <button className="btn primary block" onClick={generar} disabled={ocupado}>{ocupado ? 'Generando…' : 'Generar invitación'}</button>
        </>
      ) : (
        <>
          <div className="stack tight" style={{ alignItems: 'center' }}>
            <span className="muted small">Código</span>
            <div className="clave-box" style={{ fontSize: 26, width: '100%' }}>{fmtCodigo(inv.codigo)}</div>
          </div>
          <button className="btn primary block" onClick={async () => {
            const r = await compartirTexto(texto, 'Invitación Finanzas Familia');
            if (r === 'copiado') avisar('Invitación copiada. Pégala en WhatsApp.', 'info');
          }}>{Icon.share} Enviar invitación</button>
          <a className="btn block" href={`https://wa.me/?text=${encodeURIComponent(texto)}`} target="_blank" rel="noopener noreferrer">Enviar por WhatsApp</a>
          <button className="btn sm" onClick={async () => avisar((await copiarTexto(texto)) ? 'Copiado' : 'No se pudo copiar', 'info')}>{Icon.copy} Copiar mensaje</button>
          <details>
            <summary className="small muted" style={{ cursor: 'pointer' }}>Ver mensaje</summary>
            <pre className="small" style={{ whiteSpace: 'pre-wrap', background: 'var(--surface)', padding: 12, borderRadius: 10, border: '1px solid var(--border)' }}>{texto}</pre>
          </details>
        </>
      )}
    </Sheet>
  );
}

function MiembroSheet({ m, onClose }: { m: Member; onClose: () => void }) {
  const f = useFamilia();
  const { backend, error, avisar } = useApp();
  return (
    <Sheet titulo={m.nombre} onClose={onClose}>
      <p className="muted small">{m.email}</p>
      <Campo label="Rol">
        <Seg opciones={[['admin', 'Administrador'], ['miembro', 'Miembro']]} valor={m.rol} onChange={async (rol) => {
          try {
            await backend.setMemberRole(f.family.id, m.uid, rol);
            avisar('Rol actualizado');
            onClose();
          } catch (e) {
            error(e);
          }
        }} />
      </Campo>
      <button className="btn danger block" onClick={async () => {
        if (!confirm(`¿Quitar a ${m.nombre} de la familia? Dejará de tener acceso a los datos de la familia.`)) return;
        try {
          await backend.removeMember(f.family.id, m.uid);
          avisar('Miembro quitado', 'info');
          onClose();
        } catch (e) {
          error(e);
        }
      }}>Quitar de la familia</button>
    </Sheet>
  );
}
