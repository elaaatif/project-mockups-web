<script setup>
import { ref } from 'vue'
import { ArrowUpRight, Code2, Menu, X } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { portfolioService } from '@/modules/portfolio/portfolio.service'

const { data: me } = useResource(portfolioService.profile)
const mobile = ref(false)
const links = [['/#work', 'Work'], ['/#services', 'Services'], ['/#pricing', 'Pricing'], ['/#process', 'Process'], ['/#contact', 'Contact']]
</script>

<template>
  <div class="min-h-screen bg-[#0a0a0a] text-zinc-300 selection:bg-brand-400 selection:text-black">
    <header class="sticky top-0 z-40 border-b border-white/5 bg-[#0a0a0a]/75 backdrop-blur-xl">
      <div class="mx-auto flex h-16 max-w-7xl items-center gap-8 px-6">
        <RouterLink to="/" class="flex items-center gap-2.5 font-semibold text-white">
          <span class="grid size-9 place-items-center rounded-xl bg-brand-400 text-black"><Code2 class="size-5" /></span>{{ me?.name ?? '…' }}
        </RouterLink>
        <nav class="hidden gap-7 text-sm md:flex"><RouterLink v-for="[to, l] in links" :key="to" :to="to" class="hover:text-white">{{ l }}</RouterLink></nav>
        <RouterLink to="/#contact" class="ml-auto hidden items-center gap-2 rounded-full bg-white px-4 py-2 text-sm font-semibold text-black transition hover:bg-brand-300 sm:inline-flex">
          <span v-if="me?.available" class="size-2 animate-pulse rounded-full bg-emerald-500" />Start a project <ArrowUpRight class="size-4" />
        </RouterLink>
        <button class="ml-auto text-white md:hidden" @click="mobile = !mobile"><component :is="mobile ? X : Menu" class="size-6" /></button>
      </div>
      <nav v-if="mobile" class="border-t border-white/5 px-6 py-3 md:hidden"><RouterLink v-for="[to, l] in links" :key="to" :to="to" class="block py-2 text-white" @click="mobile = false">{{ l }}</RouterLink></nav>
    </header>
    <RouterView v-slot="{ Component }"><Transition name="page" mode="out-in"><component :is="Component" /></Transition></RouterView>
    <footer class="border-t border-white/5">
      <div class="mx-auto flex max-w-7xl flex-wrap items-center gap-6 px-6 py-10 text-sm text-zinc-500">
        <p>© 2026 {{ me?.name }} · Built with Vue 3 + FastAPI (modular MVC)</p>
        <div class="ml-auto flex gap-5"><a v-for="(url, k) in me?.links" :key="k" :href="url" target="_blank" rel="noopener" class="capitalize hover:text-white">{{ k }}</a><RouterLink to="/app" class="hover:text-white">Inbox</RouterLink></div>
      </div>
    </footer>
  </div>
</template>
