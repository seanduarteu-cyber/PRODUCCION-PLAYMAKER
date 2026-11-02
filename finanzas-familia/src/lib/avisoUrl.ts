// Cuando un enlace de correo de Supabase falla (ya usado, vencido...), Supabase
// vuelve a la app con ?error_code=... Se guarda un aviso claro para mostrarlo en
// la pantalla de ingreso y se limpia la dirección.
const KEY = 'ff_aviso_url';

export function capturarErrorDeUrl() {
  const url = new URL(location.href);
  const hash = new URLSearchParams(url.hash.slice(1));
  const codigo = url.searchParams.get('error_code') || hash.get('error_code') || url.searchParams.get('error') || hash.get('error');
  if (!codigo) return;
  try {
    sessionStorage.setItem(KEY, codigo);
  } catch {
    /* nada */
  }
  for (const k of ['error', 'error_code', 'error_description', 'sb']) url.searchParams.delete(k);
  history.replaceState(null, '', url.pathname + url.search);
}

export function avisoDeUrl(): string | null {
  let codigo: string | null = null;
  try {
    codigo = sessionStorage.getItem(KEY);
    sessionStorage.removeItem(KEY);
  } catch {
    /* nada */
  }
  if (!codigo) return null;
  if (codigo === 'otp_expired') {
    return 'El enlace del correo ya se había usado o venció (algunos correos de empresa lo abren solos). Entra con tu correo y contraseña: si tu cuenta aún no está confirmada, la app te pedirá el código del correo.';
  }
  return 'No se pudo completar el enlace del correo. Intenta entrar con tu correo y contraseña, o pide un correo nuevo.';
}
