import { SubPagina } from '../components/ui';
import { useApp } from '../data/store';

export function Privacidad({ onBack }: { onBack: () => void }) {
  const { backend } = useApp();
  return (
    <SubPagina titulo="Privacidad" onBack={onBack}>
      <div className="card stack">
        <h2>Cada familia es privada</h2>
        <p className="small">Cada familia es un centro de costos independiente. Solo sus miembros (invitados con código) pueden leer o escribir sus datos: las reglas de la base de datos bloquean a cualquier otra cuenta, incluida la de quien administra la app.</p>
      </div>
      <div className="card stack">
        <h2>Cifrado de extremo a extremo</h2>
        <p className="small">Montos, descripciones, categorías, presupuestos, boletas, deudas y fotos se cifran en tu teléfono (AES-256) con la <b>clave de la familia</b> antes de subirse. La clave nunca se envía al servidor, así que en la nube solo queda texto ilegible, incluso para quien administra el proyecto.</p>
        <p className="small">Lo único visible en el servidor es lo mínimo para que funcione: el correo y nombre de cada cuenta, el nombre de la familia, quién es miembro, y el mes y la fecha de creación de cada registro (no su contenido).</p>
      </div>
      <div className="card stack">
        <h2>Tu responsabilidad</h2>
        <ul className="small" style={{ margin: 0, paddingLeft: 18 }}>
          <li>Guarda la clave de la familia en un lugar seguro. Si se pierde en todos los teléfonos, los datos no se pueden recuperar.</li>
          <li>Envía las invitaciones solo a quien corresponde: incluyen la clave.</li>
          <li>Los archivos Excel y PDF que descargas no van cifrados.</li>
        </ul>
      </div>
      {backend.mode === 'local' && (
        <div className="alert warn small">Estás en modo demostración: los datos quedan solo en este navegador y no se comparten con nadie.</div>
      )}
    </SubPagina>
  );
}
