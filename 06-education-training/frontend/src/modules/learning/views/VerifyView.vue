<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { BadgeCheck, ShieldX } from 'lucide-vue-next'
import { date } from '@/core/format'
import { learningService } from '../learning.service'

const route = useRoute()
const id = ref(route.query.id ?? '')
const cert = ref(null)
const error = ref('')
async function verify() {
  error.value = ''
  cert.value = null
  try { cert.value = await learningService.certificate(id.value) } catch (e) { error.value = e.message }
}
onMounted(() => id.value && verify())
</script>

<template>
  <div class="mx-auto max-w-2xl px-6 py-16 text-center">
    <h1 class="text-4xl font-bold tracking-tight">Verify a certificate</h1>
    <p class="mt-2 text-slate-600">Employers can confirm any Brightpath credential instantly.</p>
    <form class="mt-8 flex gap-2" @submit.prevent="verify">
      <input v-model="id" required class="input font-mono uppercase" placeholder="BP-XXXX-2026" />
      <button class="btn btn-primary shrink-0">Verify</button>
    </form>
    <p class="mt-2 text-sm text-slate-500">Try <button class="font-mono font-semibold text-brand-700 underline" @click="id = 'BP-7F3K-2026'; verify()">BP-7F3K-2026</button></p>
    <div v-if="cert" class="mt-10 rounded-3xl bg-emerald-50 p-8 text-left ring-1 ring-emerald-200">
      <p class="flex items-center gap-2 font-bold text-emerald-700"><BadgeCheck class="size-6" /> Valid credential</p>
      <dl class="mt-5 grid grid-cols-2 gap-4 text-sm">
        <div><dt class="text-slate-500">Learner</dt><dd class="font-semibold">{{ cert.learner }}</dd></div>
        <div><dt class="text-slate-500">Course</dt><dd class="font-semibold">{{ cert.course }}</dd></div>
        <div><dt class="text-slate-500">Score</dt><dd class="font-semibold">{{ cert.score }}%</dd></div>
        <div><dt class="text-slate-500">Issued</dt><dd class="font-semibold">{{ date(cert.issued) }}</dd></div>
      </dl>
      <RouterLink :to="`/certificate/${cert.id}`" class="btn btn-secondary mt-6">View certificate</RouterLink>
    </div>
    <p v-if="error" class="mt-10 flex items-center justify-center gap-2 rounded-2xl bg-rose-50 p-6 font-semibold text-rose-700"><ShieldX class="size-5" />{{ error }}</p>
  </div>
</template>
