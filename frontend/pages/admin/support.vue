<template>
  <div class="min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="md:pl-64">
      <AdminHeader title="Support Tickets" />
      <div class="p-6">
        <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-gray-100 bg-gray-50/50">
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Message</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th class="text-right px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="ticket in tickets" :key="ticket.id" class="hover:bg-gray-50/50 transition-colors">
                  <td class="px-6 py-4">
                    <span :class="statusClass(ticket.status)" class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium">{{ ticket.status }}</span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-600">{{ ticket.user_id?.slice(0, 8) }}...</td>
                  <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ ticket.subject }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">{{ ticket.message }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ new Date(ticket.created_at).toLocaleDateString() }}</td>
                  <td class="px-6 py-4 text-right">
                    <select v-model="ticket.status" @change="updateStatus(ticket)"
                      class="text-sm border border-gray-200 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none">
                      <option value="open">Open</option>
                      <option value="in_progress">In Progress</option>
                      <option value="resolved">Resolved</option>
                      <option value="closed">Closed</option>
                    </select>
                  </td>
                </tr>
                <tr v-if="!tickets.length">
                  <td colspan="6" class="px-6 py-12 text-center text-gray-400">No support tickets yet</td>
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
import { API_BASE, apiFetch } from '~/utils/api'

const tickets = ref<any[]>([])

onMounted(async () => {
  try {
    tickets.value = await apiFetch<any[]>(`${API_BASE}/admin/support`)
  } catch {}
})

async function updateStatus(ticket: any) {
  await apiFetch(`${API_BASE}/admin/support/${ticket.id}`, {
    method: 'PUT',
    body: { status: ticket.status },
  })
}

function statusClass(status: string) {
  return {
    'bg-green-100 text-green-700': status === 'resolved' || status === 'closed',
    'bg-yellow-100 text-yellow-700': status === 'open',
    'bg-blue-100 text-blue-700': status === 'in_progress',
  }
}

definePageMeta({
  title: 'Support Tickets — Lotus Studio Admin',
  middleware: 'admin',
})
</script>
