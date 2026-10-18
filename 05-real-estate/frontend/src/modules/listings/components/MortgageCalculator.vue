<script setup>
import { computed, ref } from 'vue'
import { Calculator } from 'lucide-vue-next'
import { money } from '@/core/format'

const props = defineProps({ price: Number })
const depositPct = ref(20)
const rate = ref(4.6)
const years = ref(25)

const loan = computed(() => props.price * (1 - depositPct.value / 100))
const monthly = computed(() => {
  const r = rate.value / 100 / 12
  const n = years.value * 12
  return r ? (loan.value * r) / (1 - (1 + r) ** -n) : loan.value / n
})
const stampDuty = computed(() => {
  // simplified UK SDLT bands for a main residence
  const bands = [[250000, 0], [925000, 0.05], [1500000, 0.1], [Infinity, 0.12]]
  let tax = 0, lower = 0
  for (const [upper, r] of bands) { if (props.price > lower) tax += (Math.min(props.price, upper) - lower) * r; lower = upper }
  return tax
})
</script>

<template>
  <div class="rounded-2xl bg-slate-50 p-6">
    <p class="flex items-center gap-2 font-semibold"><Calculator class="size-5 text-brand-600" /> Mortgage calculator</p>
    <div class="mt-5 grid gap-5 sm:grid-cols-3">
      <label class="text-sm"><span class="flex justify-between text-slate-500">Deposit <strong class="text-slate-800">{{ depositPct }}%</strong></span><input v-model.number="depositPct" type="range" min="5" max="60" class="mt-2 w-full accent-brand-600" /></label>
      <label class="text-sm"><span class="flex justify-between text-slate-500">Interest <strong class="text-slate-800">{{ rate }}%</strong></span><input v-model.number="rate" type="range" min="1" max="9" step="0.1" class="mt-2 w-full accent-brand-600" /></label>
      <label class="text-sm"><span class="flex justify-between text-slate-500">Term <strong class="text-slate-800">{{ years }} yrs</strong></span><input v-model.number="years" type="range" min="5" max="35" class="mt-2 w-full accent-brand-600" /></label>
    </div>
    <div class="mt-6 grid gap-4 sm:grid-cols-3">
      <div class="rounded-xl bg-white p-4 ring-1 ring-slate-200"><p class="text-xs text-slate-500">Monthly repayment</p><p class="mt-1 text-2xl font-bold text-brand-700">{{ money(monthly) }}</p></div>
      <div class="rounded-xl bg-white p-4 ring-1 ring-slate-200"><p class="text-xs text-slate-500">Deposit</p><p class="mt-1 text-xl font-bold">{{ money(price - loan) }}</p></div>
      <div class="rounded-xl bg-white p-4 ring-1 ring-slate-200"><p class="text-xs text-slate-500">Est. stamp duty</p><p class="mt-1 text-xl font-bold">{{ money(stampDuty) }}</p></div>
    </div>
  </div>
</template>
