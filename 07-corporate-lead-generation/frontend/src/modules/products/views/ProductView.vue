<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowRight, CheckCircle2, ChevronRight, Clock, FileDown, ShieldCheck } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { setSeo } from '@/core/seo'
import { toast } from '@/core/toast'
import ProductVisual from '../components/ProductVisual.vue'
import { productsService } from '../products.service'

const route = useRoute()
const { data: p, reload } = useResource(() => productsService.detail(route.params.slug))
watch(() => route.params.slug, (s) => s && reload())
watch(p, (v) => v && setSeo({ title: v.name, description: v.summary, jsonLd: { '@type': 'Product', name: v.name, sku: v.sku, description: v.summary, brand: { '@type': 'Brand', name: 'Vertex' } } }))
</script>

<template>
  <div v-if="p" class="mx-auto max-w-7xl px-6 py-10">
    <nav class="flex items-center gap-1 text-sm text-slate-500"><RouterLink to="/products" class="hover:text-slate-900">Products</RouterLink><ChevronRight class="size-4" /><RouterLink :to="`/products?category=${p.category}`" class="capitalize hover:text-slate-900">{{ p.category }}</RouterLink><ChevronRight class="size-4" /><span class="text-slate-900">{{ p.sku }}</span></nav>
    <div class="mt-8 grid gap-12 lg:grid-cols-2">
      <ProductVisual :category="p.category" :sku="p.sku" class="aspect-square" />
      <div>
        <p class="font-mono text-sm font-bold text-brand-600">{{ p.sku }}</p>
        <h1 class="mt-2 text-4xl font-black uppercase">{{ p.name }}</h1>
        <p class="mt-4 text-lg text-slate-600">{{ p.summary }}</p>
        <div class="mt-6 flex flex-wrap gap-2"><span v-for="c in p.certifications" :key="c" class="inline-flex items-center gap-1 bg-slate-100 px-2.5 py-1 text-xs font-bold"><ShieldCheck class="size-3.5 text-emerald-600" />{{ c }}</span></div>
        <table class="mt-8 w-full text-sm">
          <caption class="mb-2 text-left text-xs font-bold tracking-widest text-slate-500 uppercase">Technical specification</caption>
          <tbody><tr v-for="(v, k) in p.specs" :key="k" class="border-b border-slate-100"><th class="w-1/3 py-3 pr-4 text-left font-semibold text-slate-500">{{ k }}</th><td class="py-3 font-semibold">{{ v }}</td></tr></tbody>
        </table>
        <p class="mt-6 text-sm font-semibold text-slate-500">Typical applications</p>
        <div class="mt-2 flex flex-wrap gap-x-5 gap-y-2"><span v-for="a in p.applications" :key="a" class="flex items-center gap-1.5 text-sm"><CheckCircle2 class="size-4 text-brand-600" />{{ a }}</span></div>
        <p class="mt-6 flex items-center gap-2 text-sm text-slate-600"><Clock class="size-4" /> Standard lead time {{ p.lead_time_weeks }} weeks · express builds available</p>
        <div class="mt-8 flex flex-wrap gap-3">
          <RouterLink :to="{ path: '/quote', query: { product: p.id } }" class="btn btn-primary !rounded-none !px-6 !py-3.5">Request a quote <ArrowRight class="size-4" /></RouterLink>
          <button class="btn btn-secondary !rounded-none !px-6 !py-3.5" @click="toast(`Datasheet ${p.sku}.pdf sent to your downloads (demo)`)"><FileDown class="size-4" /> Download datasheet</button>
        </div>
      </div>
    </div>
    <section v-if="p.related.length" class="mt-20">
      <h2 class="text-2xl font-black uppercase">Related products</h2>
      <div class="mt-6 grid gap-6 md:grid-cols-3">
        <RouterLink v-for="r in p.related" :key="r.id" :to="`/products/${r.slug}`" class="flex items-center gap-4 border border-slate-200 p-4 hover:border-brand-500"><ProductVisual :category="r.category" class="size-20 shrink-0" /><div><p class="font-bold">{{ r.name }}</p><p class="line-clamp-2 text-xs text-slate-500">{{ r.summary }}</p></div></RouterLink>
      </div>
    </section>
  </div>
</template>
