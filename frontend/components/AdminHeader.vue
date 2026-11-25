<template>
  <div class="bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between">
    <div>
      <h1 class="font-display text-xl text-gray-900">{{ title }}</h1>
      <nav class="flex items-center space-x-2 text-sm text-gray-400 mt-1">
        <NuxtLink to="/admin" class="hover:text-teal-600">Admin</NuxtLink>
        <span>/</span>
        <span class="text-gray-600">{{ title }}</span>
      </nav>
    </div>
    <div class="flex items-center space-x-4">
      <NuxtLink to="/admin/settings" class="p-2 text-gray-400 hover:text-teal-600 transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </NuxtLink>
      <NuxtLink to="/profile" class="flex items-center space-x-2 text-sm text-gray-600 hover:text-teal-600">
        <div class="w-8 h-8 rounded-full bg-teal-100 flex items-center justify-center">
          <span class="text-teal-700 font-medium text-xs">A</span>
        </div>
        <span class="hidden sm:inline">Admin</span>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ title: string }>()
</script>
