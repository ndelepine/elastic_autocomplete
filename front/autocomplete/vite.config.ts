import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
    
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:9200',  // URL du serveur Elastic
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')  // Supprime le préfixe /api pour Elasticsearch
      }
    }
  }
})
