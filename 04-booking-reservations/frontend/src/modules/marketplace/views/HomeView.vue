<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight, BellRing, CalendarCheck, MousePointerClick, Search, ShieldCheck, Star } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { img } from '@/core/media'
import BusinessCard from '../components/BusinessCard.vue'
import { CATEGORY_ICONS, marketplaceService } from '../marketplace.service'

const router = useRouter()
const q = ref('')
const { data: categories } = useResource(marketplaceService.categories)
const { data: featured } = useResource(() => marketplaceService.list())
const search = () => router.push({ path: '/explore', query: q.value ? { q: q.value } : {} })
const HERO = 'https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?auto=format&fit=crop'
</script>

<template>
  <div>
    <section class="relative overflow-hidden bg-gradient-to-b from-brand-50 to-white">
      <div class="mx-auto grid max-w-7xl items-center gap-12 px-6 py-20 lg:grid-cols-2">
        <div>
          <span class="inline-flex items-center gap-2 rounded-full bg-white px-3 py-1 text-xs font-bold text-brand-700 shadow-sm ring-1 ring-brand-100"><Star class="size-3.5 fill-amber-400 text-amber-400" /> 4.9 · 120k bookings this month</span>
          <h1 class="mt-6 text-5xl leading-[1.05] font-extrabold tracking-tight text-slate-900 sm:text-6xl">Book your next appointment in <span class="text-brand-600">30 seconds.</span></h1>
          <p class="mt-5 max-w-lg text-lg text-slate-600">Dentists, clinics, restaurants, salons, repair shops and trainers — real-time availability, instant confirmation, no phone calls.</p>
          <form class="mt-8 flex max-w-xl gap-2 rounded-2xl bg-white p-2 shadow-xl ring-1 ring-slate-200" @submit.prevent="search">
            <div class="relative flex-1"><Search class="absolute top-1/2 left-3 size-5 -translate-y-1/2 text-slate-400" /><input v-model="q" class="w-full rounded-xl py-3 pr-3 pl-11 outline-none" placeholder="Try “dentist”, “haircut” or “dinner”" /></div>
            <button class="btn btn-primary !px-6">Search</button>
          </form>
          <div class="mt-6 flex flex-wrap gap-2">
            <RouterLink v-for="c in categories" :key="c.slug" :to="`/explore?category=${c.slug}`" class="inline-flex items-center gap-1.5 rounded-full bg-white px-3 py-1.5 text-sm font-semibold text-slate-700 ring-1 ring-slate-200 hover:ring-brand-400">
              <component :is="CATEGORY_ICONS[c.icon]" class="size-4 text-brand-600" />{{ c.name }}
            </RouterLink>
          </div>
        </div>
        <div class="relative hidden lg:block">
          <img :src="img(HERO, 1000)" alt="" class="aspect-[4/5] w-full rounded-[2.5rem] object-cover shadow-2xl" />
          <div class="absolute top-10 -left-10 w-64 rounded-2xl bg-white p-4 shadow-2xl ring-1 ring-slate-100">
            <p class="text-xs font-bold text-brand-600 uppercase">Confirmed</p><p class="mt-1 font-bold">Cut & finish with Chloe</p><p class="text-sm text-slate-500">Tomorrow · 10:30 · Studio Rouge</p>
          </div>
          <div class="absolute -right-6 bottom-12 flex items-center gap-3 rounded-2xl bg-white p-4 shadow-2xl ring-1 ring-slate-100">
            <span class="grid size-10 place-items-center rounded-full bg-amber-100 text-amber-600"><BellRing class="size-5" /></span>
            <div><p class="text-sm font-bold">Reminder sent</p><p class="text-xs text-slate-500">via WhatsApp, 24h before</p></div>
          </div>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-6 py-16">
      <div class="flex items-end justify-between"><h2 class="text-3xl font-extrabold tracking-tight">Popular near you</h2><RouterLink to="/explore" class="inline-flex items-center gap-1 text-sm font-bold text-brand-700">See all <ArrowRight class="size-4" /></RouterLink></div>
      <div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3"><BusinessCard v-for="b in featured?.slice(0, 6)" :key="b.slug" :business="b" /></div>
    </section>

    <section class="bg-slate-950 py-20 text-white">
      <div class="mx-auto max-w-7xl px-6">
        <h2 class="text-center text-3xl font-extrabold">How Bookly works</h2>
        <div class="mt-12 grid gap-8 md:grid-cols-3">
          <div v-for="(s, i) in [[Search, 'Find', 'Search by service, area or business and compare ratings and prices.'], [MousePointerClick, 'Pick a slot', 'See live availability per staff member and choose a time that suits you.'], [CalendarCheck, 'Done', 'Instant confirmation, calendar invite and reminders. Reschedule anytime.']]" :key="i" class="rounded-3xl bg-white/5 p-8 ring-1 ring-white/10">
            <span class="grid size-12 place-items-center rounded-2xl bg-brand-500/20 text-brand-300"><component :is="s[0]" class="size-6" /></span>
            <p class="mt-5 text-sm font-bold text-brand-300">STEP {{ i + 1 }}</p><h3 class="mt-1 text-xl font-bold">{{ s[1] }}</h3><p class="mt-2 text-slate-400">{{ s[2] }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-6 pt-20">
      <div class="grid items-center gap-8 rounded-[2rem] bg-brand-600 p-10 text-white sm:p-14 lg:grid-cols-3">
        <div class="lg:col-span-2">
          <ShieldCheck class="size-10 text-brand-200" />
          <h2 class="mt-4 text-3xl font-extrabold">Run a clinic, salon or restaurant?</h2>
          <p class="mt-2 text-brand-100">Get a booking page, staff calendars, deposits and automated reminders that cut no-shows by up to 60%. Plans from $0/month.</p>
        </div>
        <div class="flex flex-wrap gap-3 lg:justify-end">
          <RouterLink to="/for-business" class="btn bg-white text-brand-700 hover:bg-brand-50">See pricing</RouterLink>
          <RouterLink to="/app" class="btn text-white ring-1 ring-white/40 hover:bg-white/10">Try the dashboard</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>
