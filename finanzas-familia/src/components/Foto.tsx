// Fotos de boletas y comprobantes: tomar con la cámara o elegir de la galería,
// ver en grande y guardar una copia. Se guardan 60 días y luego se borran solas.
import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import type { FotoLeida } from '../data/acciones';
import { useApp, useFamilia } from '../data/store';
import { fmtFecha, hoy } from '../lib/format';
import { comprimirFoto, DIAS_FOTO, fechaBorradoFoto, guardarCopiaFoto } from '../lib/imagen';
import { Icon, useBotonAtras } from './ui';

type Estado = FotoLeida | 'cargando' | 'error';

/** Lee una foto guardada (con reintento si falla la conexión). */
function useFotoGuardada(adjuntoId?: string) {
  const f = useFamilia();
  const [estado, setEstado] = useState<Estado | null>(adjuntoId ? 'cargando' : null);
  const [intento, setIntento] = useState(0);
  useEffect(() => {
    if (!adjuntoId) {
      setEstado(null);
      return;
    }
    let vivo = true;
    setEstado('cargando');
    f.acciones.leerAdjunto(adjuntoId)
      .then((r) => vivo && setEstado(r))
      .catch(() => vivo && setEstado('error'));
    return () => {
      vivo = false;
    };
  }, [adjuntoId, f.acciones, intento]);
  return { estado, reintentar: () => setIntento((n) => n + 1) };
}

const fechaBorrado = (creadoEn: number) => fmtFecha(hoy(fechaBorradoFoto(creadoEn)));

function useGuardarCopia() {
  const { error } = useApp();
  return (dataUrl: string, nombre: string) =>
    guardarCopiaFoto(dataUrl, nombre).catch(() => error(new Error('No se pudo guardar la copia. Mantén el dedo sobre la foto y elige “Guardar imagen”.')));
}

/** Aviso que se muestra al subir una foto. */
export function AvisoFoto60() {
  return (
    <div className="alert warn" role="note">
      <span aria-hidden>⏳</span>
      <span>
        <b>Esta foto se guarda {DIAS_FOTO} días.</b> Después se borra automáticamente para ahorrar espacio en la nube.
        Si la necesitas por más tiempo, toca “Guardar copia” y déjala en tu teléfono.
      </span>
    </div>
  );
}

/**
 * Campo para agregar, cambiar o quitar la foto de un formulario.
 * `onCambio` recibe la foto nueva (dataURL) o null si se quitó.
 */
