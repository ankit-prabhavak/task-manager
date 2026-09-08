import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Standard Vite + React config. `server.host: true` lets the dev
// server be reachable from outside the container (needed later
// when this runs inside Docker).
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
  },
})
