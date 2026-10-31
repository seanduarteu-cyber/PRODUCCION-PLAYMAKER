import { defineConfig } from 'vitest/config';

// Pruebas del esquema de Supabase: necesitan Supabase local (npm run test:supabase).
export default defineConfig({
  test: {
    include: ['tests/supabase.integracion.ts'],
    environment: 'node',
    testTimeout: 30000,
    hookTimeout: 30000,
    fileParallelism: false,
  },
});
