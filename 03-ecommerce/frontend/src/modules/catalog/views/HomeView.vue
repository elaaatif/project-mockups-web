<script setup>
import { ArrowRight, Building2, PackageSearch, RefreshCcw, ShieldCheck, Truck } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { img } from '@/core/media'
import ProductCard from '../components/ProductCard.vue'
import { catalogService } from '../catalog.service'

const { data: featured } = useResource(() => catalogService.products({ sort: 'featured' }))
const { data: categories } = useResource(catalogService.categories)

const HERO = 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop'
const CATEGORY_IMAGES = {
  'audio-tech': '1505740420928-5e560c06d30e', watches: '1523275335684-37898b6baf30', footwear: '1542291026-7eec264c27ff',
  accessories: '1572635196237-14b3f281503f', home: '1555041469-a586c61ea9bc', beauty: '1585386959984-a4155224a1ad',
}
const catImg = (slug) => img(`https://images.unsplash.com/photo-${CATEGORY_IMAGES[slug]}?auto=format&fit=crop`, 500)
const perks = [
  { icon: Truck, title: 'Free shipping', text: 'On orders over $75' },
  { icon: RefreshCcw, title: '30-day returns', text: 'No questions asked' },
  { icon: ShieldCheck, title: '2-year warranty', text: 'On every product' },
  { icon: PackageSearch, title: 'Live tracking', text: 'From warehouse to door' },
]
</script>

<template>
  <div>
    <!-- Hero -->
    <section class="mx-auto max-w-7xl px-6 pt-8">
      <div class="relative overflow-hidden rounded-[2rem] bg-slate-900">
        <img :src="img(HERO, 1800)" alt="" class="absolute inset-0 size-full object-cover opacity-80" />
        <div class="absolute inset-0 bg-gradient-to-r from-slate-950/80 via-slate-950/40 to-transparent" />
        <div class="relative max-w-xl px-8 py-24 text-white sm:px-14 sm:py-32">
          <p class="text-sm font-semibold tracking-widest text-brand-300 uppercase">Autumn collection 2026</p>
          <h1 class="mt-4 font-display text-5xl leading-tight font-semibold sm:text-6xl">Pieces that make a house feel like home.</h1>
          <p class="mt-5 text-lg text-white/80">Considered design for living, working and moving — now with up to 35% off in our wholesale portal.</p>
          <div class="mt-8 flex flex-wrap gap-3">
            <RouterLink to="/shop" class="btn bg-white !px-6 !py-3.5 text-slate-900 hover:bg-brand-50">Shop the collection <ArrowRight class="size-4" /></RouterLink>
            <RouterLink to="/wholesale" class="btn !px-6 !py-3.5 text-white ring-1 ring-white/40 hover:bg-white/10">Buy wholesale</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <section class="mx-auto mt-10 grid max-w-7xl grid-cols-2 gap-4 px-6 md:grid-cols-4">
      <div v-for="p in perks" :key="p.title" class="flex items-center gap-3 rounded-2xl bg-white p-4 ring-1 ring-slate-200/70">
        <span class="grid size-10 place-items-center rounded-xl bg-brand-50 text-brand-700"><component :is="p.icon" class="size-5" /></span>
        <div><p class="text-sm font-semibold">{{ p.title }}</p><p class="text-xs text-slate-500">{{ p.text }}</p></div>
      </div>
    </section>

    <!-- Categories -->
    <section class="mx-auto mt-20 max-w-7xl px-6">
      <h2 class="font-display text-3xl font-semibold">Shop by category</h2>
      <div class="mt-8 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
        <RouterLink v-for="c in categories" :key="c.slug" :to="`/shop?category=${c.slug}`" class="group relative aspect-square overflow-hidden rounded-2xl">
          <img :src="catImg(c.slug)" :alt="c.name" class="size-full object-cover transition duration-500 group-hover:scale-110" />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/70 to-transparent" />
          <p class="absolute bottom-3 left-4 font-semibold text-white">{{ c.name }}</p>
        </RouterLink>
      </div>
    </section>

    <!-- Featured -->
    <section class="mx-auto mt-20 max-w-7xl px-6">
      <div class="flex items-end justify-between">
        <h2 class="font-display text-3xl font-semibold">Bestsellers & new in</h2>
        <RouterLink to="/shop" class="inline-flex items-center gap-1 text-sm font-semibold text-brand-700">View all <ArrowRight class="size-4" /></RouterLink>
      </div>
      <div class="mt-8 grid grid-cols-2 gap-x-5 gap-y-10 lg:grid-cols-4">
        <ProductCard v-for="p in featured?.slice(0, 8)" :key="p.id" :product="p" />
        <template v-if="!featured"><div v-for="i in 8" :key="i" class="aspect-[4/5] animate-pulse rounded-2xl bg-slate-200/70" /></template>
      </div>
    </section>

    <!-- B2B banner -->
    <section class="mx-auto mt-24 max-w-7xl px-6">
      <div class="grid items-center gap-10 rounded-[2rem] bg-brand-900 p-10 text-white sm:p-14 lg:grid-cols-2">
        <div>
          <Building2 class="size-10 text-brand-300" />
          <h2 class="mt-4 font-display text-4xl font-semibold">Buying for a business?</h2>
          <p class="mt-3 text-brand-100">Open the wholesale portal for tiered pricing (15–35% off), Net 30 terms and pallet delivery — or send us a product list for a tailored quotation.</p>
          <div class="mt-8 flex flex-wrap gap-3">
            <RouterLink to="/wholesale" class="btn bg-white text-brand-900 hover:bg-brand-50">Wholesale portal</RouterLink>
            <RouterLink to="/quote" class="btn text-white ring-1 ring-white/30 hover:bg-white/10">Request a quote</RouterLink>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-3 text-center">
          <div v-for="t in [['10+', '15% off'], ['50+', '25% off'], ['200+', '35% off']]" :key="t[0]" class="rounded-2xl bg-white/10 p-6">
            <p class="font-display text-3xl font-semibold">{{ t[0] }}</p><p class="mt-1 text-sm text-brand-200">units · {{ t[1] }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
