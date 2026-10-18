<script setup>
// Two-panel lead form: an instant price estimate on the left feeds the enquiry on the right.
import { ref, watch } from 'vue'
import { CheckCircle2, Send, Zap } from 'lucide-vue-next'
import { act, useResource } from '@/core/resource'
import { money } from '@/core/format'
import { portfolioService } from '../portfolio.service'

const { data: opts } = useResource(portfolioService.options)
const choice = ref({ project_type: 'booking', addons: ['payments'], urgency: 'standard' })
const est = ref(null)
watch(choice, async () => { est.value = await portfolioService.estimate(choice.value).catch(() => null) }, { deep: true, immediate: true })

const form = ref({ name: '', email: '', company: '', budget: '', message: '' })
const sent = ref(false)
async function send() {
  const body = { ...form.value, project_type: est.value?.label ?? '', estimate: est.value }
  if (await act(() => portfolioService.send(body), 'Message sent — I\'ll reply within 24 hours')) sent.value = true
}
</script>

<template>
  <div class="grid gap-6 lg:grid-cols-2">
    <div class="rounded-3xl border border-white/10 bg-white/[.03] p-8">
      <p class="flex items-center gap-2 text-sm font-semibold text-brand-300"><Zap class="size-4" /> Instant estimate</p>
      <p class="mt-6 text-xs font-semibold tracking-wider text-zinc-500 uppercase">What are we building?</p>
      <div class="mt-3 flex flex-wrap gap-2">
        <button v-for="t in opts?.types" :key="t.key" class="rounded-full border px-3.5 py-1.5 text-sm transition" :class="choice.project_type === t.key ? 'border-brand-400 bg-brand-400 font-semibold text-black' : 'border-white/10 hover:border-white/30'" @click="choice.project_type = t.key">{{ t.label }}</button>
      </div>
      <p class="mt-6 text-xs font-semibold tracking-wider text-zinc-500 uppercase">Add-ons</p>
      <div class="mt-3 flex flex-wrap gap-2">
        <label v-for="a in opts?.addons" :key="a.key" class="cursor-pointer rounded-full border px-3.5 py-1.5 text-sm transition" :class="choice.addons.includes(a.key) ? 'border-white bg-white text-black' : 'border-white/10 hover:border-white/30'">
          <input v-model="choice.addons" type="checkbox" :value="a.key" class="sr-only" />{{ a.label }}
        </label>
      </div>
      <p class="mt-6 text-xs font-semibold tracking-wider text-zinc-500 uppercase">Timeline</p>
      <div class="mt-3 inline-flex rounded-full border border-white/10 p-1">
        <button v-for="u in [['standard', 'Standard'], ['fast', 'Fast-track']]" :key="u[0]" class="rounded-full px-4 py-1.5 text-sm" :class="choice.urgency === u[0] ? 'bg-white font-semibold text-black' : ''" @click="choice.urgency = u[0]">{{ u[1] }}</button>
      </div>
      <div v-if="est" class="mt-8 rounded-2xl bg-gradient-to-br from-brand-400 to-lime-300 p-6 text-black">
        <p class="text-sm font-medium opacity-70">{{ est.label }}</p>
        <p class="mt-1 text-4xl font-bold tracking-tight">{{ money(est.low) }} – {{ money(est.high) }}</p>
        <p class="mt-2 text-sm">≈ {{ est.weeks }} weeks · optional care plan {{ money(est.monthly_care) }}/mo</p>
      </div>
    </div>

    <div class="rounded-3xl border border-white/10 bg-white/[.03] p-8">
      <div v-if="sent" class="grid h-full place-items-center text-center"><div><CheckCircle2 class="mx-auto size-14 text-brand-400" /><p class="mt-4 text-2xl font-semibold text-white">Thanks — message received!</p><p class="mt-2 text-zinc-400">I'll get back to you within 24 hours with questions and next steps.</p></div></div>
      <form v-else class="space-y-4" @submit.prevent="send">
        <p class="text-sm font-semibold text-brand-300">Tell me about your project</p>
        <div class="grid gap-4 sm:grid-cols-2">
          <input v-model="form.name" required minlength="2" class="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none placeholder:text-zinc-500 focus:border-brand-400" placeholder="Your name" />
          <input v-model="form.email" required type="email" class="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none placeholder:text-zinc-500 focus:border-brand-400" placeholder="Email" />
        </div>
        <input v-model="form.company" class="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none placeholder:text-zinc-500 focus:border-brand-400" placeholder="Company (optional)" />
        <select v-model="form.budget" class="w-full rounded-xl border border-white/10 bg-[#141414] px-4 py-3 text-white outline-none focus:border-brand-400">
          <option value="">Budget range</option><option>Under $3k</option><option>$3k – $10k</option><option>$10k – $25k</option><option>$25k+</option>
        </select>
        <textarea v-model="form.message" required minlength="10" rows="6" class="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none placeholder:text-zinc-500 focus:border-brand-400" placeholder="What problem should the software solve? Who will use it?" />
        <p v-if="est" class="text-xs text-zinc-500">Your estimate ({{ est.label }}, {{ money(est.low) }}–{{ money(est.high) }}) will be attached.</p>
        <button class="inline-flex w-full items-center justify-center gap-2 rounded-full bg-brand-400 px-6 py-3.5 font-semibold text-black transition hover:bg-brand-300">Send enquiry <Send class="size-4" /></button>
      </form>
    </div>
  </div>
</template>
