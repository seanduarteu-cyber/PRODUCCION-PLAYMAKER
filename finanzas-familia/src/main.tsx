import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { capturarInvitacionDeUrl } from './lib/enlace';
import './styles.css';

capturarInvitacionDeUrl();

// La vista previa se muestra dentro de otra página, donde confirm() no aparece.
if (import.meta.env.VITE_VISTA_PREVIA) window.confirm = () => true;

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

if (import.meta.env.PROD && 'serviceWorker' in navigator && !import.meta.env.VITE_SIN_PWA && !import.meta.env.VITE_VISTA_PREVIA) {
  import('virtual:pwa-register').then(({ registerSW }) => registerSW({ immediate: true })).catch(() => undefined);
}
