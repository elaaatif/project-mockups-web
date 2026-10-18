<script setup>
import { ref } from 'vue'
import { ArrowLeft, Sparkles, TrendingUp } from 'lucide-vue-next'
import { act, useResource } from '@/core/resource'
import { money } from '@/core/format'
import { valuationService } from '../valuation.service'

const { data: meta } = useResource(valuationService.districts)
const step = ref(1)
const form = ref({ district: 'Islington', type: 'apartment', beds: 2, area_sqm: 80, condition: 'good', name: '', email: '', phone: '' })
const result = ref(null)
async function submit() {
  const res = await act(() => valuationService.estimate(form.value))
  if (res) { result.value = res; step.value = 3 }
}
</script>

<template>
  <div class="bg-gradient-to-b from-brand-50 to-white">
    <div class="mx-auto max-w-3xl px-6 py-16">
      <div class="text-center">
        <p class="text-sm font-semibold tracking-widest text-brand-700 uppercase">Free · 60 seconds · no obligation</p>
        <h1 class="mt-3 font-display text-5xl font-semibold">What's your home worth?</h1>
      </div>
      <div class="card mt-10 p-8 shadow-xl">
        <form v-if="step === 1" class="grid gap-5 sm:grid-cols-2" @submit.prevent="step = 2">
          <div><label class="label">Area</label><select v-model="form.district" class="input"><option v-for="d in meta?.districts" :key="d">{{ d }}</option></select></div>
          <div><label class="label">Property type</label><select v-model="form.type" class="input capitalize"><option v-for="t in meta?.types" :key="t" :value="t">{{ t }}</option></select></div>
          <div><label class="label">Bedrooms</label><input v-model.number="form.beds" type="number" min="0" max="12" class="input" /></div>
          <div><label class="label">Floor area (m²)</label><input v-model.number="form.area_sqm" type="number" min="11" required class="input" /></div>
          <div class="sm:col-span-2"><label class="label">Condition</label>
            <div class="grid grid-cols-3 gap-2"><button v-for="c in [['needs_work', 'Needs work'], ['good', 'Good'], ['excellent', 'Excellent']]" :key="c[0]" type="button" class="rounded-xl py-3 text-sm font-semibold ring-1" :class="form.condition === c[0] ? 'bg-slate-900 text-white ring-slate-900' : 'ring-slate-200'" @click="form.condition = c[0]">{{ c[1] }}</button></div></div>
          <button class="btn btn-primary sm:col-span-2">Next: where should we send it?</button>
        </form>
        <form v-else-if="step === 2" class="space-y-4" @submit.prevent="submit">
          <button type="button" class="flex items-center gap-1 text-sm text-slate-500" @click="step = 1"><ArrowLeft class="size-4" /> Back</button>
          <input v-model="form.name" required minlength="2" class="input" placeholder="Full name" />
          <input v-model="form.email" required type="email" class="input" placeholder="Email" />
          <input v-model="form.phone" class="input" placeholder="Phone (optional)" />
          <button class="btn btn-primary w-full"><Sparkles class="size-4" /> Show my valuation</button>
          <p class="text-center text-xs text-slate-400">A local agent may contact you to arrange a free in-person valuation.</p>
        </form>
        <div v-else class="text-center">
          <p class="text-sm text-slate-500">Estimated value for your {{ form.beds }}-bed {{ form.type }} in {{ form.district }}</p>
          <p class="mt-3 font-display text-6xl font-semibold">{{ money(result.estimate) }}</p>
          <p class="mt-2 text-slate-500">Likely range {{ money(result.low) }} – {{ money(result.high) }}</p>
          <div class="mt-8 grid gap-4 sm:grid-cols-3">
            <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs text-slate-500">Your £/m²</p><p class="mt-1 text-xl font-bold">{{ money(result.per_sqm) }}</p></div>
            <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs text-slate-500">Area average</p><p class="mt-1 text-xl font-bold">{{ money(result.district_avg_per_sqm) }}</p></div>
            <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs text-slate-500">Rental estimate</p><p class="mt-1 text-xl font-bold">{{ money(result.rent_estimate) }} pcm</p></div>
          </div>
          <p class="mt-6 flex items-center justify-center gap-2 text-sm font-semibold text-emerald-700"><TrendingUp class="size-4" /> {{ form.district }} prices are up 4.2% year on year</p>
          <RouterLink to="/list-your-property" class="btn btn-primary mt-8">Sell or let with Haven</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>
