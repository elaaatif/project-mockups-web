<script setup>
import { ref } from 'vue'
import { ArrowRight, Mail, MapPin, Menu, Phone, X } from 'lucide-vue-next'
import config from '@/app.config'

const mobile = ref(false)
const links = [['/products', 'Products'], ['/#services', 'Services'], ['/about', 'About'], ['/careers', 'Careers'], ['/contact', 'Contact']]
</script>

<template>
  <div class="min-h-screen bg-white">
    <div class="hidden bg-slate-950 text-xs text-slate-400 md:block">
      <div class="mx-auto flex max-w-7xl gap-6 px-6 py-2"><span class="flex items-center gap-1.5"><Phone class="size-3.5" /> +44 121 496 0000</span><span class="flex items-center gap-1.5"><Mail class="size-3.5" /> sales@vertex-industrial.example</span><span class="ml-auto">24/7 service hotline · ISO 9001 · ISO 14001 · ISO 45001</span></div>
    </div>
    <header class="sticky top-0 z-30 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div class="mx-auto flex h-18 max-w-7xl items-center gap-10 px-6">
        <RouterLink to="/" class="flex items-center gap-2.5 text-xl font-black tracking-tight uppercase">
          <span class="grid size-10 place-items-center bg-slate-950 text-brand-500"><component :is="config.logo" class="size-5" /></span>Vertex<span class="font-medium text-slate-400">Industrial</span>
        </RouterLink>
        <nav class="hidden gap-8 text-sm font-semibold text-slate-700 lg:flex">
          <RouterLink v-for="[to, label] in links" :key="to" :to="to" class="hover:text-brand-600">{{ label }}</RouterLink>
        </nav>
        <RouterLink to="/quote" class="btn btn-primary ml-auto !rounded-none">Request a quote <ArrowRight class="size-4" /></RouterLink>
        <button class="lg:hidden" @click="mobile = !mobile"><component :is="mobile ? X : Menu" class="size-6" /></button>
      </div>
      <nav v-if="mobile" class="border-t border-slate-100 px-6 py-3 lg:hidden"><RouterLink v-for="[to, label] in links" :key="to" :to="to" class="block py-2 font-semibold" @click="mobile = false">{{ label }}</RouterLink></nav>
    </header>
    <RouterView v-slot="{ Component }"><Transition name="page" mode="out-in"><component :is="Component" /></Transition></RouterView>
    <footer class="bg-slate-950 text-slate-400">
      <div class="mx-auto grid max-w-7xl gap-10 px-6 py-16 md:grid-cols-4">
        <div class="md:col-span-2">
          <p class="text-xl font-black tracking-tight text-white uppercase">Vertex <span class="font-medium text-slate-500">Industrial</span></p>
          <p class="mt-3 max-w-sm text-sm">Designing, manufacturing and maintaining industrial flow and automation equipment since 1987.</p>
          <p class="mt-4 flex items-center gap-2 text-sm"><MapPin class="size-4 text-brand-500" /> Unit 7, Aston Science Park, Birmingham B7 4BJ</p>
        </div>
        <div class="text-sm"><p class="font-semibold text-white">Company</p><p class="mt-3"><RouterLink to="/about">About us</RouterLink></p><p class="mt-2"><RouterLink to="/careers">Careers</RouterLink></p><p class="mt-2"><RouterLink to="/contact">Contact</RouterLink></p><p class="mt-2"><a href="/api/seo/sitemap.xml">Sitemap</a></p></div>
        <div class="text-sm"><p class="font-semibold text-white">Products</p><p class="mt-3"><RouterLink to="/products?category=pumps">Pumps</RouterLink></p><p class="mt-2"><RouterLink to="/products?category=valves">Valves</RouterLink></p><p class="mt-2"><RouterLink to="/products?category=automation">Automation</RouterLink></p><p class="mt-2"><RouterLink to="/app">Staff login</RouterLink></p></div>
      </div>
      <p class="border-t border-white/5 py-6 text-center text-xs">© 2026 Vertex Industrial Ltd · Registered in England No. 0214XXXX · Built with Vue 3 + FastAPI</p>
    </footer>
  </div>
</template>
