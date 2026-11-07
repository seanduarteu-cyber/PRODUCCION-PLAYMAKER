/**
 * Reduce la foto de una boleta para guardarla cifrada en la base de datos
 * (máx. ~1400 px y ~350 KB en JPEG).
 */
export async function comprimirFoto(file: File, maxLado = 1400, maxBytes = 350_000): Promise<string> {
  const bitmap = await createImageBitmap(file).catch(async () => {
    const url = URL.createObjectURL(file);
    try {
      const img = new Image();
      img.src = url;
      await img.decode();
      return img;
    } finally {
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }
  });
  let w = bitmap.width;
  let h = bitmap.height;
  const escala = Math.min(1, maxLado / Math.max(w, h));
  w = Math.round(w * escala);
  h = Math.round(h * escala);
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  canvas.getContext('2d')!.drawImage(bitmap, 0, 0, w, h);
  let q = 0.72;
  let url = canvas.toDataURL('image/jpeg', q);
  while (url.length * 0.75 > maxBytes && q > 0.3) {
    q -= 0.12;
    url = canvas.toDataURL('image/jpeg', q);
  }
  if (url.length * 0.75 > maxBytes) {
    const c2 = document.createElement('canvas');
    c2.width = Math.round(w * 0.6);
    c2.height = Math.round(h * 0.6);
    c2.getContext('2d')!.drawImage(canvas, 0, 0, c2.width, c2.height);
    url = c2.toDataURL('image/jpeg', 0.6);
  }
  return url;
}

/** Las fotos se guardan este número de días y luego se borran solas. */
export const DIAS_FOTO = 60;

export function fotoVencida(creadoEn: number, ahora = Date.now()): boolean {
  return creadoEn > 0 && ahora - creadoEn > DIAS_FOTO * 86400000;
}

export function fechaBorradoFoto(creadoEn: number): Date {
  return new Date(creadoEn + DIAS_FOTO * 86400000);
}

/** Guarda una copia de la foto en el teléfono (Compartir › Guardar imagen, o descarga). */
export async function guardarCopiaFoto(dataUrl: string, nombre: string): Promise<void> {
  const blob = await (await fetch(dataUrl)).blob();
  const archivo = new File([blob], nombre, { type: blob.type || 'image/jpeg' });
  const nav = navigator as Navigator & { canShare?: (d: ShareData) => boolean };
  const tactil = matchMedia('(pointer: coarse)').matches;
  if (tactil && nav.canShare?.({ files: [archivo] })) {
    try {
      await nav.share({ files: [archivo], title: nombre });
      return;
    } catch (e) {
      if ((e as Error).name === 'AbortError') return; // la persona canceló
    }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = nombre;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}
