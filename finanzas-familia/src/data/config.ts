const env = import.meta.env;

/** true si se configuraron las variables VITE_FIREBASE_* (ver .env.example). */
export const firebaseConfigurado = Boolean(env.VITE_FIREBASE_API_KEY && env.VITE_FIREBASE_PROJECT_ID);
