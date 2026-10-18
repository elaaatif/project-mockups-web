<script setup>
import { ref } from 'vue'
import { Menu, X } from 'lucide-vue-next'
import config from '@/app.config'

const mobile = ref(false)
const links = [['/courses', 'Courses'], ['/my-learning', 'My learning'], ['/pricing', 'For teams & schools'], ['/verify', 'Verify certificate']]
</script>

<template>
  <div class="min-h-screen bg-white">
    <header class="sticky top-0 z-30 border-b border-slate-100 bg-white/90 backdrop-blur-xl">
      <div class="mx-auto flex h-16 max-w-7xl items-center gap-8 px-6">
        <RouterLink to="/" class="flex items-center gap-2 text-xl font-bold"><span class="grid size-9 place-items-center rounded-xl bg-brand-600 text-white"><component :is="config.logo" class="size-5" /></span>{{ config.name }}</RouterLink>
        <nav class="hidden gap-7 text-sm font-medium text-slate-600 md:flex">
          <RouterLink v-for="[to, label] in links" :key="to" :to="to" class="hover:text-brand-700" active-class="text-brand-700">{{ label }}</RouterLink>
        </nav>
        <div class="ml-auto flex items-center gap-2">
          <RouterLink to="/app" class="btn btn-ghost hidden sm:inline-flex">Admin</RouterLink>
          <RouterLink to="/courses" class="btn btn-primary">Start learning</RouterLink>
          <button class="md:hidden" @click="mobile = !mobile"><component :is="mobile ? X : Menu" class="size-6" /></button>
        </div>
      </div>
      <nav v-if="mobile" class="border-t border-slate-100 px-6 py-3 md:hidden"><RouterLink v-for="[to, label] in links" :key="to" :to="to" class="block py-2 font-medium" @click="mobile = false">{{ label }}</RouterLink></nav>
    </header>
    <RouterView v-slot="{ Component }"><Transition name="page" mode="out-in"><component :is="Component" /></Transition></RouterView>
    <footer class="mt-24 border-t border-slate-100 bg-slate-50 py-10 text-center text-sm text-slate-500">© 2026 Brightpath Academy · Built with Vue 3 + FastAPI</footer>
  </div>
</template>
