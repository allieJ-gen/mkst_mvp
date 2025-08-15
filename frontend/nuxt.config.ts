// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  
  // Apple HIG 기반 디자인 시스템
  modules: [
    '@nuxt/ui',
    '@pinia/nuxt'
  ],
  
  // CSS 설정 - 임시로 주석 처리
  // css: [
  //   './assets/css/apple-hig.css'
  // ],
  
  // 개발 서버 설정
  devServer: {
    port: 3000
  },
  
  // API 프록시 설정 (Django 백엔드 연결)
  nitro: {
    devProxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
