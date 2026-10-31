const env = import.meta.env;

/** true si se configuraron las variables VITE_FIREBASE_* (ver .env.example). */
export const firebaseConfigurado = Boolean(env.VITE_FIREBASE_API_KEY && env.VITE_FIREBASE_PROJECT_ID);

/** Compilación de vista previa (página de demostración con datos de ejemplo). */
export const VISTA_PREVIA = Boolean(env.VITE_VISTA_PREVIA);
