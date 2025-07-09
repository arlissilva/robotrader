import react from '@vitejs/plugin-react'

export default {
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/ordens': 'http://localhost:8000',
      '/ativos': 'http://localhost:8000',
	  '/login': 'http://localhost:8000',
      '/dados': 'http://localhost:8000'
    }
  }
}