<script setup>
import { useRoute } from 'vue-router'
import { BadgeCheck, Clock, MapPin, Star, UserRound } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { money } from '@/core/format'
import { img } from '@/core/media'
import BookingWizard from '../components/BookingWizard.vue'
import { marketplaceService } from '../marketplace.service'

const route = useRoute()
const { data: b } = useResource(() => marketplaceService.business(route.params.slug))
</script>

<template>
  <div v-if="b">
    <div class="relative h-72 sm:h-96">
      <img :src="img(b.image, 1800)" :alt="b.name" class="size-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-950/20 to-transparent" />
      <div class="absolute inset-x-0 bottom-0 mx-auto max-w-7xl px-6 pb-8 text-white">
        <p class="inline-flex items-center gap-1.5 rounded-full bg-white/15 px-3 py-1 text-xs font-bold backdrop-blur"><BadgeCheck class="size-4" /> Verified business</p>
        <h1 class="mt-3 text-4xl font-extrabold sm:text-5xl">{{ b.name }}</h1>
        <p class="mt-2 flex flex-wrap items-center gap-4 text-sm text-white/85">
          <span class="flex items-center gap-1"><Star class="size-4 fill-amber-400 text-amber-400" />{{ b.rating }} ({{ b.reviews }} reviews)</span>
          <span class="flex items-center gap-1"><MapPin class="size-4" />{{ b.area }}</span>
          <span class="flex items-center gap-1"><Clock class="size-4" />Open {{ b.open }}–{{ b.close }}</span>
        </p>
      </div>
    </div>
    <div class="mx-auto grid max-w-7xl gap-10 px-6 py-10 lg:grid-cols-5">
      <div class="space-y-10 lg:col-span-3">
        <section><h2 class="text-xl font-extrabold">About</h2><p class="mt-2 leading-relaxed text-slate-600">{{ b.about }}</p></section>
        <section>
          <h2 class="text-xl font-extrabold">{{ b.kind === 'table' ? 'Experiences' : 'Services & prices' }}</h2>
          <div class="mt-4 divide-y divide-slate-100 rounded-2xl ring-1 ring-slate-200">
            <div v-for="s in b.services" :key="s.id" class="flex items-center justify-between p-4">
              <div><p class="font-semibold">{{ s.name }}</p><p class="text-sm text-slate-500">{{ s.minutes }} min{{ s.deposit ? ` · deposit ${money(s.deposit)}` : '' }}</p></div>
              <p class="font-bold">{{ s.price ? money(s.price) + (s.per_person ? ' pp' : '') : 'Free' }}</p>
            </div>
          </div>
        </section>
        <section>
          <h2 class="text-xl font-extrabold">{{ b.kind === 'table' ? 'Seating' : 'Team' }}</h2>
          <div class="mt-4 grid gap-3 sm:grid-cols-3">
            <div v-for="s in b.staff" :key="s.id" class="rounded-2xl bg-slate-50 p-4 text-center">
              <span class="mx-auto grid size-14 place-items-center rounded-full bg-white text-brand-600 ring-1 ring-slate-200"><UserRound class="size-6" /></span>
              <p class="mt-3 font-semibold">{{ s.name }}</p><p class="text-xs text-slate-500">{{ s.role }}</p>
            </div>
          </div>
        </section>
        <section class="rounded-2xl bg-slate-50 p-5 text-sm text-slate-600"><p class="font-bold text-slate-800">Cancellation policy</p><p class="mt-1">Free cancellation up to 24 hours before. Deposits are refunded in full when you cancel in time.</p></section>
      </div>
      <div class="lg:col-span-2"><div class="lg:sticky lg:top-24"><BookingWizard :business="b" /></div></div>
    </div>
  </div>
  <div v-else class="mx-auto max-w-7xl px-6 py-10"><div class="h-80 animate-pulse rounded-3xl bg-slate-100" /></div>
</template>
