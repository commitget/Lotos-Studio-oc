<template>
  <section id="hero" class="relative min-h-screen flex items-center overflow-hidden">
    <div class="absolute inset-0 bg-gray-900">
      <img :src="heroImg" alt="Lotus Studio" class="w-full h-full object-cover opacity-60" />
      <div class="absolute inset-0 bg-gradient-to-r from-gray-900/90 via-gray-900/60 to-transparent"></div>
    </div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 relative z-10 w-full">
      <div class="max-w-2xl">
        <h1 ref="titleRef" class="font-display text-5xl sm:text-6xl lg:text-7xl text-white leading-tight">
          Build the Next
          <span class="text-teal-400">Roblox</span>
          Masterpiece
        </h1>
        <p ref="descRef" class="text-lg sm:text-xl text-gray-300 leading-relaxed max-w-xl mt-6">
          Professional LuaU development studio crafting exceptional Roblox experiences.
          From beta testing to full-scale game development, we bring your vision to life.
        </p>
        <div ref="ctaRef" class="flex flex-wrap gap-4 mt-10">
          <NuxtLink to="https://t.me/lotusstudiodevbot"
            class="inline-flex items-center px-8 py-4 bg-teal-500 text-white font-medium rounded-xl hover:bg-teal-400 transition-all shadow-lg shadow-teal-500/30">
            Start Your Project
            <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </NuxtLink>
          <a href="#benefits"
            class="inline-flex items-center px-8 py-4 bg-white/10 text-white font-medium rounded-xl border border-white/20 hover:bg-white/20 transition-all backdrop-blur-sm">
            Learn More
          </a>
        </div>
        <div ref="statsRef" class="flex flex-wrap gap-8 pt-8 mt-12 border-t border-white/10">
          <div v-for="stat in stats" :key="stat.label" class="text-center">
            <div class="font-display text-3xl text-white">{{ stat.value }}</div>
            <div class="text-sm text-gray-400">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import heroImg from '~/assets/img/hero.png'

const stats = [
  { value: '7', label: 'Projects' },
  { value: '5+', label: 'Years Active' },
  { value: '88%', label: 'Satisfaction' },
  { value: '24/7', label: 'Support' },
]

const titleRef = ref<HTMLElement>()
const descRef = ref<HTMLElement>()
const ctaRef = ref<HTMLElement>()
const statsRef = ref<HTMLElement>()

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade-in', 'opacity-100')
        entry.target.classList.remove('opacity-0')
      }
    })
  }, { threshold: 0.1 })

  ;[titleRef, descRef, ctaRef, statsRef].forEach((ref) => {
    if (ref.value) {
      ref.value.classList.add('opacity-0')
      observer.observe(ref.value)
    }
  })
})
</script>
