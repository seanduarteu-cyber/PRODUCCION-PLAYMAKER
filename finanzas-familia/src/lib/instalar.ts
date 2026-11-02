// Instalar la app en el teléfono (PWA).
// - Android / Chrome: el navegador avisa con "beforeinstallprompt" y la app puede
//   mostrar su propio botón "Instalar".
// - iPhone / iPad: Apple no permite ese botón; hay que usar Compartir › Agregar a inicio.

interface EventoInstalar extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

let evento: EventoInstalar | null = null;
const subs = new Set<() => void>();
const avisar = () => subs.forEach((f) => f());

export function capturarInstalacion() {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    evento = e as EventoInstalar;
    avisar();
  });
  window.addEventListener('appinstalled', () => {
    evento = null;
    cerrarAviso();
    avisar();
  });
}

export const puedeInstalarConBoton = () => evento != null;

export async function instalar(): Promise<boolean> {
  if (!evento) return false;
  const e = evento;
  await e.prompt();
  const r = await e.userChoice.catch(() => ({ outcome: 'dismissed' as const }));
  evento = null;
  if (r.outcome === 'accepted') cerrarAviso();
  avisar();
  return r.outcome === 'accepted';
}

export function alCambiarInstalacion(f: () => void): () => void {
  subs.add(f);
  return () => {
    subs.delete(f);
  };
}

/** ¿Ya se está usando como app instalada? */
export function esAppInstalada(): boolean {
  return matchMedia('(display-mode: standalone)').matches || (navigator as Navigator & { standalone?: boolean }).standalone === true;
}

export function esIPhone(): boolean {
  return /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
}

export function esAndroid(): boolean {
  return /android/i.test(navigator.userAgent);
}

// Si la persona cierra el aviso, no se vuelve a mostrar en 30 días.
const LS = 'ff_aviso_instalar';
export function avisoCerrado(): boolean {
  try {
    const t = Number(localStorage.getItem(LS) || 0);
    return Date.now() - t < 30 * 86400000;
  } catch {
    return false;
  }
}
export function cerrarAviso() {
  try {
    localStorage.setItem(LS, String(Date.now()));
  } catch {
    /* nada */
  }
}
