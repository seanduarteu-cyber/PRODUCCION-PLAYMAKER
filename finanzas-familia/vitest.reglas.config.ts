import { defineConfig } from 'vitest/config';

// Pruebas de reglas de Firestore: necesitan el emulador (npm run test:reglas).
export default defineConfig({
  test: {
    include: ['tests/reglas.emulador.ts'],
    environment: 'node',
    testTimeout: 20000,
    fileParallelism: false,
  },
});
