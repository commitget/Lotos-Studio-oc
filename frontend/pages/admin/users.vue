<template>
  <div class="min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="md:pl-64">
      <AdminHeader title="User Management" />
      <div class="p-6">
        <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-gray-100 bg-gray-50">
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Joined</th>
                  <th class="text-right px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="user in store.users" :key="user.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4">
                    <div class="flex items-center space-x-3">
                      <div class="w-8 h-8 rounded-full bg-teal-100 flex items-center justify-center">
                        <span class="text-teal-700 font-medium text-xs">{{ user.username?.[0]?.toUpperCase() }}</span>
                      </div>
                      <span class="text-sm font-medium text-gray-900">{{ user.username }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ user.email }}</td>
                  <td class="px-6 py-4">
                    <select v-model="user.role" @change="updateRole(user)" class="text-xs border border-gray-200 rounded-lg px-2 py-1 capitalize">
                      <option value="user">User</option>
                      <option value="tester">Tester</option>
                      <option value="customer">Customer</option>
                      <option value="manager">Manager</option>
                      <option value="moderator">Moderator</option>
                      <option value="admin">Admin</option>
                      <option value="super_admin">Super Admin</option>
                    </select>
                  </td>
                  <td class="px-6 py-4">
                    <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full" :class="user.is_active ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'">
                      {{ user.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ new Date(user.created_at).toLocaleDateString() }}</td>
                  <td class="px-6 py-4 text-right">
                    <button @click="toggleUser(user)" class="text-xs text-teal-600 hover:text-teal-700 mr-3">
                      {{ user.is_active ? 'Deactivate' : 'Activate' }}
                    </button>
                    <button @click="deleteUser(user)" v-if="auth.isSuperAdmin" class="text-xs text-red-600 hover:text-red-700">
                      Delete
                    </button>
                  </td>
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
    await store.fetchUsers()
  }
})

async function updateRole(user: any) {
  try {
    await store.updateUser(user.id, { role: user.role })
  } catch {
    alert('Failed to update role')
  }
}

async function toggleUser(user: any) {
  try {
    await store.updateUser(user.id, { is_active: !user.is_active })
    user.is_active = !user.is_active
  } catch {
    alert('Failed to toggle user')
  }
}

async function deleteUser(user: any) {
  if (confirm(`Delete user ${user.username}?`)) {
    try {
      await store.deleteUser(user.id)
    } catch {
      alert('Failed to delete user')
    }
  }
}

definePageMeta({
  title: 'User Management — Lotus Studio Admin',
  middleware: 'admin',
})
</script>
