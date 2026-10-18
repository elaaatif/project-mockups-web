<script setup>
import { Check } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { money } from '@/core/format'
import { valuationService } from '../valuation.service'

const { data: plans } = useResource(valuationService.plans)
</script>

<template>
  <div class="mx-auto max-w-6xl px-6 py-16">
    <div class="text-center">
      <p class="text-sm font-semibold tracking-widest text-brand-700 uppercase">For owners, landlords & agencies</p>
      <h1 class="mt-3 font-display text-5xl font-semibold">List your property with Haven</h1>
      <p class="mx-auto mt-4 max-w-2xl text-slate-600">Reach 40,000 monthly buyers and tenants. Pay once per listing, or subscribe for unlimited listings with our agent CRM and rental tools.</p>
    </div>
    <div class="mt-14 grid gap-6 lg:grid-cols-3">
      <div v-for="p in plans" :key="p.name" class="relative rounded-3xl p-8 ring-1" :class="p.popular ? 'bg-slate-900 text-white ring-slate-900' : 'bg-white ring-slate-200'">
        <span v-if="p.popular" class="absolute -top-3 left-8 rounded-full bg-brand-500 px-3 py-1 text-xs font-bold text-white">Best value</span>
        <h3 class="text-lg font-semibold">{{ p.name }}</h3>
        <p class="mt-4 font-display text-5xl">{{ money(p.price) }}</p>
        <p class="mt-1 text-sm opacity-60">{{ p.period }}</p>
        <ul class="mt-6 space-y-3 text-sm"><li v-for="f in p.features" :key="f" class="flex gap-2"><Check class="size-5 shrink-0 text-brand-500" />{{ f }}</li></ul>
        <RouterLink to="/valuation" class="btn mt-8 w-full" :class="p.popular ? 'btn-primary' : 'btn-secondary'">Get started</RouterLink>
      </div>
    </div>
  </div>
</template>
