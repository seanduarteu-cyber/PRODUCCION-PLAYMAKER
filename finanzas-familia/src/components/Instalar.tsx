import { useEffect, useState } from 'react';
import {
  alCambiarInstalacion, avisoCerrado, cerrarAviso, esAndroid, esAppInstalada, esIPhone, instalar, puedeInstalarConBoton,
} from '../lib/instalar';
import { Icon, Sheet } from './ui';

function useInstalacion() {
  const [, forzar] = useState(0);
  useEffect(() => alCambiarInstalacion(() => forzar((n) => n + 1)), []);
  return {
    instalada: esAppInstalada(),
    conBoton: puedeInstalarConBoton(),
    iphone: esIPhone(),
    android: esAndroid(),
  };
}

/** Pasos para instalar, según el teléfono. */
export function PasosInstalar({ iphone }: { iphone: boolean }) {
  if (iphone) {
    return (
      <ol className="small stack tight" style={{ margin: 0, paddingLeft: 20 }}>
        <li>Abre esta página en <b>Safari</b>.</li>
        <li>Toca el botón <b>Compartir</b> <span aria-hidden>(el cuadrado con una flecha hacia arriba ⬆️)</span>.</li>
        <li>Baja y toca <b>"Agregar a inicio"</b>, luego <b>"Agregar"</b>.</li>
      </ol>
    );
  }
  return (
    <ol className="small stack tight" style={{ margin: 0, paddingLeft: 20 }}>
      <li>Abre esta página en <b>Chrome</b>.</li>
      <li>Toca el menú <b>⋮</b> (arriba a la derecha).</li>
      <li>Toca <b>"Instalar app"</b> o <b>"Agregar a la pantalla principal"</b>.</li>
    </ol>
  );
}

/** Aviso para instalar la app (no aparece si ya está instalada o si se cerró). */
export function AvisoInstalar() {
  const { instalada, conBoton, iphone, android } = useInstalacion();
  const [cerrado, setCerrado] = useState(avisoCerrado);
  if (instalada || cerrado || avisoCerrado() || (!conBoton && !iphone && !android)) return null;
  const cerrar = () => {
    cerrarAviso();
    setCerrado(true);
  };
  return (
    <div className="card stack tight" style={{ borderColor: 'var(--accent)' }}>
      <div className="row between top">
        <div className="row" style={{ gap: 8 }}>
          <span style={{ width: 22, color: 'var(--accent)' }}>{Icon.download}</span>
          <h3>Instala la app en tu teléfono</h3>
        </div>
        <button className="iconbtn" style={{ width: 32, height: 32 }} onClick={cerrar} aria-label="Cerrar aviso">{Icon.close}</button>
      </div>
      <p className="small muted">Queda con su ícono en la pantalla de inicio y se abre como cualquier app.</p>
      {conBoton ? (
        <button className="btn primary block" onClick={() => instalar()}>Instalar app</button>
      ) : (
        <PasosInstalar iphone={iphone} />
      )}
    </div>
  );
}

/** Ítem de "Más" con las instrucciones (siempre disponible). */
export function InstalarSheet({ onClose }: { onClose: () => void }) {
  const { instalada, conBoton, iphone } = useInstalacion();
  return (
    <Sheet titulo="Instalar en el teléfono" onClose={onClose}>
      {instalada ? (
        <div className="alert ok">Ya estás usando la app instalada en este teléfono.</div>
      ) : conBoton ? (
        <>
          <p className="small">Toca el botón y confirma. La app queda con su ícono en la pantalla de inicio.</p>
          <button className="btn primary block" onClick={() => instalar().then((ok) => ok && onClose())}>Instalar app</button>
        </>
      ) : (
        <>
          <h3>{iphone ? 'En iPhone' : 'En Android'}</h3>
          <PasosInstalar iphone={iphone} />
          <h3 style={{ marginTop: 8 }}>{iphone ? 'En Android' : 'En iPhone'}</h3>
          <PasosInstalar iphone={!iphone} />
        </>
      )}
      <p className="muted tiny">Para tu familia: envíales la dirección de la app y que sigan estos mismos pasos.</p>
    </Sheet>
  );
}
