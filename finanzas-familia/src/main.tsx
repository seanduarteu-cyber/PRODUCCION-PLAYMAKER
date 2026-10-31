import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { capturarInvitacionDeUrl } from './lib/enlace';
import './styles.css';

capturarInvitacionDeUrl();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

if (import.meta.env.PROD && 'serviceWorker' in navigator && !import.meta.env.VITE_SIN_PWA) {
  import('virtual:pwa-register').then(({ registerSW }) => registerSW({ immediate: true })).catch(() => undefined);
}
