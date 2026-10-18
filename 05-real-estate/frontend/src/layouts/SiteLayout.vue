<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { Menu, Phone, X } from 'lucide-vue-next'
import config from '@/app.config'

const route = useRoute()
const scrolled = ref(false)
const mobile = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 40 }
onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
const transparent = computed(() => route.path === '/' && !scrolled.value && !mobile.value)
const links = [['/properties?purpose=sale', 'Buy'], ['/properties?purpose=rent', 'Rent'], ['/valuation', 'Free valuation'], ['/list-your-property', 'List a property']]
</script>

<template>
  <div class="min-h-screen bg-white">
    <header class="fixed inset-x-0 top-0 z-40 transition" :class="transparent ? 'text-white' : 'bg-white/90 text-slate-900 shadow-sm backdrop-blur-xl'">
      <div class="mx-auto flex h-18 max-w-7xl items-center gap-10 px-6 py-4">
        <RouterLink to="/" class="flex items-center gap-2 font-display text-2xl font-semibold"><component :is="config.logo" class="size-6 text-brand-500" />{{ config.name }}</RouterLink>
        <nav class="hidden gap-8 text-sm font-medium md:flex">
          <RouterLink v-for="[to, label] in links" :key="to" :to="to" class="opacity-90 hover:opacity-100 hover:text-brand-500">{{ label }}</RouterLink>
        </nav>
        <div class="ml-auto flex items-center gap-3">
          <a href="tel:+442079460100" class="hidden items-center gap-2 text-sm font-semibold lg:flex"><Phone class="size-4" /> 020 7946 0100</a>
          <RouterLink to="/app" class="btn btn-primary">Agent login</RouterLink>
          <button class="md:hidden" @click="mobile = !mobile"><component :is="mobile ? X : Menu" class="size-6" /></button>
        </div>
      </div>
      <nav v-if="mobile" class="space-y-1 border-t border-slate-100 bg-white px-6 py-3 md:hidden">
        <RouterLink v-for="[to, label] in links" :key="to" :to="to" class="block py-2 font-medium" @click="mobile = false">{{ label }}</RouterLink>
      </nav>
    </header>
    <div :class="route.path === '/' ? '' : 'pt-18'">
      <RouterView v-slot="{ Component }"><Transition name="page" mode="out-in"><component :is="Component" /></Transition></RouterView>
    </div>
    <footer class="mt-24 bg-slate-950 py-14 text-slate-400">
      <div class="mx-auto grid max-w-7xl gap-8 px-6 md:grid-cols-4">
        <div><p class="font-display text-2xl text-white">{{ config.name }}</p><p class="mt-2 text-sm">Independent London estate agents since 2009. Sales, lettings and property management.</p></div>
        <div class="text-sm"><p class="font-semibold text-white">Property</p><p class="mt-3"><RouterLink to="/properties?purpose=sale">For sale</RouterLink></p><p class="mt-2"><RouterLink to="/properties?purpose=rent">To rent</RouterLink></p></div>
        <div class="text-sm"><p class="font-semibold text-white">Services</p><p class="mt-3"><RouterLink to="/valuation">Instant valuation</RouterLink></p><p class="mt-2"><RouterLink to="/list-your-property">List with us</RouterLink></p><p class="mt-2"><RouterLink to="/app/rentals">Landlord portal</RouterLink></p></div>
        <div class="text-sm"><p class="font-semibold text-white">Contact</p><p class="mt-3">hello@haven.estate</p><p class="mt-2">48 Marylebone High St, London</p></div>
      </div>
      <p class="mt-10 text-center text-xs">© 2026 Haven Estates Ltd · Built with Vue 3 + FastAPI</p>
    </footer>
  </div>
</template>
