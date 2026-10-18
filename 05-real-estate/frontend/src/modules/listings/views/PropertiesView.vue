<script setup>
import { reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LayoutGrid, Map as MapIcon } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import PropertyCard from '../components/PropertyCard.vue'
import PropertyMap from '../components/PropertyMap.vue'
import { listingsService } from '../listings.service'

const route = useRoute()
const router = useRouter()
const f = reactive({ purpose: route.query.purpose ?? '', district: route.query.district ?? '', type: '', min_beds: 0, max_price: '', sort: 'featured' })
const { data: meta } = useResource(listingsService.meta)
const { data, loading, reload } = useResource(() => listingsService.search(f))
const showMap = ref(true)
const active = ref(null)
watch(() => route.query, (q) => { f.purpose = q.purpose ?? ''; f.district = q.district ?? '' })
watch(f, () => { router.replace({ query: { ...(f.purpose && { purpose: f.purpose }), ...(f.district && { district: f.district }) } }); reload() })
const PRICES = { sale: [[750000, '£750k'], [1500000, '£1.5m'], [3000000, '£3m']], rent: [[2500, '£2,500 pcm'], [4000, '£4,000 pcm']] }
</script>

<template>
  <div class="mx-auto max-w-[1600px] px-6 py-8">
    <div class="flex flex-wrap items-center gap-2">
      <div class="flex rounded-xl bg-slate-100 p-1">
        <button v-for="p in [['', 'All'], ['sale', 'Buy'], ['rent', 'Rent']]" :key="p[0]" class="rounded-lg px-4 py-2 text-sm font-semibold" :class="f.purpose === p[0] ? 'bg-white shadow' : 'text-slate-500'" @click="f.purpose = p[0]; f.max_price = ''">{{ p[1] }}</button>
      </div>
      <select v-model="f.district" class="input !w-auto"><option value="">Any area</option><option v-for="d in meta?.districts" :key="d">{{ d }}</option></select>
      <select v-model="f.type" class="input !w-auto capitalize"><option value="">Any type</option><option v-for="t in meta?.types" :key="t" :value="t">{{ t }}</option></select>
      <select v-model.number="f.min_beds" class="input !w-auto"><option :value="0">Any beds</option><option v-for="n in [1, 2, 3, 4, 5]" :key="n" :value="n">{{ n }}+ beds</option></select>
      <select v-if="f.purpose" v-model="f.max_price" class="input !w-auto"><option value="">No max</option><option v-for="[v, l] in PRICES[f.purpose]" :key="v" :value="v">Up to {{ l }}</option></select>
      <select v-model="f.sort" class="input !w-auto"><option value="featured">Featured</option><option value="newest">Newest</option><option value="price_asc">Lowest price</option><option value="price_desc">Highest price</option></select>
      <button class="btn btn-secondary ml-auto hidden lg:inline-flex" @click="showMap = !showMap"><component :is="showMap ? LayoutGrid : MapIcon" class="size-4" />{{ showMap ? 'Grid only' : 'Show map' }}</button>
    </div>
    <p class="mt-4 text-sm text-slate-500"><strong class="text-slate-900">{{ data?.length ?? '…' }}</strong> properties</p>

    <div class="mt-4 grid gap-6" :class="showMap ? 'lg:grid-cols-[1fr_minmax(0,0.9fr)]' : ''">
      <div class="grid content-start gap-6 sm:grid-cols-2" :class="[{ 'opacity-60': loading }, showMap ? 'xl:grid-cols-2' : 'lg:grid-cols-3 xl:grid-cols-4']">
        <div v-for="p in data" :key="p.id" @mouseenter="active = p.id"><PropertyCard :property="p" :active="active === p.id" /></div>
        <p v-if="data && !data.length" class="col-span-full py-20 text-center text-slate-500">No properties match — try widening your search.</p>
      </div>
      <div v-if="showMap" class="hidden lg:block"><div class="sticky top-24 h-[calc(100vh-8rem)]"><PropertyMap :properties="data ?? []" :active-id="active" @select="active = $event" /></div></div>
    </div>
  </div>
</template>
