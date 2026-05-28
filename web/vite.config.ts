import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// GitHub Pages project site: https://christiewmy1.github.io/choose-your-own-adventure/
const base = process.env.BASE_PATH ?? '/';
const apiTarget = process.env.VITE_API_PROXY_TARGET ?? 'http://127.0.0.1:8000';

export default defineConfig({
  base,
  plugins: [react()],
  server: {
    port: 4173,
    proxy: {
      '/api': {
        target: apiTarget,
        changeOrigin: true,
      },
      '/health': {
        target: apiTarget,
        changeOrigin: true,
      },
    },
  },
});