export function FotoCampo({ adjuntoId, etiqueta, nombreArchivo, onCambio }: {
  adjuntoId?: string; etiqueta: string; nombreArchivo: string; onCambio: (foto: string | null) => void;
}) {
  const { error } = useApp();
  const { estado, reintentar } = useFotoGuardada(adjuntoId);
  const [nueva, setNueva] = useState<string | null | undefined>(undefined);
  const [procesando, setProcesando] = useState(false);
  const [ver, setVer] = useState(false);
  const guardarCopia = useGuardarCopia();
  const cambio = useRef(onCambio);
  cambio.current = onCambio;

  // Si la foto anterior ya se borró, al guardar se quita también el enlace.
  useEffect(() => {
    if (estado === 'borrada' && nueva === undefined) cambio.current(null);
  }, [estado, nueva]);

  const guardada = estado && typeof estado === 'object' ? estado : null;
  const foto = nueva !== undefined ? nueva : guardada?.dataUrl ?? null;

  async function elegir(input: HTMLInputElement) {
    const file = input.files?.[0];
    input.value = ''; // permite volver a elegir la misma foto
    if (!file) return;
    setProcesando(true);
    try {
      const d = await comprimirFoto(file);
      setNueva(d);
      cambio.current(d);
    } catch {
      error(new Error('No se pudo leer la foto. Prueba con otra imagen.'));
    } finally {
      setProcesando(false);
    }
  }

  const quitar = () => {
    setNueva(null);
    cambio.current(null);
  };

  return (
    <div className="field foto-campo">
      <span className="label">{etiqueta}</span>
      {procesando || (nueva === undefined && estado === 'cargando') ? (
        <div className="foto-cargando">{procesando ? 'Preparando foto…' : 'Cargando foto…'}</div>
      ) : foto ? (
        <>
          <img className="thumb" src={foto} alt={etiqueta} onClick={() => setVer(true)} />
          {nueva ? <AvisoFoto60 /> : guardada && (
            <p className="help">⏳ Se borrará automáticamente el {fechaBorrado(guardada.creadoEn)}.</p>
          )}
          <div className="btn-row">
            <button type="button" className="btn sm" onClick={() => guardarCopia(foto, nombreArchivo)}>{Icon.download} Guardar copia</button>
            <button type="button" className="btn sm danger" onClick={quitar}>{Icon.trash} Quitar</button>
          </div>
        </>
      ) : (
        <>
          {nueva === undefined && estado === 'borrada' && (
            <div className="alert"><span aria-hidden>🗑️</span><span>La foto anterior se borró automáticamente porque pasaron {DIAS_FOTO} días.</span></div>
          )}
          {nueva === undefined && estado === 'error' && (
            <div className="alert danger">
              <span>No se pudo cargar la foto. Revisa tu conexión. <button type="button" className="link" onClick={reintentar}>Reintentar</button></span>
            </div>
          )}
          <div className="foto-btns">
            <label className="foto-btn">
              {Icon.camera} Tomar foto
              <input type="file" accept="image/*" capture="environment" onChange={(e) => elegir(e.currentTarget)} />
            </label>
            <label className="foto-btn">
              {Icon.image} Desde galería
              <input type="file" accept="image/*" onChange={(e) => elegir(e.currentTarget)} data-galeria="" />
            </label>
          </div>
          <p className="help">⏳ Las fotos se guardan {DIAS_FOTO} días y luego se borran solas para ahorrar espacio.</p>
        </>
      )}
      {ver && foto && <VisorFoto src={foto} titulo={etiqueta} onClose={() => setVer(false)} />}
    </div>
  );
}

/** Muestra una foto ya guardada (boleta o comprobante de pago). */
export function FotoGuardada({ adjuntoId, titulo, nombreArchivo, chica }: {
  adjuntoId: string; titulo?: string; nombreArchivo: string; chica?: boolean;
}) {
  const { estado, reintentar } = useFotoGuardada(adjuntoId);
  const [ver, setVer] = useState(false);
  const guardarCopia = useGuardarCopia();

  if (estado === 'cargando' || estado == null) return <div className={'foto-cargando' + (chica ? ' sm' : '')}>Cargando foto…</div>;
  if (estado === 'borrada') return <p className="muted tiny">🗑️ {titulo ? `${titulo}: ` : 'La foto '}se borró automáticamente (pasaron {DIAS_FOTO} días).</p>;
  if (estado === 'error') {
    return <p className="muted tiny">No se pudo cargar la foto. <button type="button" className="link small" onClick={reintentar}>Reintentar</button></p>;
  }
  return (
    <div className="stack tight">
      {titulo && <span className="label muted small" style={{ fontWeight: 600 }}>{titulo}</span>}
      <img className={'thumb' + (chica ? ' sm' : '')} src={estado.dataUrl} alt={titulo || 'Foto'} onClick={() => setVer(true)} />
      <div className="row between" style={{ gap: 8 }}>
        <span className="muted tiny">⏳ Se borra el {fechaBorrado(estado.creadoEn)}</span>
        <button type="button" className="link small row" style={{ gap: 4 }} onClick={() => guardarCopia(estado.dataUrl, nombreArchivo)}>
          <span style={{ width: 16, height: 16, display: 'inline-block' }}>{Icon.download}</span> Guardar copia
        </button>
      </div>
      {ver && <VisorFoto src={estado.dataUrl} titulo={titulo || 'Foto'} onClose={() => setVer(false)} />}
    </div>
  );
}

/** Foto en pantalla completa. */
export function VisorFoto({ src, titulo, onClose }: { src: string; titulo: string; onClose: () => void }) {
  useBotonAtras(true, onClose);
  return createPortal(
    <div className="visor" role="dialog" aria-modal="true" aria-label={titulo} onClick={onClose}>
      <img src={src} alt={titulo} />
      <button type="button" className="iconbtn cerrar" aria-label="Cerrar" onClick={onClose}>{Icon.close}</button>
    </div>,
    document.body,
  );
}
