<template>
  <aside class="fixed left-0 top-0 bottom-0 w-64 bg-gray-900 text-white z-40 hidden md:block">
    <div class="p-6">
      <nav class="space-y-1 mt-4">
        <NuxtLink v-for="item in navItems" :key="item.to" :to="item.to"
          class="flex items-center space-x-3 px-4 py-3 rounded-xl text-sm transition-colors"
          :class="isActive(item.to) ? 'bg-teal-600 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800'">
          <component :is="item.icon" class="w-5 h-5" />
          <span>{{ item.label }}</span>
        </NuxtLink>
      </nav>
    </div>
    <div class="absolute bottom-0 left-0 right-0 p-6 border-t border-gray-800">
      <NuxtLink to="/" class="flex items-center space-x-2 text-sm text-gray-400 hover:text-white transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span>Back to Site</span>
      </NuxtLink>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { DashboardIcon, UsersIcon, ProductsIcon, LogsIcon, SettingsIcon, SupportIcon } from './icons'

const route = useRoute()

const navItems = [
  { to: '/admin', label: 'Dashboard', icon: DashboardIcon },
  { to: '/admin/users', label: 'Users', icon: UsersIcon },
  { to: '/admin/products', label: 'Products', icon: ProductsIcon },
  { to: '/admin/support', label: 'Support', icon: SupportIcon },
  { to: '/admin/logs', label: 'Change Logs', icon: LogsIcon },
  { to: '/admin/settings', label: 'Settings', icon: SettingsIcon },
]

function isActive(path: string) {
  return route.path === path
}
</script>
