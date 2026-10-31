// Cifrado de extremo a extremo (AES-256-GCM) de los datos de cada familia.
//
// La "clave de la familia" se genera en el teléfono de quien crea la familia y
// nunca se envía al servidor: se comparte con los miembros por la invitación
// (WhatsApp, etc.). En la base de datos solo quedan datos cifrados, por lo que
// ni el dueño del proyecto Firebase ni otras familias pueden leerlos.

const ALFABETO = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // 32 símbolos = 5 bits c/u
const ITERACIONES = 150_000;
const VERIFICADOR = 'finanzas-familia:v1';

const enc = new TextEncoder();
const dec = new TextDecoder();

function aBase64(bytes: Uint8Array): string {
  let s = '';
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(s);
}

function deBase64(s: string): Uint8Array<ArrayBuffer> {
  const bin = atob(s);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

/** Clave aleatoria de 20 símbolos (100 bits), ej: K7PD-3MXQ-9TRW-HZ2B-6NVC */
export function generarClaveFamilia(): string {
  const a = new Uint8Array(20);
  crypto.getRandomValues(a);
  return Array.from(a, (b) => ALFABETO[b % 32]).join('');
}

export function normalizarClave(c: string): string {
  return c.toUpperCase().replace(/[^A-Z0-9]/g, '');
}

export const fmtClave = (c: string) => normalizarClave(c).replace(/(.{4})(?=.)/g, '$1-');

export const claveValida = (c: string) => normalizarClave(c).length === 20;

export function generarSal(): string {
  return aBase64(crypto.getRandomValues(new Uint8Array(16)));
}

export async function derivarLlave(clave: string, sal: string): Promise<CryptoKey> {
  const base = await crypto.subtle.importKey('raw', enc.encode(normalizarClave(clave)), 'PBKDF2', false, ['deriveKey']);
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', hash: 'SHA-256', salt: deBase64(sal), iterations: ITERACIONES },
    base,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt'],
  );
}

export async function cifrar(llave: CryptoKey, valor: unknown): Promise<string> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ct = new Uint8Array(await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, llave, enc.encode(JSON.stringify(valor))));
  const out = new Uint8Array(iv.length + ct.length);
  out.set(iv);
  out.set(ct, iv.length);
  return aBase64(out);
}

export async function descifrar<T>(llave: CryptoKey, texto: string): Promise<T> {
  const bytes = deBase64(texto);
  const pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: bytes.subarray(0, 12) }, llave, bytes.subarray(12));
  return JSON.parse(dec.decode(pt)) as T;
}

export const crearVerificador = (llave: CryptoKey) => cifrar(llave, VERIFICADOR);

export async function verificarLlave(llave: CryptoKey, verificador: string): Promise<boolean> {
  try {
    return (await descifrar<string>(llave, verificador)) === VERIFICADOR;
  } catch {
    return false;
  }
}

// ---- Guardado de la clave en este dispositivo ----
const k = (fid: string) => `ff_clave_${fid}`;

export function claveGuardada(fid: string): string | null {
  try {
    return localStorage.getItem(k(fid));
  } catch {
    return null;
  }
}

export function guardarClave(fid: string, clave: string) {
  try {
    localStorage.setItem(k(fid), normalizarClave(clave));
  } catch {
    /* almacenamiento no disponible */
  }
}

export function olvidarClave(fid: string) {
  try {
    localStorage.removeItem(k(fid));
  } catch {
    /* nada */
  }
}
