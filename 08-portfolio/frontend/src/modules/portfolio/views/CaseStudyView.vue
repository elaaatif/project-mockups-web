<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, ArrowRight, BookOpen, Check, ExternalLink, FolderTree, Lightbulb, Target, Wallet } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { portfolioService } from '../portfolio.service'

const route = useRoute()
const { data: p, reload } = useResource(() => portfolioService.project(route.params.slug))
watch(() => route.params.slug, (s) => s && reload())
const live = ref(false)
onMounted(async () => { const s = await portfolioService.status().catch(() => ({})); live.value = !!s[route.params.slug] })
watch(p, (v) => { if (v) document.title = `${v.brand} — ${v.title} · Case study` })
</script>

<template>
  <div v-if="p">
    <section class="mx-auto max-w-7xl px-6 pt-14">
      <RouterLink to="/#work" class="inline-flex items-center gap-1.5 text-sm text-zinc-400 hover:text-white"><ArrowLeft class="size-4" /> All work</RouterLink>
      <div class="mt-8 flex flex-wrap items-end justify-between gap-6">
        <div class="max-w-3xl">
          <p class="inline-flex rounded-full bg-gradient-to-r px-3 py-1 text-xs font-semibold text-white" :class="p.color">{{ p.category }}</p>
          <h1 class="mt-5 text-5xl font-semibold tracking-tight text-white sm:text-6xl">{{ p.brand }}</h1>
          <p class="mt-3 text-xl text-zinc-400">{{ p.title }}</p>
        </div>
        <div class="flex flex-wrap gap-3">
          <a :href="p.web_url" target="_blank" rel="noopener" class="inline-flex items-center gap-2 rounded-full px-5 py-3 text-sm font-semibold" :class="live ? 'bg-brand-400 text-black hover:bg-brand-300' : 'border border-white/15 text-zinc-400'">
            <span class="size-2 rounded-full" :class="live ? 'bg-emerald-600' : 'bg-zinc-500'" />{{ live ? 'Open live demo' : 'Demo offline' }} <ExternalLink class="size-4" />
          </a>
          <a :href="p.api_url" target="_blank" rel="noopener" class="inline-flex items-center gap-2 rounded-full border border-white/15 px-5 py-3 text-sm font-semibold text-white hover:bg-white/5"><BookOpen class="size-4" /> API docs</a>
        </div>
      </div>
      <p v-if="!live" class="mt-4 text-sm text-zinc-500">Start it with <code class="rounded bg-white/10 px-1.5 py-0.5 text-zinc-300">.\start.ps1 {{ p.n }}</code> from the repository root.</p>
      <div class="mt-10 overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-2 shadow-2xl shadow-brand-500/5">
        <img :src="p.cover" :alt="p.title" class="w-full rounded-2xl" />
      </div>
    </section>

    <section class="mx-auto grid max-w-7xl gap-6 px-6 py-16 md:grid-cols-3">
      <div class="rounded-3xl border border-white/10 p-7"><Target class="size-6 text-rose-400" /><p class="mt-4 font-semibold text-white">The problem</p><p class="mt-2 text-zinc-400">{{ p.problem }}</p></div>
      <div class="rounded-3xl border border-white/10 p-7"><Lightbulb class="size-6 text-brand-400" /><p class="mt-4 font-semibold text-white">The solution</p><p class="mt-2 text-zinc-400">{{ p.summary }}</p></div>
      <div class="rounded-3xl border border-white/10 p-7"><Wallet class="size-6 text-amber-400" /><p class="mt-4 font-semibold text-white">How it makes money</p><p class="mt-2 text-zinc-400">{{ p.revenue }}</p></div>
    </section>

    <section class="mx-auto grid max-w-7xl gap-10 px-6 pb-16 lg:grid-cols-2">
      <div>
        <h2 class="text-2xl font-semibold text-white">What's implemented</h2>
        <ul class="mt-6 space-y-3"><li v-for="f in p.features" :key="f" class="flex gap-3"><Check class="mt-0.5 size-5 shrink-0 text-brand-400" />{{ f }}</li></ul>
        <div class="mt-8 flex flex-wrap gap-2"><span v-for="s in p.stack" :key="s" class="rounded-full border border-white/10 px-3 py-1 text-xs">{{ s }}</span></div>
      </div>
      <div>
        <h2 class="flex items-center gap-2 text-2xl font-semibold text-white"><FolderTree class="size-6 text-brand-400" /> Modular MVC structure</h2>
        <pre class="mt-6 overflow-x-auto rounded-2xl border border-white/10 bg-black/40 p-5 font-mono text-[13px] leading-relaxed text-zinc-400"><span class="text-white">{{ p.folder }}/</span>
├─ backend/
│  ├─ main.py               <span class="text-zinc-600"># app factory, registers modules</span>
│  └─ app/modules/
<template v-for="(m, i) in p.modules" :key="m">│     {{ i === p.modules.length - 1 ? '└' : '├' }}─ <span class="text-brand-300">{{ m }}/</span>  models · service · controller
</template>└─ frontend/src/
   ├─ core/ · components/ui/ · layouts/
   └─ modules/<span class="text-zinc-600">&lt;feature&gt;</span>/  views · *.service.js · routes.js</pre>
      </div>
    </section>

    <section v-if="p.gallery.length" class="mx-auto max-w-7xl px-6 pb-16">
      <h2 class="text-2xl font-semibold text-white">More screens</h2>
      <div class="mt-6 grid gap-6 md:grid-cols-2"><img v-for="g in p.gallery" :key="g" :src="g" :alt="`${p.brand} screen`" loading="lazy" class="rounded-2xl border border-white/10" /></div>
    </section>

    <section class="mx-auto max-w-7xl px-6 pb-24">
      <RouterLink :to="`/work/${p.next.slug}`" class="group flex items-center justify-between rounded-3xl border border-white/10 p-8 transition hover:border-brand-400">
        <div><p class="text-sm text-zinc-500">Next case study</p><p class="mt-1 text-2xl font-semibold text-white group-hover:text-brand-300">{{ p.next.title }}</p></div>
        <ArrowRight class="size-8 transition group-hover:translate-x-2" />
      </RouterLink>
    </section>
  </div>
  <div v-else class="mx-auto max-w-7xl px-6 py-20"><div class="h-96 animate-pulse rounded-3xl bg-white/5" /></div>
</template>
