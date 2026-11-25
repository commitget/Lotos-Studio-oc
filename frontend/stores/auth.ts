import { defineStore } from 'pinia'
import { API_BASE } from '~/utils/api'

interface User {
  id: string
  email: string
  username: string
  role: string
  is_active: boolean
  is_verified: boolean
  totp_enabled: boolean
  created_at: string
}

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    accessToken: null,
    refreshToken: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isAdmin: (state) => state.user?.role === 'admin' || state.user?.role === 'super_admin',
    isSuperAdmin: (state) => state.user?.role === 'super_admin',
  },
  actions: {
    init() {
      if (process.client) {
        const token = localStorage.getItem('access_token')
        const refresh = localStorage.getItem('refresh_token')
        const user = localStorage.getItem('user')
        if (token) this.accessToken = token
        if (refresh) this.refreshToken = refresh
        if (user) this.user = JSON.parse(user)
      }
    },
    async login(email: string, password: string) {
      const res = await $fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        body: { email, password },
      })
      this.accessToken = res.access_token
      this.refreshToken = res.refresh_token
      if (process.client) {
        localStorage.setItem('access_token', res.access_token)
        localStorage.setItem('refresh_token', res.refresh_token)
      }
      await this.fetchUser()
    },
    async register(email: string, username: string, password: string) {
      const res = await $fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        body: { email, username, password },
      })
      this.accessToken = res.access_token
      this.refreshToken = res.refresh_token
      if (process.client) {
        localStorage.setItem('access_token', res.access_token)
        localStorage.setItem('refresh_token', res.refresh_token)
      }
      await this.fetchUser()
    },
    async fetchUser() {
      try {
        const user = await $fetch(`${API_BASE}/auth/me`, {
          headers: { Authorization: `Bearer ${this.accessToken}` },
        })
        this.user = user
        if (process.client) {
          localStorage.setItem('user', JSON.stringify(user))
        }
      } catch {
        this.logout()
      }
    },
    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      if (process.client) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        navigateTo('/')
      }
    },
  },
})
