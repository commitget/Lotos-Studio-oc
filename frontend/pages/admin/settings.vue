<template>
  <div class="min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="md:pl-64">
      <AdminHeader title="Settings" />
      <div class="p-6 max-w-2xl">
        <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-8">
          <h3 class="font-display text-lg text-gray-900 mb-6">Platform Configuration</h3>
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">App Name</label>
              <input type="text" :value="config.APP_NAME" class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-sm" disabled />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Version</label>
              <input type="text" :value="config.APP_VERSION" class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-sm" disabled />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Environment</label>
              <input type="text" :value="config.ENVIRONMENT" class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-sm" disabled />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Admin Email</label>
              <input type="text" :value="config.ADMIN_EMAIL" class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-sm" disabled />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = {
  APP_NAME: 'Lotus Studio',
  APP_VERSION: '1.0.0',
  ENVIRONMENT: 'development',
  ADMIN_EMAIL: 'admin@lotusstudio.dev',
}

definePageMeta({
  title: 'Settings — Lotus Studio Admin',
  middleware: 'admin',
})
</script>
