<script setup>
import { ref } from 'vue'
import { Menu, X } from 'lucide-vue-next'
import config from '@/app.config'

const mobile = ref(false)
const links = [['/explore', 'Explore'], ['/explore?category=clinics', 'Clinics'], ['/explore?category=restaurants', 'Restaurants'], ['/explore?category=salons', 'Salons'], ['/my-bookings', 'My bookings']]
</script>

<template>
  <div class="min-h-screen bg-white">
    <header class="sticky top-0 z-30 border-b border-slate-100 bg-white/85 backdrop-blur-xl">
      <div class="mx-auto flex h-16 max-w-7xl items-center gap-8 px-6">
        <RouterLink to="/" class="flex items-center gap-2 text-xl font-extrabold">
          <span class="grid size-9 place-items-center rounded-xl bg-brand-600 text-white"><component :is="config.logo" class="size-5" /></span>{{ config.name }}
        </RouterLink>
        <nav class="hidden gap-6 text-sm font-semibold text-slate-600 lg:flex">
          <RouterLink v-for="[to, label] in links" :key="to" :to="to" class="hover:text-brand-700">{{ label }}</RouterLink>
        </nav>
        <div class="ml-auto flex items-center gap-2">
          <RouterLink to="/for-business" class="btn btn-ghost hidden sm:inline-flex">For businesses</RouterLink>
          <RouterLink to="/app" class="btn btn-primary">Business login</RouterLink>
          <button class="p-2 lg:hidden" @click="mobile = !mobile"><component :is="mobile ? X : Menu" class="size-6" /></button>
        </div>
      </div>
      <nav v-if="mobile" class="space-y-1 border-t border-slate-100 px-6 py-3 lg:hidden">
        <RouterLink v-for="[to, label] in links" :key="to" :to="to" class="block rounded-lg px-2 py-2 font-semibold hover:bg-slate-50" @click="mobile = false">{{ label }}</RouterLink>
      </nav>
    </header>
    <RouterView v-slot="{ Component }"><Transition name="page" mode="out-in"><component :is="Component" /></Transition></RouterView>
    <footer class="mt-24 border-t border-slate-100 bg-slate-50">
      <div class="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-6 py-10 text-sm text-slate-500">
        <p>© 2026 {{ config.name }} · Built with Vue 3 + FastAPI</p>
        <div class="flex gap-6"><RouterLink to="/for-business">Pricing</RouterLink><RouterLink to="/my-bookings">Manage a booking</RouterLink><RouterLink to="/app">Business dashboard</RouterLink></div>
      </div>
    </footer>
  </div>
</template>
