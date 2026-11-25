<template>
  <div class="min-h-screen bg-gray-50 py-24 px-4">
    <div class="max-w-4xl mx-auto">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="bg-gradient-to-r from-teal-600 to-teal-800 px-8 py-12">
          <div class="flex flex-col sm:flex-row items-center sm:space-x-6 text-center sm:text-left">
            <div class="w-20 h-20 rounded-full bg-white/20 flex items-center justify-center shrink-0">
              <span class="text-3xl font-display text-white">{{ auth.user?.username?.[0]?.toUpperCase() }}</span>
            </div>
            <div class="text-white mt-3 sm:mt-0">
              <h1 class="font-display text-2xl sm:text-3xl break-all">{{ auth.user?.username }}</h1>
              <p class="text-teal-100">{{ auth.user?.email }}</p>
              <span class="inline-block mt-2 px-3 py-1 bg-white/20 rounded-full text-sm text-white capitalize">
                {{ auth.user?.role }}
              </span>
            </div>
          </div>
        </div>
        <div class="p-8">
          <div class="grid md:grid-cols-2 gap-8">
            <div>
              <h3 class="font-display text-lg text-gray-900 mb-4">Account Details</h3>
              <dl class="space-y-4">
                <div>
                  <dt class="text-sm text-gray-500">Email</dt>
                  <dd class="text-gray-900">{{ auth.user?.email }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Username</dt>
                  <dd class="text-gray-900">{{ auth.user?.username }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Role</dt>
                  <dd class="text-gray-900 capitalize">{{ auth.user?.role }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Verified</dt>
                  <dd>
                    <span :class="auth.user?.is_verified ? 'text-green-600' : 'text-yellow-600'" class="text-sm font-medium">
                      {{ auth.user?.is_verified ? 'Verified' : 'Pending' }}
                    </span>
                  </dd>
                </div>
              </dl>
            </div>
            <div>
              <h3 class="font-display text-lg text-gray-900 mb-4">Quick Links</h3>
              <div class="space-y-3">
                <NuxtLink to="/admin" v-if="auth.isAdmin"
                  class="flex items-center justify-between px-4 py-3 bg-gray-50 rounded-xl hover:bg-teal-50 transition-colors">
                  <span class="text-gray-700">Admin Dashboard</span>
                  <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </NuxtLink>
                <NuxtLink to="/marketplace"
                  class="flex items-center justify-between px-4 py-3 bg-gray-50 rounded-xl hover:bg-teal-50 transition-colors">
                  <span class="text-gray-700">Browse Marketplace</span>
                  <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </NuxtLink>
                <NuxtLink to="/beta"
                  class="flex items-center justify-between px-4 py-3 bg-gray-50 rounded-xl hover:bg-teal-50 transition-colors">
                  <span class="text-gray-700">Beta Testing</span>
                  <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </NuxtLink>
                <button @click="auth.logout()"
                  class="flex items-center justify-between w-full px-4 py-3 bg-red-50 rounded-xl hover:bg-red-100 transition-colors">
                  <span class="text-red-600">Sign Out</span>
                  <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const auth = useAuthStore()

definePageMeta({
  title: 'Profile — Lotus Studio',
  middleware: 'auth',
})
</script>
