<script setup>
import { onMounted } from 'vue'
import { ArrowRight, ArrowUpRight, Award, Factory, Globe2, Headphones, ShieldCheck } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { img } from '@/core/media'
import { setSeo } from '@/core/seo'
import config from '@/app.config'
import ProductVisual from '@/modules/products/components/ProductVisual.vue'
import { productsService } from '@/modules/products/products.service'
import { SERVICE_ICONS, siteService } from '../site.service'

const { data: co } = useResource(siteService.company)
const { data: cats } = useResource(productsService.categories)
onMounted(() => setSeo({ jsonLd: { '@type': 'Organization', name: config.name, url: location.origin, foundingDate: '1987', address: { '@type': 'PostalAddress', addressLocality: 'Birmingham', addressCountry: 'GB' } } }))
</script>

<template>
  <div v-if="co">
    <section class="relative overflow-hidden bg-slate-950 text-white">
      <img :src="img(co.hero_image, 2000)" alt="Vertex Industrial process plant" class="absolute inset-0 size-full object-cover opacity-35" />
      <div class="absolute inset-0 bg-gradient-to-r from-slate-950 via-slate-950/80 to-transparent" />
      <div class="relative mx-auto max-w-7xl px-6 py-28 lg:py-36">
        <p class="flex items-center gap-2 text-sm font-bold tracking-[.2em] text-brand-400 uppercase"><span class="h-px w-10 bg-brand-500" /> Engineered in Britain since 1987</p>
        <h1 class="mt-6 max-w-3xl text-5xl leading-[1.02] font-black tracking-tight uppercase sm:text-7xl">Flow, power &amp; automation that never stops.</h1>
        <p class="mt-6 max-w-xl text-lg text-slate-300">Pumps, valves, drives and control systems — designed, built and maintained by one accountable partner.</p>
        <div class="mt-10 flex flex-wrap gap-3">
          <RouterLink to="/quote" class="btn btn-primary !rounded-none !px-7 !py-4 !text-base">Get a quote in 2 minutes <ArrowRight class="size-5" /></RouterLink>
          <RouterLink to="/products" class="btn !rounded-none !px-7 !py-4 !text-base text-white ring-1 ring-white/30 hover:bg-white/10">Browse product catalogue</RouterLink>
        </div>
      </div>
      <div class="relative border-t border-white/10 bg-slate-950/60 backdrop-blur">
        <div class="mx-auto grid max-w-7xl grid-cols-2 divide-white/10 px-6 md:grid-cols-4 md:divide-x">
          <div v-for="s in co.stats" :key="s.label" class="py-6 md:px-6 md:first:pl-0"><p class="text-3xl font-black text-brand-400">{{ s.value }}</p><p class="text-sm text-slate-400">{{ s.label }}</p></div>
        </div>
      </div>
    </section>

    <section id="services" class="mx-auto max-w-7xl scroll-mt-24 px-6 py-24">
      <p class="text-sm font-bold tracking-[.2em] text-brand-600 uppercase">What we do</p>
      <h2 class="mt-3 max-w-2xl text-4xl font-black tracking-tight uppercase">From drawing board to 24/7 service</h2>
      <div class="mt-12 grid gap-px bg-slate-200 md:grid-cols-2 lg:grid-cols-4">
        <RouterLink v-for="s in co.services" :key="s.slug" :to="`/services/${s.slug}`" class="group bg-white p-8 transition hover:bg-slate-950 hover:text-white">
          <component :is="SERVICE_ICONS[s.icon]" class="size-9 text-brand-600" />
          <h3 class="mt-6 text-xl font-bold">{{ s.title }}</h3>
          <p class="mt-3 text-sm text-slate-500 group-hover:text-slate-400">{{ s.summary }}</p>
          <ArrowUpRight class="mt-6 size-5 text-slate-300 transition group-hover:text-brand-500" />
        </RouterLink>
      </div>
    </section>

    <section class="bg-slate-50 py-24">
      <div class="mx-auto max-w-7xl px-6">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <div><p class="text-sm font-bold tracking-[.2em] text-brand-600 uppercase">Product catalogue</p><h2 class="mt-3 text-4xl font-black tracking-tight uppercase">Specified by engineers</h2></div>
          <RouterLink to="/products" class="inline-flex items-center gap-1 font-semibold text-brand-700">All products <ArrowRight class="size-4" /></RouterLink>
        </div>
        <div class="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <RouterLink v-for="c in cats" :key="c.slug" :to="`/products?category=${c.slug}`" class="group bg-white ring-1 ring-slate-200 transition hover:-translate-y-1 hover:shadow-xl">
            <ProductVisual :category="c.slug" class="aspect-square" />
            <div class="p-4"><p class="font-bold">{{ c.name }}</p><p class="text-sm text-slate-500">{{ c.count }} product ranges</p></div>
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-6 py-24">
      <p class="text-sm font-bold tracking-[.2em] text-brand-600 uppercase">Case studies</p>
      <h2 class="mt-3 text-4xl font-black tracking-tight uppercase">Measurable results</h2>
      <div class="mt-10 grid gap-6 md:grid-cols-3">
        <article v-for="c in co.case_studies" :key="c.client" class="border-t-4 border-brand-500 bg-slate-950 p-8 text-white">
          <p class="text-xs font-bold tracking-widest text-slate-400 uppercase">{{ c.industry }}</p>
          <p class="mt-4 text-4xl font-black text-brand-400">{{ c.result }}</p>
          <h3 class="mt-4 text-lg font-bold">{{ c.client }}</h3><p class="mt-2 text-sm text-slate-400">{{ c.summary }}</p>
        </article>
      </div>
      <div class="mt-16 flex flex-wrap items-center justify-center gap-x-10 gap-y-4 text-sm font-bold tracking-widest text-slate-400 uppercase">
        <span v-for="i in co.industries" :key="i">{{ i }}</span>
      </div>
    </section>

    <section class="bg-brand-600 text-white">
      <div class="mx-auto grid max-w-7xl gap-8 px-6 py-16 md:grid-cols-4">
        <div v-for="f in [[ShieldCheck, 'ISO certified', '9001 · 14001 · 45001'], [Headphones, '24/7 service', '4-hour call-out in the UK'], [Globe2, 'Global supply', '62 countries, 9 distributors'], [Award, '5-year warranty', 'on Vertex-built equipment']]" :key="f[1]" class="flex items-start gap-4">
          <component :is="f[0]" class="size-8 shrink-0" /><div><p class="font-bold">{{ f[1] }}</p><p class="text-sm text-brand-100">{{ f[2] }}</p></div>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-6 py-24">
      <div class="grid items-center gap-10 bg-slate-950 p-10 text-white md:grid-cols-3 md:p-14">
        <div class="md:col-span-2"><Factory class="size-10 text-brand-500" /><h2 class="mt-4 text-3xl font-black uppercase">Have a project or a spec sheet?</h2><p class="mt-2 text-slate-400">Send us your requirements — our engineers reply with a costed proposal, usually the same day.</p></div>
        <div class="flex flex-wrap gap-3 md:justify-end"><RouterLink to="/quote" class="btn btn-primary !rounded-none !px-6 !py-3.5">Request a quote</RouterLink><RouterLink to="/contact" class="btn !rounded-none !px-6 !py-3.5 ring-1 ring-white/30">Talk to sales</RouterLink></div>
      </div>
    </section>
  </div>
  <div v-else class="h-[80vh] animate-pulse bg-slate-900" />
</template>
