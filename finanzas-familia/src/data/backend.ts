import type {
  AppUser, ColeccionNombre, FamilyDoc, FamilyRef, Invite, Member, MesKey, RawDoc, Rol,
} from '../lib/types';

export type Unsub = () => void;

/** Filtro por mes (campo `mes` visible) — desde/hasta incluidos. */
export interface RangoMeses {
  desde: MesKey;
  hasta: MesKey;
}

export type WriteOp =
  | { op: 'set'; coll: ColeccionNombre; id: string; data: Omit<RawDoc, 'id'> }
  | { op: 'delete'; coll: ColeccionNombre; id: string };

export type NuevaFamilia = Omit<FamilyDoc, 'id'>;

/**
 * Todo el acceso a datos pasa por esta interfaz. Hay dos implementaciones:
 * - firebase: datos en la nube, compartidos entre los miembros de la familia.
 * - local: modo demostración, datos solo en este dispositivo.
 */
export interface Backend {
  mode: 'firebase' | 'supabase' | 'local';
  /** ¿Se muestra el botón "Continuar con Google"? */
  conGoogle: boolean;
  /** Aviso cuando el usuario vuelve desde el correo de "olvidé mi contraseña". */
  onRecuperacion?(cb: () => void): Unsub;
  cambiarContrasena?(password: string): Promise<void>;
  onAuth(cb: (u: AppUser | null) => void): Unsub;
  signIn(email: string, password: string): Promise<void>;
  signUp(nombre: string, email: string, password: string): Promise<void>;
  signInGoogle(): Promise<void>;
  resetPassword(email: string): Promise<void>;
  signOut(): Promise<void>;

  watchMyFamilies(user: AppUser, cb: (f: FamilyRef[]) => void): Unsub;
  /** `familia` ya viene con los settings cifrados. */
  createFamily(user: AppUser, familia: NuevaFamilia, id: string): Promise<void>;
  joinFamily(user: AppUser, codigo: string): Promise<FamilyRef>;
  leaveFamily(user: AppUser, familyId: string): Promise<void>;
  forgetFamily(user: AppUser, familyId: string): Promise<void>;

  watchFamily(familyId: string, cb: (f: FamilyDoc | null) => void, onError: (e: Error) => void): Unsub;
  updateFamily(familyId: string, patch: { nombre?: string; settingsEnc?: string }): Promise<void>;
  watchMembers(familyId: string, cb: (m: Member[]) => void): Unsub;
  setMemberRole(familyId: string, uid: string, rol: Rol): Promise<void>;
  removeMember(familyId: string, uid: string): Promise<void>;
  createInvite(user: AppUser, family: { id: string; nombre: string }, rol: Rol): Promise<Invite>;

  watchCollection(familyId: string, coll: ColeccionNombre, cb: (docs: RawDoc[]) => void, rango?: RangoMeses, onError?: (e: Error) => void): Unsub;
  getCollection(familyId: string, coll: ColeccionNombre, rango?: RangoMeses): Promise<RawDoc[]>;
  getDoc(familyId: string, coll: ColeccionNombre, id: string): Promise<RawDoc | null>;
  /** Escribe en lote. Se resuelve cuando el servidor confirma (offline queda en cola). */
  commit(familyId: string, ops: WriteOp[]): Promise<void>;
  newFamilyId(): string;
}

export function mensajeError(e: unknown): string {
  const code = (e as { code?: string })?.code || '';
  const map: Record<string, string> = {
    'auth/invalid-email': 'El correo no es válido.',
    'auth/missing-password': 'Escribe tu contraseña.',
    'auth/invalid-credential': 'Correo o contraseña incorrectos.',
    'auth/wrong-password': 'Correo o contraseña incorrectos.',
    'auth/user-not-found': 'No existe una cuenta con ese correo.',
    'auth/email-already-in-use': 'Ya existe una cuenta con ese correo. Inicia sesión.',
    'auth/weak-password': 'La contraseña debe tener al menos 6 caracteres.',
    'auth/popup-closed-by-user': 'Se cerró la ventana de Google antes de terminar.',
    'auth/network-request-failed': 'Sin conexión a internet.',
    'auth/too-many-requests': 'Demasiados intentos. Espera unos minutos.',
    'permission-denied': 'No tienes permiso para hacer esto en esta familia.',
    'unavailable': 'Sin conexión. Se guardará cuando vuelva internet.',
    // Supabase
    'invalid_credentials': 'Correo o contraseña incorrectos.',
    'email_not_confirmed': 'Primero confirma tu correo: abre el enlace que te enviamos (revisa también spam).',
    'user_already_exists': 'Ya existe una cuenta con ese correo. Inicia sesión.',
    'email_exists': 'Ya existe una cuenta con ese correo. Inicia sesión.',
    'weak_password': 'La contraseña debe tener al menos 6 caracteres.',
    'same_password': 'La nueva contraseña debe ser distinta a la anterior.',
    'validation_failed': 'Revisa que el correo esté bien escrito.',
    'over_email_send_rate_limit': 'Se enviaron demasiados correos. Espera unos minutos.',
    'over_request_rate_limit': 'Demasiados intentos. Espera unos minutos.',
    'signup_disabled': 'El registro de cuentas nuevas está desactivado.',
    '42501': 'No tienes permiso para hacer esto en esta familia.',
    'PGRST301': 'Tu sesión expiró. Vuelve a entrar.',
  };
  if (map[code]) return map[code];
  const msg = (e as Error)?.message || String(e);
  if (/failed to fetch|load failed|networkerror|network request failed/i.test(msg)) return 'Sin conexión a internet. Revisa tu conexión e intenta de nuevo.';
  return msg.replace(/^Firebase: /, '').replace(/\s*\(.*\)\.?$/, '');
}

const ALFABETO = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';

export function generarCodigo(): string {
  const a = new Uint8Array(8);
  crypto.getRandomValues(a);
  return Array.from(a, (b) => ALFABETO[b % ALFABETO.length]).join('');
}

export function normalizarCodigo(c: string): string {
  return c.toUpperCase().replace(/[^A-Z0-9]/g, '');
}

export const fmtCodigo = (c: string) => `${c.slice(0, 4)}-${c.slice(4)}`;

export const DIAS_INVITACION = 7;
