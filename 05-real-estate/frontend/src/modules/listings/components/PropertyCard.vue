<script setup>
import { Bath, BedDouble, MapPin, Ruler } from 'lucide-vue-next'
import { humanize } from '@/core/format'
import { img } from '@/core/media'
import { shortPrice } from '../listings.service'

defineProps({ property: Object, active: Boolean })
</script>

<template>
  <RouterLink :to="`/property/${property.slug}`" class="group block overflow-hidden rounded-2xl bg-white ring-1 transition hover:shadow-xl" :class="active ? 'ring-2 ring-brand-500' : 'ring-slate-200'">
    <div class="relative aspect-[4/3] overflow-hidden">
      <img :src="img(property.images[0], 700)" :alt="property.title" loading="lazy" class="size-full object-cover transition duration-500 group-hover:scale-105" />
      <div class="absolute top-3 left-3 flex gap-1.5">
        <span class="rounded-md bg-white/95 px-2 py-1 text-[11px] font-bold tracking-wide uppercase">{{ property.purpose === 'rent' ? 'To rent' : 'For sale' }}</span>
        <span v-if="property.featured" class="rounded-md bg-brand-500 px-2 py-1 text-[11px] font-bold tracking-wide text-white uppercase">Featured</span>
        <span v-if="property.status !== 'available'" class="rounded-md bg-slate-900 px-2 py-1 text-[11px] font-bold tracking-wide text-white uppercase">{{ humanize(property.status) }}</span>
      </div>
      <p class="absolute bottom-3 left-3 rounded-lg bg-slate-950/80 px-3 py-1.5 text-lg font-bold text-white backdrop-blur">{{ shortPrice(property) }}</p>
    </div>
    <div class="p-4">
      <p class="font-semibold text-slate-900 group-hover:text-brand-700">{{ property.title }}</p>
      <p class="mt-1 flex items-center gap-1 text-sm text-slate-500"><MapPin class="size-3.5" />{{ property.address }}</p>
      <div class="mt-3 flex gap-4 border-t border-slate-100 pt-3 text-sm text-slate-600">
        <span class="flex items-center gap-1.5"><BedDouble class="size-4" />{{ property.beds }}</span>
        <span class="flex items-center gap-1.5"><Bath class="size-4" />{{ property.baths }}</span>
        <span class="flex items-center gap-1.5"><Ruler class="size-4" />{{ property.area_sqm }} m²</span>
      </div>
    </div>
  </RouterLink>
</template>
