<script setup>
import { Check } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { catalogService } from '../catalog.service'

const { data: plans } = useResource(catalogService.plans)
</script>

<template>
  <div class="mx-auto max-w-7xl px-6 py-16">
    <div class="text-center">
      <h1 class="text-5xl font-bold tracking-tight">Plans for learners, teams and institutions</h1>
      <p class="mx-auto mt-4 max-w-2xl text-slate-600">Buy single courses, subscribe for everything, or license Brightpath for your company or training centre.</p>
    </div>
    <div class="mt-14 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      <div v-for="p in plans" :key="p.name" class="relative flex flex-col rounded-3xl p-7 ring-1" :class="p.popular ? 'bg-brand-600 text-white ring-brand-600' : 'bg-white ring-slate-200'">
        <span v-if="p.popular" class="absolute -top-3 left-7 rounded-full bg-amber-400 px-3 py-1 text-xs font-bold text-amber-950">Most popular</span>
        <p class="text-xs font-semibold uppercase opacity-70">{{ p.audience }}</p>
        <h3 class="mt-1 text-xl font-bold">{{ p.name }}</h3>
        <p class="mt-4"><span class="text-4xl font-bold">{{ p.price }}</span> <span class="text-sm opacity-70">{{ p.period }}</span></p>
        <ul class="mt-6 flex-1 space-y-3 text-sm"><li v-for="f in p.features" :key="f" class="flex gap-2"><Check class="size-5 shrink-0" :class="p.popular ? 'text-white' : 'text-brand-600'" />{{ f }}</li></ul>
        <RouterLink :to="p.audience === 'Individuals' ? '/courses' : '/app'" class="btn mt-8 w-full" :class="p.popular ? 'bg-white text-brand-700 hover:bg-brand-50' : 'btn-secondary'">{{ p.price === 'Custom' ? 'Talk to sales' : 'Get started' }}</RouterLink>
      </div>
    </div>
  </div>
</template>
