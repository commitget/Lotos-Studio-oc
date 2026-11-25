<template>
  <div class="min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="md:pl-64">
      <AdminHeader title="Dashboard" />
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div v-for="stat in statCards" :key="stat.label" class="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-500">{{ stat.label }}</span>
              <div class="w-10 h-10 rounded-lg flex items-center justify-center" :class="stat.bg">
                <component :is="stat.icon" class="w-5 h-5" :class="stat.color" />
              </div>
            </div>
            <div class="font-display text-3xl text-gray-900">{{ stat.value }}</div>
          </div>
        </div>
        <div class="grid lg:grid-cols-2 gap-6">
          <div class="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
            <h3 class="font-display text-lg text-gray-900 mb-4">Recent Activity</h3>
            <div v-if="store.changelogs.length" class="space-y-3">
              <div v-for="log in store.changelogs.slice(0, 10)" :key="log.id" class="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <div>
                  <span class="text-sm font-medium text-gray-700 capitalize">{{ log.action }}</span>
                  <span class="text-sm text-gray-400 ml-2">{{ log.entity_type }}</span>
                </div>
                <span class="text-xs text-gray-400">{{ new Date(log.created_at).toLocaleDateString() }}</span>
              </div>
            </div>
            <p v-else class="text-sm text-gray-400">No recent activity</p>
          </div>
          <div class="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
            <h3 class="font-display text-lg text-gray-900 mb-4">Quick Actions</h3>
            <div class="space-y-3">
              <NuxtLink to="/admin/users" class="flex items-center justify-between px-4 py-3 bg-gray-50 rounded-xl hover:bg-teal-50 transition-colors">
                <span class="text-sm text-gray-700">Manage Users</span>
                <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </NuxtLink>
              <NuxtLink to="/admin/logs" class="flex items-center justify-between px-4 py-3 bg-gray-50 rounded-xl hover:bg-teal-50 transition-colors">
                <span class="text-sm text-gray-700">View Audit Log</span>
                <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </NuxtLink>
              <button @click="resetDB" class="flex items-center justify-between w-full px-4 py-3 bg-red-50 rounded-xl hover:bg-red-100 transition-colors">
                <span class="text-sm text-red-600">Reset Database</span>
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAdminStore } from '~/stores/admin'
import { useAuthStore } from '~/stores/auth'
import { UserIcon, OrderIcon, RevenueIcon, SubsIcon } from '~/components/icons'
import { API_BASE, apiFetch } from '~/utils/api'

const auth = useAuthStore()
const store = useAdminStore()

const statCards = computed(() => [
  { label: 'Total Users', value: store.stats?.total_users ?? '-', icon: UserIcon, bg: 'bg-blue-50', color: 'text-blue-600' },
  { label: 'Orders', value: store.stats?.total_orders ?? '-', icon: OrderIcon, bg: 'bg-green-50', color: 'text-green-600' },
  { label: 'Revenue', value: `$${store.stats?.total_payments ?? 0}`, icon: RevenueIcon, bg: 'bg-teal-50', color: 'text-teal-600' },
  { label: 'Active Subs', value: store.stats?.active_subscriptions ?? '-', icon: SubsIcon, bg: 'bg-purple-50', color: 'text-purple-600' },
])

onMounted(async () => {
  if (auth.isAdmin) {
    await store.fetchStats()
    await store.fetchChangelogs()
  }
})

async function resetDB() {
  if (confirm('Are you sure you want to reset the database? This action cannot be undone.')) {
    try {
      await apiFetch(`${API_BASE}/admin/db/reset`, { method: 'POST' })
      alert('Database reset completed')
      await store.fetchStats()
    } catch (e: any) {
      alert(e?.data?.detail || 'Reset failed')
    }
  }
}

definePageMeta({
  title: 'Admin Dashboard — Lotus Studio',
  middleware: 'admin',
})
</script>
