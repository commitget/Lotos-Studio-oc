<template>
  <section id="faq" class="py-24 bg-white">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="font-display text-4xl sm:text-5xl text-gray-900 mb-4">
          Frequently Asked Questions
        </h2>
        <p class="text-lg text-gray-500">
          Everything you need to know about Lotus Studio.
        </p>
      </div>
      <div class="space-y-3">
        <div v-for="(item, index) in faqItems" :key="index"
          class="border border-gray-100 rounded-xl overflow-hidden transition-all duration-300"
          :class="{ 'shadow-md border-teal-100': openIndex === index }">
          <button @click="openIndex = openIndex === index ? -1 : index"
            class="w-full flex items-center justify-between px-6 py-5 text-left transition-colors hover:bg-gray-50">
            <span class="font-display text-lg text-gray-900">{{ item.question }}</span>
            <svg class="w-5 h-5 text-gray-400 transition-transform duration-300 flex-shrink-0 ml-4"
              :class="{ 'rotate-180': openIndex === index }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <Transition name="fade">
            <div v-if="openIndex === index" class="px-6 pb-5">
              <p class="text-gray-500 leading-relaxed">{{ item.answer }}</p>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const openIndex = ref(-1)

const faqItems = [
  {
    question: 'What is Lotus Studio?',
    answer: 'Lotus Studio is a professional Roblox development studio with over 5 years of experience. We specialize in creating custom Roblox experiences, selling beta testing access, and offering a marketplace for Roblox places and systems.',
  },
  {
    question: 'How does beta testing work?',
    answer: 'Our beta testing platform allows game developers to sell access to beta versions of their games. Testers can purchase access, provide feedback, and report bugs through our integrated system.',
  },
  {
    question: 'Can I buy ready-made Roblox places?',
    answer: 'Yes! Our marketplace features a curated selection of high-quality Roblox places, systems, and modules. Each product undergoes thorough quality assurance before listing.',
  },
  {
    question: 'How do I order custom development?',
    answer: 'Simply register an account and submit a development request through our platform. We will review your requirements, provide a quote, and assign a dedicated team to your project.',
  },
  {
    question: 'What payment methods do you accept?',
    answer: 'We accept payments via Bybit and «ЮMoney», supporting major credit cards, cryptocurrencies, and various payment methods depending on your region.',
  },
  {
    question: 'Is there a money-back guarantee?',
    answer: 'Yes, we offer a 14-day money-back guarantee on all marketplace purchases. Custom development projects have a satisfaction guarantee with milestone-based payments.',
  },
]
</script>
