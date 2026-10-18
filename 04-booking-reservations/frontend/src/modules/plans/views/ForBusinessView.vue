<script setup>
import { BellRing, CalendarRange, Check, CreditCard, Globe, LineChart, Users } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { http } from '@/core/http'

const { data: plans } = useResource(() => http.get('/plans'))
const features = [
  { icon: Globe, title: 'Your booking page', text: 'A branded page with live availability you can link from Google, Instagram and your website.' },
  { icon: CalendarRange, title: 'Staff calendars', text: 'Per-person schedules, service durations and buffers — no double bookings, ever.' },
  { icon: BellRing, title: 'Smart reminders', text: 'Email, SMS and WhatsApp reminders that cut no-shows by up to 60%.' },
  { icon: CreditCard, title: 'Deposits', text: 'Take deposits for high-value services and refund automatically on time cancellations.' },
  { icon: Users, title: 'Tables & party sizes', text: 'Restaurants map seating areas and capacities; we find the right table.' },
  { icon: LineChart, title: 'Reports', text: 'Occupancy, revenue and no-show rate per staff member and service.' },
]
</script>

<template>
  <div>
    <section class="bg-slate-950 py-20 text-center text-white">
      <p class="text-sm font-bold tracking-widest text-brand-300 uppercase">For clinics, restaurants, salons, repair shops & trainers</p>
      <h1 class="mx-auto mt-4 max-w-3xl text-5xl font-extrabold tracking-tight">Fill your calendar while you sleep.</h1>
      <p class="mx-auto mt-4 max-w-xl text-slate-400">Subscription or pay-per-booking — choose what fits your business.</p>
    </section>
    <section class="mx-auto -mt-10 grid max-w-6xl gap-6 px-6 lg:grid-cols-3">
      <div v-for="p in plans" :key="p.name" class="relative rounded-3xl bg-white p-8 shadow-xl ring-1" :class="p.popular ? 'ring-2 ring-brand-500' : 'ring-slate-200'">
        <span v-if="p.popular" class="absolute -top-3 left-8 rounded-full bg-brand-600 px-3 py-1 text-xs font-bold text-white">Most popular</span>
        <h3 class="text-lg font-bold">{{ p.name }}</h3>
        <p class="mt-4"><span class="text-5xl font-extrabold">{{ p.price }}</span><span class="text-slate-500">{{ p.period }}</span></p>
        <p class="mt-1 text-sm font-semibold text-brand-700">{{ p.fee }}</p>
        <ul class="mt-6 space-y-3 text-sm"><li v-for="f in p.features" :key="f" class="flex gap-2"><Check class="size-5 shrink-0 text-brand-600" />{{ f }}</li></ul>
        <RouterLink to="/app" class="btn mt-8 w-full" :class="p.popular ? 'btn-primary' : 'btn-secondary'">Start free trial</RouterLink>
      </div>
    </section>
    <section class="mx-auto mt-24 max-w-6xl px-6">
      <h2 class="text-center text-3xl font-extrabold">Everything you need to take bookings</h2>
      <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div v-for="f in features" :key="f.title" class="rounded-3xl bg-slate-50 p-7">
          <span class="grid size-11 place-items-center rounded-xl bg-brand-100 text-brand-700"><component :is="f.icon" class="size-5" /></span>
          <h3 class="mt-4 font-bold">{{ f.title }}</h3><p class="mt-1 text-sm text-slate-600">{{ f.text }}</p>
        </div>
      </div>
    </section>
  </div>
</template>
