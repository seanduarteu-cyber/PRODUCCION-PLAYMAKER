// Enlaces de invitación: https://app/?unirse=CODIGO#clave=CLAVE
// La clave va después del "#", por lo que el navegador nunca la envía al
// servidor: solo la ve quien recibe el enlace.
import { fmtCodigo } from '../data/backend';
import { fmtClave } from './crypto';

const KEY = 'ff_invitacion_pendiente';

export interface InvitacionPendiente { codigo: string; clave: string }

export function capturarInvitacionDeUrl() {
  const url = new URL(location.href);
  const codigo = url.searchParams.get('unirse');
  if (!codigo) return;
  const clave = new URLSearchParams(url.hash.slice(1)).get('clave') || '';
  try {
    localStorage.setItem(KEY, JSON.stringify({ codigo, clave, guardada: Date.now() }));
  } catch {
    /* nada */
  }
  url.searchParams.delete('unirse');
  url.hash = '';
  history.replaceState(null, '', url.pathname + url.search);
}

export function invitacionPendiente(): InvitacionPendiente | null {
  try {
    const s = localStorage.getItem(KEY);
    const inv = s ? (JSON.parse(s) as InvitacionPendiente & { guardada?: number }) : null;
    // Una invitación pendiente se recuerda por 7 días (lo que dura el código).
    if (inv && (!inv.guardada || Date.now() - inv.guardada > 7 * 86400000)) {
      localStorage.removeItem(KEY);
      return null;
    }
    return inv;
  } catch {
    return null;
  }
}

export function descartarInvitacion() {
  try {
    localStorage.removeItem(KEY);
  } catch {
    /* nada */
  }
}

export function enlaceInvitacion(codigo: string, clave: string): string {
  const base = location.origin + location.pathname;
  return `${base}?unirse=${codigo}#clave=${clave}`;
}

export function textoInvitacion(familia: string, codigo: string, clave: string): string {
  return [
    `Te invito a la familia "${familia}" en Finanzas Familia.`,
    '',
    `1) Abre este enlace: ${enlaceInvitacion(codigo, clave)}`,
    '2) Crea tu cuenta o inicia sesión.',
    '',
    `Si te lo pide, ingresa a mano:`,
    `Código: ${fmtCodigo(codigo)}`,
    `Clave de la familia: ${fmtClave(clave)}`,
    '',
    'No compartas este mensaje con nadie más: la clave permite ver nuestras finanzas.',
  ].join('\n');
}
