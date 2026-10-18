<script setup>
import { ref } from 'vue'
import { Bell, LogOut, Menu, Search, Sparkles } from 'lucide-vue-next'
import { navItems } from '@/router'
import { initials } from '@/core/format'
import config from '@/app.config'

const open = ref(false)
const linkFor = (item) => (item.path ? `/app/${item.path}` : '/app')
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <aside
      class="fixed inset-y-0 left-0 z-40 flex w-64 flex-col bg-slate-950 text-slate-400 transition-transform duration-300 lg:translate-x-0"
      :class="open ? 'translate-x-0' : '-translate-x-full'"
    >
      <RouterLink to="/" class="flex h-16 items-center gap-2.5 px-6 text-lg font-extrabold text-white">
        <span class="grid size-9 place-items-center rounded-xl bg-gradient-to-br from-brand-400 to-brand-700 shadow-lg shadow-brand-600/40"><component :is="config.logo" class="size-5" /></span>
        {{ config.name }}
      </RouterLink>
      <nav class="mt-4 flex-1 space-y-1 overflow-y-auto px-3">
        <p class="px-3 pb-2 text-[11px] font-semibold tracking-widest text-slate-600 uppercase">Workspace</p>
        <RouterLink
          v-for="item in navItems" :key="item.path" :to="linkFor(item)" @click="open = false"
          class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition hover:bg-white/5 hover:text-white"
          exact-active-class="!bg-brand-600 !text-white shadow-lg shadow-brand-950/60"
        >
          <component :is="item.meta.nav.icon" class="size-[18px]" />
          {{ item.meta.nav.label }}
        </RouterLink>
      </nav>
      <div v-if="config.promo" class="m-3 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-800 p-4 text-white">
        <Sparkles class="size-5 text-brand-200" />
        <p class="mt-2 text-sm font-bold">{{ config.promo.title }}</p>
        <p class="mt-0.5 text-xs text-brand-100">{{ config.promo.text }}</p>
        <RouterLink :to="config.promo.to" class="mt-3 block rounded-lg bg-white/15 py-1.5 text-center text-xs font-semibold hover:bg-white/25">{{ config.promo.cta }}</RouterLink>
      </div>
    </aside>
    <div v-if="open" class="fixed inset-0 z-30 bg-slate-900/40 backdrop-blur-sm lg:hidden" @click="open = false" />

    <div class="lg:pl-64">
      <header class="sticky top-0 z-20 flex h-16 items-center gap-4 border-b border-slate-200/70 bg-white/80 px-4 backdrop-blur-xl sm:px-8">
        <button class="rounded-lg p-2 text-slate-600 hover:bg-slate-100 lg:hidden" @click="open = true"><Menu class="size-5" /></button>
        <div class="relative hidden max-w-md flex-1 sm:block">
          <Search class="absolute top-1/2 left-3.5 size-4 -translate-y-1/2 text-slate-400" />
          <input class="input !rounded-full !border-transparent !bg-slate-100/80 pl-10" :placeholder="config.searchPlaceholder" />
        </div>
        <div class="ml-auto flex items-center gap-2">
          <button class="relative rounded-full p-2.5 text-slate-500 hover:bg-slate-100">
            <Bell class="size-5" /><span class="absolute top-2 right-2.5 size-2 rounded-full bg-rose-500 ring-2 ring-white" />
          </button>
          <div class="flex items-center gap-3 rounded-full py-1 pr-3 pl-1 hover:bg-slate-100">
            <span class="grid size-8 place-items-center rounded-full bg-gradient-to-br from-brand-500 to-violet-500 text-xs font-bold text-white">{{ initials(config.user.name) }}</span>
            <div class="hidden text-left leading-tight md:block">
              <p class="text-sm font-semibold text-slate-800">{{ config.user.name }}</p>
              <p class="text-xs text-slate-500">{{ config.user.role }}</p>
            </div>
          </div>
          <RouterLink to="/" class="rounded-full p-2.5 text-slate-500 hover:bg-slate-100" title="Back to website"><LogOut class="size-5" /></RouterLink>
        </div>
      </header>
      <main class="mx-auto max-w-7xl p-4 sm:p-8">
        <RouterView v-slot="{ Component }">
          <Transition name="page" mode="out-in"><component :is="Component" /></Transition>
        </RouterView>
      </main>
    </div>
  </div>
</template>
