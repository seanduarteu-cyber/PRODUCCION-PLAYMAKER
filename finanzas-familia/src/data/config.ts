const env = import.meta.env;

/** true si se configuraron VITE_SUPABASE_URL y la llave pública (ver .env.example). */
export const supabaseConfigurado = Boolean(env.VITE_SUPABASE_URL && (env.VITE_SUPABASE_ANON_KEY || env.VITE_SUPABASE_PUBLISHABLE_KEY));

/** true si se configuraron las variables VITE_FIREBASE_* (alternativa a Supabase). */
export const firebaseConfigurado = Boolean(env.VITE_FIREBASE_API_KEY && env.VITE_FIREBASE_PROJECT_ID);

/** Compilación de vista previa (página de demostración con datos de ejemplo). */
export const VISTA_PREVIA = Boolean(env.VITE_VISTA_PREVIA);
