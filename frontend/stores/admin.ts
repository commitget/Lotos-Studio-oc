import { defineStore } from 'pinia'
import { API_BASE, authHeaders, apiFetch } from '~/utils/api'

interface AdminStats {
  total_users: number
  total_orders: number
  total_places: number
  total_games: number
  total_payments: number
  active_subscriptions: number
  recent_logins: number
}

interface ChangeLog {
  id: string
  user_id: string | null
  action: string
  entity_type: string
  entity_id: string | null
  changes: any
  created_at: string
}

export const useAdminStore = defineStore('admin', {
  state: () => ({
    stats: null as AdminStats | null,
    users: [] as any[],
    changelogs: [] as ChangeLog[],
    loading: false,
  }),
  actions: {
    async fetchStats() {
      this.stats = await apiFetch<AdminStats>(`${API_BASE}/admin/stats`)
    },
    async fetchUsers() {
      this.users = await apiFetch<any[]>(`${API_BASE}/admin/users`)
    },
    async fetchChangelogs() {
      this.changelogs = await apiFetch<ChangeLog[]>(`${API_BASE}/admin/changelogs`)
    },
    async updateUser(userId: string, data: any) {
      return await apiFetch<any>(`${API_BASE}/admin/users/${userId}`, {
        method: 'PUT',
        body: data,
      })
    },
    async deleteUser(userId: string) {
      await apiFetch(`${API_BASE}/admin/users/${userId}`, {
        method: 'DELETE',
      })
      this.users = this.users.filter(u => u.id !== userId)
    },
  },
})
