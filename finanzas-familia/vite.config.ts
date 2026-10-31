import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

// VITE_VISTA_PREVIA=1 genera una sola página autocontenida (demo con datos de ejemplo).
const vistaPrevia = process.env.VITE_VISTA_PREVIA === '1';

export default defineConfig({
  base: './',
  plugins: [
    react(),
    VitePWA({
      disable: vistaPrevia,
      registerType: 'autoUpdate',
      injectRegister: false,
      includeAssets: ['icon.svg', 'apple-touch-icon.png'],
      manifest: {
        name: 'Finanzas Familia',
        short_name: 'Finanzas',
        description: 'Gastos, boletas y cuotas de tu familia, en privado.',
        lang: 'es-CL',
        start_url: './',
        scope: './',
        display: 'standalone',
        orientation: 'portrait',
        background_color: '#f3f5f4',
        theme_color: '#0e7458',
        icons: [
          { src: 'icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icon-512.png', sizes: '512x512', type: 'image/png' },
          { src: 'icon-maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,png,webmanifest}'],
        maximumFileSizeToCacheInBytes: 6 * 1024 * 1024,
        navigateFallback: 'index.html',
      },
    }),
  ],
  build: vistaPrevia
    ? {
        target: 'es2022',
        outDir: 'dist-vista',
        assetsInlineLimit: 10_000_000,
        cssCodeSplit: false,
        chunkSizeWarningLimit: 5000,
        rollupOptions: { output: { inlineDynamicImports: true } },
      }
    : {
        target: 'es2022',
        chunkSizeWarningLimit: 1500,
      },
});
