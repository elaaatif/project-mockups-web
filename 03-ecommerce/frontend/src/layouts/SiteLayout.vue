<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { FileText, Menu, Search, ShoppingBag, Truck, X } from 'lucide-vue-next'
import CartDrawer from '@/modules/cart/components/CartDrawer.vue'
import { cart } from '@/modules/cart/cart.store'
import { quoteList } from '@/modules/quotes/quote.store'
import config from '@/app.config'

const router = useRouter()
const q = ref('')
const mobile = ref(false)
const search = () => { router.push({ path: '/shop', query: q.value ? { q: q.value } : {} }); mobile.value = false }
const links = [['/shop', 'Shop all'], ['/shop?category=home', 'Home'], ['/shop?category=audio-tech', 'Tech'], ['/wholesale', 'Wholesale'], ['/track', 'Track order']]
</script>

<template>
  <div class="min-h-screen bg-[#faf9f6]">
    <div class="bg-slate-950 py-2 text-center text-xs font-medium text-white"><Truck class="mr-1.5 inline size-3.5" />Free shipping over $75 · 30-day returns · Wholesale pricing from 10 units</div>
    <header class="sticky top-0 z-30 border-b border-slate-200/70 bg-[#faf9f6]/90 backdrop-blur-xl">
      <div class="mx-auto flex h-16 max-w-7xl items-center gap-6 px-6">
        <button class="lg:hidden" @click="mobile = !mobile"><component :is="mobile ? X : Menu" class="size-6" /></button>
        <RouterLink to="/" class="font-display text-2xl font-semibold tracking-tight">{{ config.name.toLowerCase() }}<span class="text-brand-600">.</span></RouterLink>
        <nav class="hidden gap-6 text-sm font-medium text-slate-600 lg:flex">
          <RouterLink v-for="[to, label] in links" :key="to" :to="to" class="hover:text-slate-950">{{ label }}</RouterLink>
        </nav>
        <form class="relative ml-auto hidden max-w-xs flex-1 md:block" @submit.prevent="search">
          <Search class="absolute top-1/2 left-3.5 size-4 -translate-y-1/2 text-slate-400" />
          <input v-model="q" class="input !rounded-full !bg-white pl-10" placeholder="Search products" />
        </form>
        <RouterLink to="/quote" class="relative rounded-full p-2.5 hover:bg-slate-100 max-md:ml-auto" title="Quote request">
          <FileText class="size-5" />
          <span v-if="quoteList.items.length" class="absolute -top-0.5 -right-0.5 grid size-5 place-items-center rounded-full bg-amber-500 text-[10px] font-bold text-white">{{ quoteList.items.length }}</span>
        </RouterLink>
        <button class="relative rounded-full p-2.5 hover:bg-slate-100" @click="cart.state.open = true">
          <ShoppingBag class="size-5" />
          <span v-if="cart.count.value" class="absolute -top-0.5 -right-0.5 grid size-5 place-items-center rounded-full bg-brand-600 text-[10px] font-bold text-white">{{ cart.count.value }}</span>
        </button>
      </div>
      <div v-if="mobile" class="space-y-1 border-t border-slate-100 px-6 py-4 lg:hidden">
        <form @submit.prevent="search"><input v-model="q" class="input" placeholder="Search products" /></form>
        <RouterLink v-for="[to, label] in links" :key="to" :to="to" class="block rounded-lg px-2 py-2 font-medium hover:bg-slate-100" @click="mobile = false">{{ label }}</RouterLink>
      </div>
    </header>

    <RouterView v-slot="{ Component }"><Transition name="page" mode="out-in"><component :is="Component" /></Transition></RouterView>

    <footer class="mt-24 bg-slate-950 text-slate-400">
      <div class="mx-auto grid max-w-7xl gap-10 px-6 py-16 md:grid-cols-4">
        <div><p class="font-display text-2xl font-semibold text-white">{{ config.name.toLowerCase() }}<span class="text-brand-400">.</span></p><p class="mt-3 text-sm">Design-led goods for home, style and tech — for shoppers and businesses alike.</p></div>
        <div><p class="font-semibold text-white">Shop</p><ul class="mt-3 space-y-2 text-sm"><li><RouterLink to="/shop">All products</RouterLink></li><li><RouterLink to="/shop?category=home">Home & living</RouterLink></li><li><RouterLink to="/shop?category=watches">Watches</RouterLink></li></ul></div>
        <div><p class="font-semibold text-white">Business</p><ul class="mt-3 space-y-2 text-sm"><li><RouterLink to="/wholesale">Wholesale portal</RouterLink></li><li><RouterLink to="/quote">Request a quote</RouterLink></li><li><RouterLink to="/app">Store admin</RouterLink></li></ul></div>
        <div><p class="font-semibold text-white">Help</p><ul class="mt-3 space-y-2 text-sm"><li><RouterLink to="/track">Track an order</RouterLink></li><li>Returns & refunds</li><li>hello@mercato.shop</li></ul></div>
      </div>
      <p class="border-t border-white/5 py-6 text-center text-xs">© 2026 Mercato · Built with Vue 3 + FastAPI</p>
    </footer>
    <CartDrawer />
  </div>
</template>
