<script setup>
import { Clock, MapPin, Star } from 'lucide-vue-next'
import { money } from '@/core/format'
import { img } from '@/core/media'
import { CATEGORY_ICON_BY_SLUG } from '../marketplace.service'

defineProps({ business: Object })
</script>

<template>
  <RouterLink :to="`/b/${business.slug}`" class="group block overflow-hidden rounded-3xl bg-white ring-1 ring-slate-200/80 transition hover:-translate-y-1 hover:shadow-xl">
    <div class="relative aspect-[16/10] overflow-hidden">
      <img :src="img(business.image, 700)" :alt="business.name" loading="lazy" class="size-full object-cover transition duration-500 group-hover:scale-105" />
      <span class="absolute top-3 left-3 inline-flex items-center gap-1.5 rounded-full bg-white/90 px-2.5 py-1 text-xs font-bold backdrop-blur">
        <component :is="CATEGORY_ICON_BY_SLUG[business.category]" class="size-3.5 text-brand-600" />{{ business.kind === 'table' ? 'Table booking' : 'Appointments' }}
      </span>
      <span class="absolute top-3 right-3 inline-flex items-center gap-1 rounded-full bg-slate-900/80 px-2.5 py-1 text-xs font-bold text-white"><Star class="size-3.5 fill-amber-400 text-amber-400" />{{ business.rating }}</span>
    </div>
    <div class="p-5">
      <p class="text-lg font-bold text-slate-900">{{ business.name }}</p>
      <p class="mt-1 flex items-center gap-1.5 text-sm text-slate-500"><MapPin class="size-4" />{{ business.area }}</p>
      <div class="mt-4 flex items-center justify-between text-sm">
        <span class="flex items-center gap-1.5 text-slate-500"><Clock class="size-4" />{{ business.open }}–{{ business.close }}</span>
        <span class="font-semibold text-brand-700">{{ business.from_price ? `from ${money(business.from_price)}` : 'Free to book' }}</span>
      </div>
    </div>
  </RouterLink>
</template>
