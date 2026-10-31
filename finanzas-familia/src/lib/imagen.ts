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
