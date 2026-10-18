<script setup>
import { TrendingDown, TrendingUp } from 'lucide-vue-next'

defineProps({ label: String, value: [String, Number], icon: Object, delta: Number, hint: String, tone: { type: String, default: 'brand' } })

const tones = {
  brand: 'bg-brand-50 text-brand-600',
  emerald: 'bg-emerald-50 text-emerald-600',
  amber: 'bg-amber-50 text-amber-600',
  rose: 'bg-rose-50 text-rose-600',
  sky: 'bg-sky-50 text-sky-600',
}
</script>

<template>
  <div class="card p-5 transition hover:-translate-y-0.5 hover:shadow-md">
    <div class="flex items-center justify-between">
      <p class="text-sm font-medium text-slate-500">{{ label }}</p>
      <span class="grid size-10 place-items-center rounded-xl" :class="tones[tone]"><component :is="icon" class="size-5" /></span>
    </div>
    <p class="mt-3 text-2xl font-extrabold tracking-tight text-slate-900">{{ value }}</p>
    <div class="mt-1 flex items-center gap-1.5 text-xs">
      <span v-if="delta !== undefined" class="inline-flex items-center gap-0.5 font-semibold" :class="delta >= 0 ? 'text-emerald-600' : 'text-rose-600'">
        <component :is="delta >= 0 ? TrendingUp : TrendingDown" class="size-3.5" /> {{ Math.abs(delta) }}%
      </span>
      <span class="text-slate-400">{{ hint }}</span>
    </div>
  </div>
</template>
