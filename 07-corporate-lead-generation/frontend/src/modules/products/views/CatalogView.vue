<script setup>
import { reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Clock, FileDown, Search } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import ProductVisual from '../components/ProductVisual.vue'
import { productsService } from '../products.service'

const route = useRoute()
const router = useRouter()
const f = reactive({ category: route.query.category ?? '', q: '' })
const { data: cats } = useResource(productsService.categories)
const { data, reload } = useResource(() => productsService.list(f))
watch(() => route.query.category, (c) => { f.category = c ?? '' })
let t
watch(f, () => { clearTimeout(t); t = setTimeout(() => { router.replace({ query: f.category ? { category: f.category } : {} }); reload() }, 200) })
</script>

<template>
  <div>
    <section class="bg-slate-950 py-16 text-white"><div class="mx-auto max-w-7xl px-6"><p class="text-sm font-bold tracking-[.2em] text-brand-400 uppercase">Catalogue</p><h1 class="mt-3 text-5xl font-black uppercase">Industrial products</h1><p class="mt-3 max-w-2xl text-slate-400">Full specifications, certifications and downloadable datasheets. Request a quote for any configuration.</p></div></section>
    <div class="mx-auto grid max-w-7xl gap-10 px-6 py-12 lg:grid-cols-4">
      <aside class="space-y-6">
        <div class="relative"><Search class="absolute top-1/2 left-3.5 size-4 -translate-y-1/2 text-slate-400" /><input v-model="f.q" class="input !rounded-none pl-10" placeholder="Search products or applications" /></div>
        <nav class="border border-slate-200">
          <button class="flex w-full justify-between border-b border-slate-100 px-4 py-3 text-left text-sm font-semibold" :class="!f.category ? 'bg-slate-950 text-white' : 'hover:bg-slate-50'" @click="f.category = ''">All products</button>
          <button v-for="c in cats" :key="c.slug" class="flex w-full justify-between border-b border-slate-100 px-4 py-3 text-left text-sm font-semibold last:border-0" :class="f.category === c.slug ? 'bg-slate-950 text-white' : 'hover:bg-slate-50'" @click="f.category = c.slug">{{ c.name }}<span class="opacity-50">{{ c.count }}</span></button>
        </nav>
      </aside>
      <div class="grid content-start gap-6 sm:grid-cols-2 lg:col-span-3 xl:grid-cols-3">
        <RouterLink v-for="p in data" :key="p.id" :to="`/products/${p.slug}`" class="group flex flex-col border border-slate-200 transition hover:border-brand-500 hover:shadow-xl">
          <ProductVisual :category="p.category" :sku="p.sku" class="aspect-[4/3]" />
          <div class="flex flex-1 flex-col p-5">
            <p class="font-bold group-hover:text-brand-700">{{ p.name }}</p>
            <p class="mt-2 line-clamp-2 text-sm text-slate-500">{{ p.summary }}</p>
            <div class="mt-4 flex flex-wrap gap-1.5"><span v-for="c in p.certifications" :key="c" class="bg-slate-100 px-2 py-0.5 text-[11px] font-bold text-slate-600">{{ c }}</span></div>
            <div class="mt-auto flex items-center justify-between pt-5 text-xs text-slate-500"><span class="flex items-center gap-1"><Clock class="size-3.5" />{{ p.lead_time_weeks }} wk lead time</span><span class="flex items-center gap-1 font-semibold text-brand-700"><FileDown class="size-3.5" />Datasheet</span></div>
          </div>
        </RouterLink>
        <p v-if="data && !data.length" class="col-span-full py-16 text-center text-slate-500">No products match.</p>
      </div>
    </div>
  </div>
</template>
