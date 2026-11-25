<template>
  <div class="min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="md:pl-64">
      <AdminHeader title="Change Logs" />
      <div class="p-6">
        <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-gray-100 bg-gray-50">
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Entity</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Entity ID</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="log in store.changelogs" :key="log.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4 text-sm text-gray-500">{{ new Date(log.created_at).toLocaleString() }}</td>
                  <td class="px-6 py-4">
                    <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full capitalize" :class="actionClass(log.action)">
                      {{ log.action }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-700">{{ log.entity_type }}</td>
                  <td class="px-6 py-4 text-sm text-gray-400 font-mono">{{ log.entity_id?.slice(0, 8) || '-' }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ log.user_id?.slice(0, 8) || 'System' }}</td>
                </tr>
                <tr v-if="!store.changelogs.length">
                  <td colspan="5" class="px-6 py-12 text-center text-sm text-gray-400">No logs available</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAdminStore } from '~/stores/admin'
import { useAuthStore } from '~/stores/auth'

const auth = useAuthStore()
const store = useAdminStore()

onMounted(async () => {
  if (auth.isAdmin) {
    await store.fetchChangelogs()
  }
})

function actionClass(action: string) {
  const map: Record<string, string> = {
    register: 'bg-green-50 text-green-700',
    login: 'bg-blue-50 text-blue-700',
    delete: 'bg-red-50 text-red-700',
    update: 'bg-yellow-50 text-yellow-700',
    create: 'bg-teal-50 text-teal-700',
  }
  return map[action] || 'bg-gray-50 text-gray-700'
}

definePageMeta({
  title: 'Change Logs — Lotus Studio Admin',
  middleware: 'admin',
})
</script>
