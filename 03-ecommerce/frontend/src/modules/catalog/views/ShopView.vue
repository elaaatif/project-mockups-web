<script setup>
import { reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { SlidersHorizontal } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { money } from '@/core/format'
import ProductCard from '../components/ProductCard.vue'
import { catalogService } from '../catalog.service'

const route = useRoute()
const router = useRouter()
const filters = reactive({ q: route.query.q ?? '', category: route.query.category ?? '', sort: 'featured', max_price: 1500, in_stock: false })
const { data: categories } = useResource(catalogService.categories)
const { data: products, loading, reload } = useResource(() => catalogService.products(filters))

// Keep filters in sync with the URL (header search / category links)
watch(() => route.query, (q) => { filters.q = q.q ?? ''; filters.category = q.category ?? '' })
let t
watch(filters, () => {
  clearTimeout(t)
  t = setTimeout(() => {
    router.replace({ query: { ...(filters.q && { q: filters.q }), ...(filters.category && { category: filters.category }) } })
    reload()
  }, 200)
})
</script>

<template>
  <div class="mx-auto max-w-7xl px-6 py-12">
    <h1 class="font-display text-4xl font-semibold">{{ categories?.find((c) => c.slug === filters.category)?.name ?? 'All products' }}</h1>
    <p class="mt-1 text-slate-500">{{ products?.length ?? '…' }} products{{ filters.q ? ` matching “${filters.q}”` : '' }}</p>

    <div class="mt-8 grid gap-10 lg:grid-cols-4">
      <aside class="space-y-8 lg:sticky lg:top-24 lg:self-start">
        <div class="flex items-center gap-2 font-semibold"><SlidersHorizontal class="size-4" /> Filters</div>
        <div><label class="label">Search</label><input v-model="filters.q" class="input" placeholder="Name or keyword" /></div>
        <div>
          <p class="label">Category</p>
          <div class="space-y-1">
            <button class="block w-full rounded-lg px-3 py-2 text-left text-sm" :class="!filters.category ? 'bg-brand-50 font-semibold text-brand-800' : 'hover:bg-slate-100'" @click="filters.category = ''">All</button>
            <button v-for="c in categories" :key="c.slug" class="block w-full rounded-lg px-3 py-2 text-left text-sm" :class="filters.category === c.slug ? 'bg-brand-50 font-semibold text-brand-800' : 'hover:bg-slate-100'" @click="filters.category = c.slug">{{ c.name }}</button>
          </div>
        </div>
        <div><p class="label">Max price · {{ money(filters.max_price) }}</p><input v-model.number="filters.max_price" type="range" min="40" max="1500" step="10" class="w-full accent-brand-600" /></div>
        <label class="flex items-center gap-2 text-sm"><input v-model="filters.in_stock" type="checkbox" class="size-4 accent-brand-600" /> In stock only</label>
      </aside>

      <div class="lg:col-span-3">
        <div class="mb-6 flex justify-end">
          <select v-model="filters.sort" class="input !w-auto"><option value="featured">Featured</option><option value="price_asc">Price: low to high</option><option value="price_desc">Price: high to low</option><option value="rating">Top rated</option></select>
        </div>
        <div class="grid grid-cols-2 gap-x-5 gap-y-10 md:grid-cols-3" :class="{ 'opacity-60': loading }">
          <ProductCard v-for="p in products" :key="p.id" :product="p" />
        </div>
        <p v-if="products && !products.length" class="py-20 text-center text-slate-500">Nothing matches those filters.</p>
      </div>
    </div>
  </div>
</template>
