<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight, Award, Home, KeyRound, LineChart, Search } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { img } from '@/core/media'
import PropertyCard from '../components/PropertyCard.vue'
import { listingsService } from '../listings.service'

const router = useRouter()
const purpose = ref('sale')
const district = ref('')
const { data: meta } = useResource(listingsService.meta)
const { data: featured } = useResource(() => listingsService.search({ sort: 'featured' }))
const search = () => router.push({ path: '/properties', query: { purpose: purpose.value, ...(district.value && { district: district.value }) } })
const HERO = 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop'
const SERVICES = [
  { icon: Home, title: 'Sell', text: 'Premium marketing, accompanied viewings and expert negotiation.', to: '/valuation' },
  { icon: KeyRound, title: 'Let & manage', text: 'Tenant finding, rent collection and 24/7 maintenance.', to: '/list-your-property' },
  { icon: LineChart, title: 'Value', text: 'An instant, data-backed estimate of what your home is worth.', to: '/valuation' },
]
</script>

<template>
  <div>
    <section class="relative flex min-h-[92vh] items-end">
      <img :src="img(HERO, 2000)" alt="" class="absolute inset-0 size-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/50 to-slate-950/50" />
      <div class="relative mx-auto w-full max-w-7xl px-6 pb-20 text-white">
        <p class="text-sm font-semibold tracking-[.25em] text-brand-300 uppercase">London's independent agent</p>
        <h1 class="mt-4 max-w-3xl font-display text-5xl leading-tight font-semibold sm:text-7xl">Find a home that fits your life.</h1>
        <form class="mt-10 max-w-3xl rounded-2xl bg-white p-2 text-slate-900 shadow-2xl" @submit.prevent="search">
          <div class="flex flex-wrap gap-2 sm:flex-nowrap">
            <div class="flex rounded-xl bg-slate-100 p-1">
              <button v-for="p in [['sale', 'Buy'], ['rent', 'Rent']]" :key="p[0]" type="button" class="rounded-lg px-5 py-2.5 text-sm font-semibold" :class="purpose === p[0] ? 'bg-white shadow' : 'text-slate-500'" @click="purpose = p[0]">{{ p[1] }}</button>
            </div>
            <select v-model="district" class="min-w-0 flex-1 rounded-xl px-4 text-sm font-medium outline-none">
              <option value="">All London areas</option><option v-for="d in meta?.districts" :key="d">{{ d }}</option>
            </select>
            <button class="btn btn-primary !px-7"><Search class="size-4" /> Search</button>
          </div>
        </form>
        <div class="mt-10 flex flex-wrap gap-10 text-sm">
          <div><p class="font-display text-3xl">£2.1bn</p><p class="text-white/70">property sold since 2009</p></div>
          <div><p class="font-display text-3xl">18 days</p><p class="text-white/70">average time to offer</p></div>
          <div><p class="font-display text-3xl">4.9★</p><p class="text-white/70">from 1,800 reviews</p></div>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-6 py-20">
      <div class="flex items-end justify-between">
        <div><p class="text-sm font-semibold tracking-widest text-brand-600 uppercase">Featured</p><h2 class="mt-2 font-display text-4xl font-semibold">Hand-picked homes</h2></div>
        <RouterLink to="/properties" class="inline-flex items-center gap-1 text-sm font-semibold hover:text-brand-700">All properties <ArrowRight class="size-4" /></RouterLink>
      </div>
      <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3"><PropertyCard v-for="p in featured?.slice(0, 6)" :key="p.id" :property="p" /></div>
    </section>

    <section class="bg-slate-50 py-20">
      <div class="mx-auto grid max-w-7xl gap-6 px-6 md:grid-cols-3">
        <RouterLink v-for="s in SERVICES" :key="s.title" :to="s.to" class="group rounded-3xl bg-white p-8 ring-1 ring-slate-200 transition hover:-translate-y-1 hover:shadow-xl">
          <span class="grid size-12 place-items-center rounded-2xl bg-slate-900 text-brand-400"><component :is="s.icon" class="size-6" /></span>
          <h3 class="mt-6 font-display text-2xl font-semibold">{{ s.title }}</h3><p class="mt-2 text-slate-600">{{ s.text }}</p>
          <span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-brand-700">Learn more <ArrowRight class="size-4 transition group-hover:translate-x-1" /></span>
        </RouterLink>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-6 pt-20">
      <div class="grid items-center gap-10 overflow-hidden rounded-[2rem] bg-slate-900 text-white lg:grid-cols-2">
        <div class="p-10 sm:p-14">
          <Award class="size-10 text-brand-400" />
          <h2 class="mt-4 font-display text-4xl font-semibold">What's your home worth?</h2>
          <p class="mt-3 text-slate-300">Get an instant estimate based on recent sales in your area — then book a free in-person valuation.</p>
          <RouterLink to="/valuation" class="btn btn-primary mt-8">Get my free valuation</RouterLink>
        </div>
        <img :src="img('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop', 1000)" alt="" class="h-full min-h-72 w-full object-cover" />
      </div>
    </section>
  </div>
</template>
