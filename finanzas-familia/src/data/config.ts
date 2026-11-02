const env = import.meta.env;

/**
 * Configuración en tiempo de ejecución: `config.js` (junto a index.html) puede
 * definir window.FINANZAS_CONFIG. Así la misma app compilada sirve para
 * cualquier proyecto de Supabase sin volver a compilar. Si no está, se usan las
 * variables VITE_* de la compilación (Netlify / .env.local).
 */
interface ConfigEjecucion {
  SUPABASE_URL?: string;
  SUPABASE_ANON_KEY?: string;
  SUPABASE_GOOGLE?: boolean | string;
}

const rt: ConfigEjecucion =
  (typeof window !== 'undefined' && (window as unknown as { FINANZAS_CONFIG?: ConfigEjecucion }).FINANZAS_CONFIG) || {};

const limpio = (s?: string) => (s || '').trim() || undefined;

export const supabaseUrl = limpio(rt.SUPABASE_URL) || env.VITE_SUPABASE_URL;
export const supabaseKey = limpio(rt.SUPABASE_ANON_KEY) || env.VITE_SUPABASE_ANON_KEY || env.VITE_SUPABASE_PUBLISHABLE_KEY;
export const supabaseGoogle = rt.SUPABASE_GOOGLE === true || rt.SUPABASE_GOOGLE === '1' || env.VITE_SUPABASE_GOOGLE === '1';

/** true si hay URL y llave pública de Supabase (config.js o variables VITE_SUPABASE_*). */
export const supabaseConfigurado = Boolean(supabaseUrl && supabaseKey);

/** true si se configuraron las variables VITE_FIREBASE_* (alternativa a Supabase). */
export const firebaseConfigurado = Boolean(env.VITE_FIREBASE_API_KEY && env.VITE_FIREBASE_PROJECT_ID);

/** Compilación de vista previa (página de demostración con datos de ejemplo). */
export const VISTA_PREVIA = Boolean(env.VITE_VISTA_PREVIA);
