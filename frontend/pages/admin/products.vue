<template>
  <div class="min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="md:pl-64">
      <AdminHeader title="Product Management" />
      <div class="p-6">
        <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-gray-100 bg-gray-50">
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                  <th class="text-right px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-if="!places.length">
                  <td colspan="5" class="px-6 py-12 text-center text-sm text-gray-400">No products yet</td>
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
import { useAuthStore } from '~/stores/auth'
import { API_BASE, authHeaders, apiFetch } from '~/utils/api'

const auth = useAuthStore()
const places = ref([])

onMounted(async () => {
  try {
    places.value = await apiFetch<any[]>(`${API_BASE}/admin/places`)
  } catch {}
})

definePageMeta({
  title: 'Products — Lotus Studio Admin',
  middleware: 'admin',
})
</script>
