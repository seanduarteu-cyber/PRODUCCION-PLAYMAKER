// =====================================================================
// Finanzas Familia · datos de conexión con Supabase
//
// Pega aquí los datos de tu proyecto (Supabase › Project Settings › API,
// o el botón "Connect"):
//   SUPABASE_URL       → Project URL, ej: https://abcd1234.supabase.co
//   SUPABASE_ANON_KEY  → la llave pública "anon" o "publishable"
//
// Esta llave es pública por diseño: los datos los protegen las reglas del
// esquema SQL y el cifrado de la app. NUNCA pongas aquí la llave
// "service_role" / "secret".
//
// Si lo dejas vacío, la app abre en "modo demostración" (datos solo en el
// teléfono).
// =====================================================================
window.FINANZAS_CONFIG = {
  SUPABASE_URL: '',
  SUPABASE_ANON_KEY: '',
  // true si activaste "Google" en Supabase › Authentication › Providers
  SUPABASE_GOOGLE: false,
};
