export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: 'Lotus Studio — Roblox Development Studio',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Lotus Studio — профессиональная разработка Roblox плейсов на LuaU. Бета-тесты, маркетплейс, кастомная разработка.' },
        { name: 'keywords', content: 'Roblox, LuaU, game development, beta testing, Roblox places' },
        { property: 'og:title', content: 'Lotus Studio — Roblox Development Studio' },
        { property: 'og:description', content: 'Профессиональная разработка Roblox плейсов на LuaU' },
        { property: 'og:type', content: 'website' },
        { name: 'twitter:card', content: 'summary_large_image' },
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/logo.png' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Darumadrop+One&family=Roboto+Serif:ital,opsz,wght@0,8..144,100..900;1,8..144,100..900&display=swap' },
      ],
    },
  },
  tailwindcss: {
    config: {
      content: ['./pages/**/*.vue', './components/**/*.vue', './layouts/**/*.vue'],
      theme: {
        extend: {
          fontFamily: {
            display: ['Darumadrop One', 'cursive'],
            body: ['Roboto Serif', 'serif'],
          },
          colors: {
            teal: {
              50: '#f0fdfa',
              100: '#ccfbf1',
              200: '#99f6e4',
              300: '#5eead4',
              400: '#2dd4bf',
              500: '#14b8a6',
              600: '#0d9488',
              700: '#0f766e',
              800: '#115e59',
              900: '#134e4a',
            },
          },
          animation: {
            'fade-in': 'fadeIn 0.6s ease-out',
            'slide-up': 'slideUp 0.6s ease-out',
            'slide-down': 'slideDown 0.3s ease-out',
          },
          keyframes: {
            fadeIn: {
              '0%': { opacity: '0' },
              '100%': { opacity: '1' },
            },
            slideUp: {
              '0%': { opacity: '0', transform: 'translateY(30px)' },
              '100%': { opacity: '1', transform: 'translateY(0)' },
            },
            slideDown: {
              '0%': { opacity: '0', transform: 'translateY(-10px)' },
              '100%': { opacity: '1', transform: 'translateY(0)' },
            },
          },
        },
      },
    },
  },
  nitro: {
    devProxy: {
      '/api': {
        target: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api',
        changeOrigin: true,
        prependPath: true,
      },
    },
  },
  routeRules: {
    '/': { prerender: true },
    '/admin/**': { ssr: false },
  },
})
