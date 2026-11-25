<template>
  <div class="min-h-screen bg-gray-50 py-24 px-4">
    <div class="max-w-2xl mx-auto">
      <div class="text-center mb-8">
        <h1 class="font-display text-4xl text-gray-900">Help Center</h1>
        <p class="text-gray-500 mt-2">Submit a ticket and we'll get back to you as soon as possible</p>
      </div>
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Subject</label>
            <input v-model="subject" type="text" required
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all"
              placeholder="What is your issue about?" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Message</label>
            <textarea v-model="message" required rows="6"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all resize-none"
              placeholder="Describe your issue in detail..."></textarea>
          </div>
          <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
          <p v-if="success" class="text-green-600 text-sm font-medium">Ticket submitted! We'll review it shortly.</p>
          <button type="submit" :disabled="loading"
            class="w-full py-3 bg-teal-600 text-white font-medium rounded-xl hover:bg-teal-700 transition-colors disabled:opacity-50">
            {{ loading ? 'Submitting...' : 'Submit Ticket' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { API_BASE, apiFetch } from '~/utils/api'

const subject = ref('')
const message = ref('')
const error = ref('')
const success = ref(false)
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  success.value = false
  loading.value = true
  try {
    await apiFetch(`${API_BASE}/support/tickets`, {
      method: 'POST',
      body: { subject: subject.value, message: message.value },
    })
    success.value = true
    subject.value = ''
    message.value = ''
  } catch (e: any) {
    error.value = e?.data?.detail || 'Failed to submit ticket'
  } finally {
    loading.value = false
  }
}

definePageMeta({
  title: 'Help Center — Lotus Studio',
  middleware: 'auth',
})
</script>
