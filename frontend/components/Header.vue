<template>
  <header v-if="!isAdminPage" class="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center space-x-2">

          <nav class="hidden md:flex ml-10 space-x-1">
            <NuxtLink v-for="item in navItems" :key="item.href" :to="item.href"
              class="px-3 py-2 text-sm text-gray-600 hover:text-teal-600 transition-colors rounded-lg hover:bg-gray-50">
              {{ item.label }}
            </NuxtLink>
          </nav>
        </div>
        <div class="flex items-center space-x-4">
          <template v-if="auth.user">
            <NuxtLink to="/profile" class="hidden md:flex items-center space-x-2 text-sm text-gray-600 hover:text-teal-600">
              <div class="w-8 h-8 rounded-full bg-teal-100 flex items-center justify-center">
                <span class="text-teal-700 font-medium text-xs">{{ auth.user.username?.[0]?.toUpperCase() }}</span>
              </div>
              <span>{{ auth.user.username }}</span>
            </NuxtLink>
            <button @click="auth.logout()" class="hidden md:inline-flex px-4 py-2 text-sm text-gray-600 hover:text-red-600">
              Logout
            </button>
          </template>
          <template v-else>
            <NuxtLink to="/login"
              class="hidden md:inline-flex px-4 py-2 text-sm font-medium text-gray-600 hover:text-teal-600 transition-colors">
              Sign In
            </NuxtLink>
            <NuxtLink to="/register"
              class="hidden md:inline-flex px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-lg hover:bg-teal-700 transition-colors shadow-sm">
              Get Started
            </NuxtLink>
          </template>
          <button @click="menuOpen = !menuOpen" class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!menuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      <Transition name="slide">
        <div v-if="menuOpen" class="md:hidden border-t border-gray-100 py-4 space-y-2">
          <NuxtLink v-for="item in navItems" :key="item.href" :to="item.href"
            @click="menuOpen = false"
            class="block px-4 py-2 text-sm text-gray-600 hover:text-teal-600 hover:bg-gray-50 rounded-lg transition-colors">
            {{ item.label }}
          </NuxtLink>
          <hr class="my-2 border-gray-100" />
          <template v-if="auth.user">
            <NuxtLink to="/profile" @click="menuOpen = false"
              class="block px-4 py-2 text-sm text-gray-600 hover:text-teal-600 rounded-lg">Profile</NuxtLink>
            <button @click="auth.logout(); menuOpen = false"
              class="block w-full text-left px-4 py-2 text-sm text-red-600 rounded-lg">Logout</button>
          </template>
          <template v-else>
            <NuxtLink to="/login" @click="menuOpen = false"
              class="block px-4 py-2 text-sm text-gray-600 rounded-lg">Sign In</NuxtLink>
            <NuxtLink to="/register" @click="menuOpen = false"
              class="block px-4 py-2 text-sm text-white bg-teal-600 rounded-lg text-center">Get Started</NuxtLink>
          </template>
        </div>
      </Transition>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const route = useRoute()
const auth = useAuthStore()
const menuOpen = ref(false)

const isAdminPage = computed(() => route.path.startsWith('/admin'))

const navItems = [
  { href: '/#hero', label: 'Home' },
  { href: '/#benefits', label: 'Why Us' },
  { href: '/#pricing', label: 'Pricing' },
  { href: '/#faq', label: 'FAQ' },
]

watch(menuOpen, (val) => {
  document.body.style.overflow = val ? 'hidden' : ''
})
</script>
