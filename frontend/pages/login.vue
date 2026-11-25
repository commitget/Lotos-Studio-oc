<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-24 px-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="font-display text-3xl text-gray-900">Welcome Back</h1>
        <p class="text-gray-500 mt-2">Sign in to your Lotus Studio account</p>
      </div>
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="email" type="email" required
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all"
              placeholder="you@example.com" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input v-model="password" type="password" required
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all"
              placeholder="••••••••" />
          </div>
          <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
          <button type="submit" :disabled="loading"
            class="w-full py-3 bg-teal-600 text-white font-medium rounded-xl hover:bg-teal-700 transition-colors disabled:opacity-50">
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-500">
            Don't have an account?
            <NuxtLink to="/register" class="text-teal-600 hover:text-teal-700 font-medium">Sign up</NuxtLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const auth = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    navigateTo('/')
  } catch (e: any) {
    error.value = e?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}

definePageMeta({
  title: 'Sign In — Lotus Studio',
})
</script>
