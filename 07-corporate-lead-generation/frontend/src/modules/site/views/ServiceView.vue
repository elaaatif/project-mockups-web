<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowRight, CheckCircle2 } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { img } from '@/core/media'
import { setSeo } from '@/core/seo'
import { siteService } from '../site.service'

const route = useRoute()
const { data: s, reload } = useResource(() => siteService.service(route.params.slug))
watch(() => route.params.slug, (v) => v && reload())
watch(s, (v) => v && setSeo({ title: v.title, description: v.summary, jsonLd: { '@type': 'Service', name: v.title, description: v.summary, provider: { '@type': 'Organization', name: 'Vertex Industrial' } } }))
</script>

<template>
  <div v-if="s">
    <section class="relative bg-slate-950 text-white">
      <img :src="img(s.image, 1800)" :alt="s.title" class="absolute inset-0 size-full object-cover opacity-30" />
      <div class="relative mx-auto max-w-7xl px-6 py-28"><p class="text-sm font-bold tracking-[.2em] text-brand-400 uppercase">Services</p><h1 class="mt-4 text-5xl font-black uppercase">{{ s.title }}</h1><p class="mt-4 max-w-2xl text-lg text-slate-300">{{ s.summary }}</p></div>
    </section>
    <section class="mx-auto grid max-w-7xl gap-12 px-6 py-20 lg:grid-cols-3">
      <div class="lg:col-span-2">
        <h2 class="text-2xl font-black uppercase">Capabilities</h2>
        <div class="mt-6 grid gap-4 sm:grid-cols-2"><p v-for="p in s.points" :key="p" class="flex items-center gap-3 bg-slate-50 p-5 font-semibold"><CheckCircle2 class="size-5 text-brand-600" />{{ p }}</p></div>
        <p class="mt-8 leading-relaxed text-slate-600">Our {{ s.title.toLowerCase() }} team works to your specification and schedule, with a single project manager from kick-off to handover. All work is delivered under our ISO 9001 quality system with full documentation and traceability.</p>
      </div>
      <aside class="bg-slate-950 p-8 text-white"><h3 class="text-xl font-black uppercase">Start a project</h3><p class="mt-2 text-sm text-slate-400">Tell us about your requirement and we'll respond with a costed proposal.</p><RouterLink to="/quote" class="btn btn-primary mt-6 w-full !rounded-none">Request a quote <ArrowRight class="size-4" /></RouterLink></aside>
    </section>
  </div>
</template>
