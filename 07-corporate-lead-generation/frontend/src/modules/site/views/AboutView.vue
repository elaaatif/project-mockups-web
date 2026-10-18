<script setup>
import { useResource } from '@/core/resource'
import { img } from '@/core/media'
import { siteService } from '../site.service'

const { data: co } = useResource(siteService.company)
const TIMELINE = [
  ['1987', 'Founded in Birmingham as a precision machine shop.'], ['1998', 'First Vertex-designed centrifugal pump range launched.'],
  ['2009', 'Automation & controls division established.'], ['2018', 'Opened Coventry manufacturing campus (12,000 m²).'],
  ['2024', 'Net-zero manufacturing roadmap; IE4 motors standard.'], ['2026', 'IIoT predictive-maintenance platform rolled out to 400 sites.'],
]
const LEADERS = [
  ['Helen Ward', 'Chief Executive', '1573496359142-b8d87734a5a2'], ['Marcus Webb', 'Engineering Director', '1507679799987-c73779587ccf'],
  ['Priya Raman', 'Operations Director', '1494790108377-be9c29b29330'], ['Thomas Keller', 'Service Director', '1500648767791-00dcc994a43e'],
]
</script>

<template>
  <div>
    <section class="bg-slate-950 py-24 text-white">
      <div class="mx-auto max-w-7xl px-6">
        <p class="text-sm font-bold tracking-[.2em] text-brand-400 uppercase">About Vertex</p>
        <h1 class="mt-4 max-w-3xl text-5xl font-black tracking-tight uppercase">Engineers first. Since 1987.</h1>
        <p class="mt-6 max-w-2xl text-lg text-slate-300">We're an independent, employee-owned manufacturer. Every product we sell is designed, built and supported by our own people.</p>
        <div class="mt-12 grid grid-cols-2 gap-6 md:grid-cols-4"><div v-for="s in co?.stats" :key="s.label"><p class="text-4xl font-black text-brand-400">{{ s.value }}</p><p class="text-sm text-slate-400">{{ s.label }}</p></div></div>
      </div>
    </section>
    <section class="mx-auto grid max-w-7xl gap-12 px-6 py-24 lg:grid-cols-2">
      <img :src="img('https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop', 1000)" alt="Vertex engineer in the test lab" class="aspect-[4/3] w-full object-cover" />
      <div>
        <h2 class="text-3xl font-black uppercase">Our story</h2>
        <ol class="mt-8 space-y-6 border-l-2 border-slate-200 pl-6">
          <li v-for="[y, t] in TIMELINE" :key="y" class="relative"><span class="absolute top-1 -left-[31px] size-3 bg-brand-500" /><p class="font-black text-brand-600">{{ y }}</p><p class="text-slate-600">{{ t }}</p></li>
        </ol>
      </div>
    </section>
    <section class="bg-slate-50 py-24">
      <div class="mx-auto max-w-7xl px-6">
        <h2 class="text-3xl font-black uppercase">Leadership</h2>
        <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="[n, r, p] in LEADERS" :key="n" class="bg-white"><img :src="img(`https://images.unsplash.com/photo-${p}?auto=format&fit=crop`, 500)" :alt="n" class="aspect-square w-full object-cover grayscale" /><div class="p-5"><p class="font-bold">{{ n }}</p><p class="text-sm text-slate-500">{{ r }}</p></div></div>
        </div>
      </div>
    </section>
  </div>
</template>
