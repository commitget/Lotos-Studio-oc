<template>
  <footer v-if="!isAdminPage" class="bg-gray-900 text-gray-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
        <div class="col-span-2 md:col-span-1">
          <div class="mb-4">
            <span class="font-display text-xl text-white">Lotus Studio</span>
          </div>
          <p class="text-sm text-gray-400 leading-relaxed mb-6">
            Professional Roblox development studio crafting exceptional gaming experiences since 2020.
          </p>
          <div class="flex space-x-4">
            <a v-for="social in socialLinks" :key="social.name" :href="social.url" target="_blank" :title="social.name"
              class="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-teal-600 transition-colors">
              <img :src="social.logo" :alt="social.name" class="w-5 h-5 brightness-0 invert" />
            </a>
          </div>
        </div>
        <div v-for="group in footerGroups" :key="group.title">
          <h4 class="font-display text-sm text-white mb-4 uppercase tracking-wider">{{ group.title }}</h4>
          <ul class="space-y-3">
            <li v-for="link in group.links" :key="link.label">
              <NuxtLink :to="link.href" class="text-sm text-gray-400 hover:text-white transition-colors">
                {{ link.label }}
              </NuxtLink>
            </li>
          </ul>
        </div>
      </div>
      <div class="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <p class="text-sm text-gray-500">&copy; {{ new Date().getFullYear() }} Lotus Studio. All rights reserved.</p>
        <div class="flex space-x-6 text-sm text-gray-500">
          <NuxtLink to="/privacy" class="hover:text-white transition-colors">Privacy Policy</NuxtLink>
          <NuxtLink to="/terms" class="hover:text-white transition-colors">Terms of Service</NuxtLink>
          <NuxtLink to="/docs" class="hover:text-white transition-colors">Documentation</NuxtLink>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const route = useRoute()
const isAdminPage = computed(() => route.path.startsWith('/admin'))

const socialLinks = [
  { name: 'Roblox',  url: 'https://www.roblox.com/share/g/32638472', logo: 'https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/roblox.svg' },
  { name: 'Discord', url: 'https://discord.gg/YAC8Vsra', logo: 'https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/discord.svg' },
  // { name: 'Twitter', url: 'https://twitter.com', logo: 'https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/x.svg' },
  // { name: 'YouTube', url: 'https://youtube.com', logo: 'https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/youtube.svg' },
]

const footerGroups = [
  {
    title: 'Product',
    links: [
      { label: 'Marketplace', href: '/marketplace' },
      { label: 'Beta Testing', href: '/beta' },
      { label: 'Pricing', href: '/#pricing' },
      { label: 'FAQ', href: '/#faq' },
    ],
  },
  {
    title: 'Company',
    links: [
      { label: 'About', href: '/about' },
      { label: 'Blog', href: '/blog' },
      { label: 'Contact', href: '/contact' },
    ],
  },
  {
    title: 'Support',
    links: [
      { label: 'Help Center', href: '/support' },
    ],
  },
]
</script>
