<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Bath, BedDouble, Calendar, Check, ChevronLeft, ChevronRight, Eye, Leaf, MapPin, Ruler, X } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { money } from '@/core/format'
import { img } from '@/core/media'
import AgentContact from '../components/AgentContact.vue'
import MortgageCalculator from '../components/MortgageCalculator.vue'
import PropertyCard from '../components/PropertyCard.vue'
import PropertyMap from '../components/PropertyMap.vue'
import { listingsService, shortPrice } from '../listings.service'

const route = useRoute()
const { data: p, reload } = useResource(() => listingsService.detail(route.params.slug))
watch(() => route.params.slug, (s) => s && reload())
const lightbox = ref(null)
const step = (n) => { lightbox.value = (lightbox.value + n + p.value.images.length) % p.value.images.length }
</script>

<template>
  <div v-if="p" class="mx-auto max-w-7xl px-6 py-8">
    <div class="grid h-[460px] grid-cols-4 grid-rows-2 gap-2 overflow-hidden rounded-3xl">
      <button v-for="(src, i) in p.images.slice(0, 5)" :key="i" class="relative overflow-hidden" :class="i === 0 ? 'col-span-4 row-span-2 sm:col-span-2' : 'hidden sm:block'" @click="lightbox = i">
        <img :src="img(src, i === 0 ? 1400 : 600)" :alt="p.title" class="size-full object-cover transition duration-500 hover:scale-105" />
        <span v-if="i === 4" class="absolute right-3 bottom-3 rounded-lg bg-white px-3 py-1.5 text-sm font-semibold">View all photos</span>
      </button>
    </div>

    <div class="mt-10 grid gap-12 lg:grid-cols-3">
      <div class="space-y-10 lg:col-span-2">
        <div>
          <p class="text-sm font-semibold tracking-widest text-brand-600 uppercase">{{ p.purpose === 'rent' ? 'To rent' : 'For sale' }} · {{ p.type }}</p>
          <h1 class="mt-2 font-display text-4xl font-semibold">{{ p.title }}</h1>
          <p class="mt-2 flex items-center gap-1.5 text-slate-500"><MapPin class="size-4" />{{ p.address }}</p>
          <p class="mt-5 text-4xl font-bold">{{ shortPrice(p) }}</p>
          <p v-if="p.price_per_sqm" class="text-sm text-slate-500">{{ money(p.price) }} · {{ money(p.price_per_sqm) }}/m²</p>
        </div>
        <div class="grid grid-cols-2 gap-3 sm:grid-cols-5">
          <div v-for="s in [[BedDouble, p.beds, 'Bedrooms'], [Bath, p.baths, 'Bathrooms'], [Ruler, p.area_sqm + ' m²', 'Floor area'], [Calendar, p.year_built, 'Built'], [Leaf, 'EPC ' + p.energy, 'Energy']]" :key="s[2]" class="rounded-2xl bg-slate-50 p-4">
            <component :is="s[0]" class="size-5 text-brand-600" /><p class="mt-2 text-lg font-bold">{{ s[1] }}</p><p class="text-xs text-slate-500">{{ s[2] }}</p>
          </div>
        </div>
        <section><h2 class="font-display text-2xl font-semibold">About this home</h2><p class="mt-3 leading-relaxed text-slate-600">{{ p.description }}</p>
          <p class="mt-3 flex items-center gap-1.5 text-sm text-slate-400"><Eye class="size-4" />{{ p.views.toLocaleString() }} views · listed {{ p.listed_days }} days ago</p></section>
        <section><h2 class="font-display text-2xl font-semibold">Features</h2>
          <div class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3"><p v-for="f in p.features" :key="f" class="flex items-center gap-2 text-slate-700"><Check class="size-4 text-brand-600" />{{ f }}</p></div></section>
        <section><h2 class="font-display text-2xl font-semibold">Location</h2><div class="mt-4 h-80"><PropertyMap :properties="[p]" :zoom="14" /></div></section>
        <MortgageCalculator v-if="p.purpose === 'sale'" :price="p.price" />
      </div>
      <aside><div class="lg:sticky lg:top-24"><AgentContact :key="p.id" :property="p" /></div></aside>
    </div>

    <section v-if="p.similar.length" class="mt-20">
      <h2 class="font-display text-3xl font-semibold">Similar properties</h2>
      <div class="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3"><PropertyCard v-for="s in p.similar" :key="s.id" :property="s" /></div>
    </section>

    <Teleport to="body">
      <div v-if="lightbox !== null" class="fixed inset-0 z-50 grid place-items-center bg-slate-950/95 p-6" @click.self="lightbox = null">
        <button class="absolute top-5 right-5 text-white" @click="lightbox = null"><X class="size-7" /></button>
        <button class="absolute left-5 rounded-full bg-white/10 p-3 text-white" @click="step(-1)"><ChevronLeft class="size-6" /></button>
        <img :src="img(p.images[lightbox], 1800)" :alt="p.title" class="max-h-[85vh] max-w-full rounded-xl" />
        <button class="absolute right-5 rounded-full bg-white/10 p-3 text-white" @click="step(1)"><ChevronRight class="size-6" /></button>
        <p class="absolute bottom-5 text-sm text-white/70">{{ lightbox + 1 }} / {{ p.images.length }}</p>
      </div>
    </Teleport>
  </div>
  <div v-else class="mx-auto max-w-7xl px-6 py-8"><div class="h-[460px] animate-pulse rounded-3xl bg-slate-100" /></div>
</template>
