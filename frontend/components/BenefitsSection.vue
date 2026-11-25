<template>
  <section id="benefits" class="py-24 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-3xl mx-auto mb-16">
        <h2 class="font-display text-4xl sm:text-5xl text-gray-900 mb-4">
          Why Choose Lotus Studio?
        </h2>
        <p class="text-lg text-gray-500">
          We combine technical excellence with creative vision to deliver outstanding Roblox experiences.
        </p>
      </div>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="(benefit, index) in benefits" :key="benefit.title"
          class="group p-8 rounded-2xl border border-gray-100 hover:border-teal-100 hover:shadow-xl hover:shadow-teal-50/50 transition-all duration-300"
          :style="{ animationDelay: `${index * 100}ms` }">
          <h3 class="font-display text-xl text-gray-900 mb-3">{{ benefit.title }}</h3>
          <p class="text-gray-500 leading-relaxed">{{ benefit.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { CodeIcon, TestIcon, StoreIcon, CustomizeIcon, ShieldIcon, HelpIcon } from './icons'

const benefits = [
  {
    title: 'Expert LuaU / Roblox TS Development',
    description: '5+ years of specialized Roblox development experience. Our team masters every aspect of LuaU.',
    icon: CodeIcon,
  },
  {
    title: 'Beta Testing Platform',
    description: 'Sell access to beta versions of your games. Manage testers and collect valuable feedback.',
    icon: TestIcon,
  },
  {
    title: 'Marketplace Access',
    description: 'Buy and sell ready-made Roblox places, systems, and plugins with confidence.',
    icon: StoreIcon,
  },
  {
    title: 'Custom Development',
    description: 'From concept to launch — we build custom Roblox experiences tailored to your vision.',
    icon: CustomizeIcon,
  },
  {
    title: 'Quality Assurance',
    description: 'Rigorous testing ensures every product meets the highest standards of quality and performance.',
    icon: ShieldIcon,
  },
  {
    title: '24/7 Support',
    description: 'Dedicated support team available around the clock to help you succeed.',
    icon: HelpIcon,
  },
]
</script>
