import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  base: '/', // 部署在根路径，如有子路径请改为 '/子路径/'
  plugins: [vue()],
})
