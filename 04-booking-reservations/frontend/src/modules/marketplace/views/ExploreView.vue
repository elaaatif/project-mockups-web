<script setup>
import { reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import BusinessCard from '../components/BusinessCard.vue'
import { CATEGORY_ICONS, marketplaceService } from '../marketplace.service'

const route = useRoute()
const router = useRouter()
const f = reactive({ q: route.query.q ?? '', category: route.query.category ?? '' })
const { data: categories } = useResource(marketplaceService.categories)
const { data, loading, reload } = useResource(() => marketplaceService.list(f))
watch(() => route.query, (q) => { f.q = q.q ?? ''; f.category = q.category ?? '' })
let t
watch(f, () => { clearTimeout(t); t = setTimeout(() => { router.replace({ query: { ...(f.q && { q: f.q }), ...(f.category && { category: f.category }) } }); reload() }, 200) })
</script>

<template>
  <div class="mx-auto max-w-7xl px-6 py-12">
    <h1 class="text-4xl font-extrabold tracking-tight">Explore businesses</h1>
    <div class="mt-6 flex flex-wrap items-center gap-3">
      <div class="relative min-w-64 flex-1"><Search class="absolute top-1/2 left-3.5 size-4 -translate-y-1/2 text-slate-400" /><input v-model="f.q" class="input pl-10" placeholder="Search services, businesses or areas" /></div>
    </div>
    <div class="mt-4 flex flex-wrap gap-2">
      <button class="rounded-full px-4 py-2 text-sm font-bold ring-1" :class="!f.category ? 'bg-slate-900 text-white ring-slate-900' : 'ring-slate-200 hover:ring-slate-400'" @click="f.category = ''">All</button>
      <button v-for="c in categories" :key="c.slug" class="inline-flex items-center gap-1.5 rounded-full px-4 py-2 text-sm font-bold ring-1" :class="f.category === c.slug ? 'bg-brand-600 text-white ring-brand-600' : 'ring-slate-200 hover:ring-slate-400'" @click="f.category = c.slug">
        <component :is="CATEGORY_ICONS[c.icon]" class="size-4" />{{ c.name }} <span class="opacity-60">{{ c.count }}</span>
      </button>
    </div>
    <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3" :class="{ 'opacity-60': loading }"><BusinessCard v-for="b in data" :key="b.slug" :business="b" /></div>
    <p v-if="data && !data.length" class="py-20 text-center text-slate-500">No businesses match your search.</p>
  </div>
</template>
