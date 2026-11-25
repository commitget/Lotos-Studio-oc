<template>
  <section id="pricing" class="relative py-24 bg-gray-50 overflow-hidden">
    <div class="absolute bottom-0 right-0 w-48 h-48 sm:w-64 sm:h-64 lg:w-80 lg:h-80 z-10 opacity-60 pointer-events-none">
      <img :src="fireflyImg" alt="Firefly Cat" class="w-full h-full object-contain object-bottom" />
    </div>
    <div class="sticky top-16 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="font-display text-4xl sm:text-5xl text-gray-900 mb-4">
            Transparent Pricing
          </h2>
          <p class="text-lg text-gray-500">
            Choose the plan that fits your needs. All plans include our core features.
          </p>
        </div>
        <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div v-for="(plan, index) in plans" :key="plan.name"
            class="relative bg-white rounded-2xl border p-8 transition-all duration-300 hover:shadow-xl"
            :class="[plan.featured ? 'border-teal-500 shadow-lg shadow-teal-100 scale-105' : 'border-gray-100 hover:border-teal-100']">
            <div v-if="plan.featured" class="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 bg-teal-600 text-white text-xs font-medium rounded-full">
              Most Popular
            </div>
            <div class="text-center mb-8">
              <h3 class="font-display text-xl text-gray-900 mb-2">{{ plan.name }}</h3>
              <p class="text-gray-500 text-sm mb-6">{{ plan.description }}</p>
              <div class="flex items-baseline justify-center gap-1">
                <span class="text-4xl font-display text-gray-900">${{ plan.price }}</span>
                <span class="text-gray-400 text-sm">/{{ plan.period }}</span>
              </div>
            </div>
            <ul class="space-y-4 mb-8">
              <li v-for="feature in plan.features" :key="feature" class="flex items-center space-x-3 text-sm text-gray-600">
                <svg class="w-5 h-5 text-teal-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>{{ feature }}</span>
              </li>
            </ul>
            <NuxtLink to="https://t.me/lotusstudiodevbot"
              class="block w-full py-3 text-center font-medium rounded-xl transition-all"
              :class="plan.featured
                ? 'bg-teal-600 text-white hover:bg-teal-700 shadow-md shadow-teal-200'
                : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200'">
              {{ plan.featured ? 'Get Started' : 'Choose Plan' }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import fireflyImg from '~/assets/img/Firefly_cat.png'

const plans = [
  {
    name: 'Starter',
    description: 'Perfect for getting started',
    price: '30',
    period: 'mo',
    featured: false,
    features: [
      'Basic beta testing access',
      'Up to 3 games',
      'Community support',
      'Basic analytics',
      '1 team member',
    ],
  },
  {
    name: 'Professional',
    description: 'For growing studios',
    price: '79',
    period: 'mo',
    featured: true,
    features: [
      'Full beta testing platform',
      'Unlimited games',
      'Priority support',
      'Advanced analytics',
      'Up to 10 team members',
      'Custom branding',
    ],
  },
  {
    name: 'Enterprise',
    description: 'For large organizations',
    price: '299',
    period: 'mo',
    featured: false,
    features: [
      'Everything in Professional',
      'Unlimited team members',
      'Dedicated manager or CRM',
      'Custom integrations',
      'SLA guarantee',
      'White-label solution',
      'Early access to features',
    ],
  },
]
</script>
