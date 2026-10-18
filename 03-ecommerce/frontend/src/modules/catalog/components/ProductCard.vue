<script setup>
import { Plus, Star } from 'lucide-vue-next'
import { money } from '@/core/format'
import { img } from '@/core/media'
import { cart } from '@/modules/cart/cart.store'

defineProps({ product: Object })
</script>

<template>
  <div class="group">
    <RouterLink :to="`/product/${product.slug}`" class="relative block aspect-[4/5] overflow-hidden rounded-2xl bg-slate-100">
      <img :src="img(product.image, 600)" :alt="product.name" loading="lazy" class="size-full object-cover transition duration-500 group-hover:scale-105" />
      <span v-if="product.badge" class="absolute top-3 left-3 rounded-full bg-white/90 px-2.5 py-1 text-xs font-semibold backdrop-blur">{{ product.badge }}</span>
      <span v-if="!product.stock" class="absolute inset-x-3 bottom-3 rounded-xl bg-slate-900/80 py-2 text-center text-xs font-semibold text-white">Sold out</span>
      <button v-else class="absolute right-3 bottom-3 grid size-11 translate-y-2 place-items-center rounded-full bg-white text-slate-900 opacity-0 shadow-lg transition group-hover:translate-y-0 group-hover:opacity-100 hover:bg-brand-600 hover:text-white"
              :title="`Add ${product.name} to bag`" @click.prevent="cart.add(product)">
        <Plus class="size-5" />
      </button>
    </RouterLink>
    <div class="mt-3 flex items-start justify-between gap-2">
      <div>
        <RouterLink :to="`/product/${product.slug}`" class="font-semibold text-slate-900 hover:text-brand-700">{{ product.name }}</RouterLink>
        <p class="mt-0.5 flex items-center gap-1 text-xs text-slate-500"><Star class="size-3.5 fill-amber-400 text-amber-400" />{{ product.rating }} ({{ product.reviews }})</p>
      </div>
      <div class="text-right">
        <p class="font-semibold">{{ money(product.price) }}</p>
        <p v-if="product.compare_at" class="text-xs text-slate-400 line-through">{{ money(product.compare_at) }}</p>
      </div>
    </div>
  </div>
</template>
