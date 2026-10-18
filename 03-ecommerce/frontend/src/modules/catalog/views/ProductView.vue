<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Check, ChevronRight, FileText, Minus, Plus, ShieldCheck, Star, Truck } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { money } from '@/core/format'
import { img } from '@/core/media'
import { toast } from '@/core/toast'
import { cart } from '@/modules/cart/cart.store'
import { quoteList } from '@/modules/quotes/quote.store'
import ProductCard from '../components/ProductCard.vue'
import { catalogService } from '../catalog.service'

const route = useRoute()
const { data: p, reload } = useResource(() => catalogService.product(route.params.slug))
watch(() => route.params.slug, (s) => s && reload())
const qty = ref(1)
function addToQuote() { quoteList.add(p.value, 25); toast(`${p.value.name} added to your quote request`) }
</script>

<template>
  <div v-if="p" class="mx-auto max-w-7xl px-6 py-10">
    <nav class="flex items-center gap-1 text-sm text-slate-500"><RouterLink to="/shop" class="hover:text-slate-900">Shop</RouterLink><ChevronRight class="size-4" /><RouterLink :to="`/shop?category=${p.category}`" class="hover:text-slate-900 capitalize">{{ p.category.replace('-', ' & ') }}</RouterLink><ChevronRight class="size-4" /><span class="text-slate-800">{{ p.name }}</span></nav>

    <div class="mt-8 grid gap-12 lg:grid-cols-2">
      <div class="overflow-hidden rounded-3xl bg-slate-100"><img :src="img(p.image, 1200)" :alt="p.name" class="aspect-square w-full object-cover" /></div>
      <div>
        <p v-if="p.badge" class="text-sm font-semibold tracking-widest text-brand-700 uppercase">{{ p.badge }}</p>
        <h1 class="mt-2 font-display text-4xl font-semibold">{{ p.name }}</h1>
        <p class="mt-3 flex items-center gap-2 text-sm"><span class="flex">
          <Star v-for="i in 5" :key="i" class="size-4" :class="i <= Math.round(p.rating) ? 'fill-amber-400 text-amber-400' : 'text-slate-300'" /></span>{{ p.rating }} · {{ p.reviews }} reviews</p>
        <p class="mt-6 flex items-baseline gap-3"><span class="text-3xl font-bold">{{ money(p.price) }}</span><span v-if="p.compare_at" class="text-lg text-slate-400 line-through">{{ money(p.compare_at) }}</span></p>
        <p class="mt-6 leading-relaxed text-slate-600">{{ p.description }}</p>

        <p class="mt-6 text-sm font-semibold" :class="p.stock > 15 ? 'text-brand-700' : p.stock ? 'text-amber-600' : 'text-rose-600'">
          {{ p.stock > 15 ? '● In stock, ships in 24h' : p.stock ? `● Only ${p.stock} left` : '● Sold out — available via quote' }}
        </p>
        <div class="mt-4 flex gap-3">
          <div class="flex items-center rounded-xl ring-1 ring-slate-200">
            <button class="p-3" @click="qty = Math.max(1, qty - 1)"><Minus class="size-4" /></button><span class="w-8 text-center font-semibold">{{ qty }}</span><button class="p-3" @click="qty = Math.min(p.stock || 1, qty + 1)"><Plus class="size-4" /></button>
          </div>
          <button class="btn btn-primary flex-1 !py-3.5" :disabled="!p.stock" @click="cart.add(p, qty)">Add to bag · {{ money(p.price * qty) }}</button>
        </div>
        <button class="btn btn-secondary mt-3 w-full" @click="addToQuote"><FileText class="size-4" /> Add to quote request (bulk / business)</button>

        <div class="mt-8 rounded-2xl bg-white p-5 ring-1 ring-slate-200">
          <p class="text-sm font-semibold">Wholesale price breaks</p>
          <div class="mt-3 grid grid-cols-3 gap-2 text-center">
            <div v-for="t in p.tiers" :key="t.min_qty" class="rounded-xl bg-brand-50 p-3"><p class="text-xs text-brand-700">{{ t.min_qty }}+ units</p><p class="mt-1 font-bold">{{ money(t.unit_price, 2) }}</p><p class="text-[11px] text-slate-500">-{{ t.discount * 100 }}%</p></div>
          </div>
          <RouterLink to="/wholesale" class="mt-3 inline-block text-sm font-semibold text-brand-700">Order in the wholesale portal →</RouterLink>
        </div>
        <ul class="mt-6 space-y-2 text-sm text-slate-600">
          <li class="flex gap-2"><Truck class="size-4 text-brand-600" />Free standard shipping over $75</li>
          <li class="flex gap-2"><ShieldCheck class="size-4 text-brand-600" />2-year warranty · SKU {{ p.sku }}</li>
          <li class="flex gap-2"><Check class="size-4 text-brand-600" />30-day free returns</li>
        </ul>
      </div>
    </div>

    <section v-if="p.related.length" class="mt-24">
      <h2 class="font-display text-2xl font-semibold">You may also like</h2>
      <div class="mt-6 grid grid-cols-2 gap-5 md:grid-cols-4"><ProductCard v-for="r in p.related" :key="r.id" :product="r" /></div>
    </section>
  </div>
  <div v-else class="mx-auto grid max-w-7xl gap-12 px-6 py-10 lg:grid-cols-2"><div class="aspect-square animate-pulse rounded-3xl bg-slate-200/70" /><div class="h-96 animate-pulse rounded-3xl bg-slate-200/70" /></div>
</template>
