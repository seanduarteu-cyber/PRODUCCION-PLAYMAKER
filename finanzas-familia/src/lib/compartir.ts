/** Descarga un archivo (o lo comparte en el teléfono: WhatsApp, Archivos, Mail...). */
export async function entregarArchivo(blob: Blob, nombre: string, modo: 'descargar' | 'compartir') {
  if (modo === 'compartir') {
    const file = new File([blob], nombre, { type: blob.type });
    if (navigator.canShare?.({ files: [file] })) {
      try {
        await navigator.share({ files: [file], title: nombre });
        return;
      } catch (e) {
        if ((e as Error).name === 'AbortError') return;
      }
    }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = nombre;
  a.rel = 'noopener';
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60_000);
}

export const puedeCompartirArchivos = () => {
  try {
    return !!navigator.canShare?.({ files: [new File(['x'], 'x.pdf', { type: 'application/pdf' })] });
  } catch {
    return false;
  }
};

export async function copiarTexto(t: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(t);
    return true;
  } catch {
    return false;
  }
}

export async function compartirTexto(texto: string, titulo: string): Promise<'compartido' | 'copiado' | 'nada'> {
  if (navigator.share) {
    try {
      await navigator.share({ text: texto, title: titulo });
      return 'compartido';
    } catch (e) {
      if ((e as Error).name === 'AbortError') return 'nada';
    }
  }
  return (await copiarTexto(texto)) ? 'copiado' : 'nada';
}
