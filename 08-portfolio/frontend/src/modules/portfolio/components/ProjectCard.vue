<script setup>
import { ArrowUpRight, ExternalLink } from 'lucide-vue-next'

defineProps({ project: Object, live: Boolean, large: Boolean })
</script>

<template>
  <article class="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/[.03] transition hover:border-white/20">
    <RouterLink :to="`/work/${project.slug}`" class="block">
      <div class="relative overflow-hidden" :class="large ? 'aspect-[16/9]' : 'aspect-[16/10]'">
        <img :src="project.cover" :alt="`${project.brand} — ${project.title}`" loading="lazy" class="size-full object-cover object-top transition duration-700 group-hover:scale-[1.03]" />
        <div class="absolute inset-0 bg-gradient-to-t from-[#0a0a0a] via-transparent to-transparent" />
        <span class="absolute top-4 left-4 rounded-full bg-gradient-to-r px-3 py-1 text-xs font-semibold text-white shadow-lg" :class="project.color">{{ project.category }}</span>
        <span class="absolute top-4 right-4 flex items-center gap-1.5 rounded-full bg-black/60 px-2.5 py-1 text-[11px] font-medium backdrop-blur" :class="live ? 'text-emerald-300' : 'text-zinc-400'">
          <span class="size-1.5 rounded-full" :class="live ? 'animate-pulse bg-emerald-400' : 'bg-zinc-500'" />{{ live ? 'Running locally' : 'Offline' }}
        </span>
      </div>
    </RouterLink>
    <div class="p-6">
      <div class="flex items-start justify-between gap-4">
        <div>
          <p class="font-mono text-xs text-zinc-500">{{ String(project.n).padStart(2, '0') }} / {{ project.brand }}</p>
          <RouterLink :to="`/work/${project.slug}`" class="mt-1 block text-xl font-semibold text-white group-hover:text-brand-300">{{ project.title }}</RouterLink>
        </div>
        <RouterLink :to="`/work/${project.slug}`" class="grid size-10 shrink-0 place-items-center rounded-full border border-white/10 transition group-hover:rotate-45 group-hover:bg-brand-400 group-hover:text-black"><ArrowUpRight class="size-5" /></RouterLink>
      </div>
      <p class="mt-3 text-sm leading-relaxed text-zinc-400">{{ project.summary }}</p>
      <p class="mt-4 text-xs text-zinc-500"><span class="text-zinc-300">Revenue model:</span> {{ project.revenue }}</p>
      <div class="mt-4 flex flex-wrap items-center gap-1.5">
        <span v-for="s in project.stack" :key="s" class="rounded-full border border-white/10 px-2.5 py-0.5 text-[11px]">{{ s }}</span>
        <a v-if="live" :href="project.web_url" target="_blank" rel="noopener" class="ml-auto inline-flex items-center gap-1 text-xs font-semibold text-brand-300 hover:text-brand-200">Live demo <ExternalLink class="size-3.5" /></a>
      </div>
    </div>
  </article>
</template>
