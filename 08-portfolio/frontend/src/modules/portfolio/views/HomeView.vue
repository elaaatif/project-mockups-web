<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { ArrowDown, ArrowUpRight, Check, Layers, MapPin, MessagesSquare, Quote, Rocket, Search, Server, Wrench } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { money } from '@/core/format'
import EstimateContact from '../components/EstimateContact.vue'
import ProjectCard from '../components/ProjectCard.vue'
import { portfolioService } from '../portfolio.service'

const { data: me } = useResource(portfolioService.profile)
const { data: projects } = useResource(portfolioService.projects)
const status = ref({})
const filter = ref('All')
const categories = computed(() => ['All', ...new Set((projects.value ?? []).map((p) => p.category))])
const shown = computed(() => (projects.value ?? []).filter((p) => filter.value === 'All' || p.category === filter.value))
const liveCount = computed(() => Object.values(status.value).filter(Boolean).length)

let timer
async function poll() { status.value = await portfolioService.status().catch(() => ({})) }
onMounted(() => { poll(); timer = setInterval(poll, 15000) })
onUnmounted(() => clearInterval(timer))

const PROCESS = [
  { icon: MessagesSquare, title: 'Discovery call', text: 'We map the workflow, users and the money: what the software must earn or save.' },
  { icon: Layers, title: 'Clickable design', text: 'A branded prototype like the demos above — agreed before a line of production code.' },
  { icon: Server, title: 'Build in modules', text: 'Weekly demos. Each feature is its own MVC module, so scope can grow safely.' },
  { icon: Rocket, title: 'Launch & care', text: 'Deployment, monitoring, backups and a retainer for improvements and SEO.' },
]
</script>

<template>
  <div>
    <!-- Hero -->
    <section class="grain relative overflow-hidden">
      <div class="pointer-events-none absolute -top-40 left-1/2 size-[46rem] -translate-x-1/2 rounded-full bg-brand-500/15 blur-[140px]" />
      <div class="relative mx-auto max-w-7xl px-6 pt-24 pb-16">
        <p v-if="me" class="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs">
          <span class="size-2 rounded-full" :class="me.available ? 'animate-pulse bg-emerald-400' : 'bg-zinc-500'" />{{ me.available ? 'Available for new projects' : 'Fully booked' }} · <MapPin class="size-3" />{{ me.location }}
        </p>
        <h1 class="mt-8 max-w-5xl text-5xl leading-[1.02] font-semibold tracking-tight text-white sm:text-7xl lg:text-8xl">
          {{ me?.headline ?? 'I build business software that pays for itself.' }}
        </h1>
        <div class="mt-10 grid items-end gap-10 lg:grid-cols-2">
          <p class="max-w-xl text-lg leading-relaxed text-zinc-400">{{ me?.intro }}</p>
          <div class="flex flex-wrap gap-3 lg:justify-end">
            <a href="#work" class="inline-flex items-center gap-2 rounded-full bg-brand-400 px-6 py-3.5 font-semibold text-black hover:bg-brand-300">See the work <ArrowDown class="size-4" /></a>
            <a href="#contact" class="inline-flex items-center gap-2 rounded-full border border-white/15 px-6 py-3.5 font-semibold text-white hover:bg-white/5">Get an estimate <ArrowUpRight class="size-4" /></a>
          </div>
        </div>
        <div class="mt-16 grid grid-cols-2 gap-px overflow-hidden rounded-3xl border border-white/10 bg-white/10 md:grid-cols-4">
          <div v-for="s in me?.stats" :key="s.label" class="bg-[#0a0a0a] p-6"><p class="text-3xl font-semibold text-white">{{ s.value }}</p><p class="mt-1 text-sm text-zinc-500">{{ s.label }}</p></div>
        </div>
      </div>
      <div class="overflow-hidden border-y border-white/5 py-5">
        <div class="marquee flex w-max gap-12 text-2xl font-semibold whitespace-nowrap text-zinc-700">
          <span v-for="i in 2" :key="i" class="flex gap-12"><span v-for="w in ['B2B SaaS', 'AI automation', 'E-commerce', 'Booking systems', 'Real estate', 'E-learning', 'Lead generation', 'Vue.js', 'FastAPI']" :key="w + i">{{ w }} <span class="text-brand-500">✦</span></span></span>
        </div>
      </div>
    </section>

    <!-- Work -->
    <section id="work" class="mx-auto max-w-7xl scroll-mt-20 px-6 py-24">
      <div class="flex flex-wrap items-end justify-between gap-6">
        <div>
          <p class="font-mono text-sm text-brand-400">01 — Selected work</p>
          <h2 class="mt-3 text-4xl font-semibold tracking-tight text-white sm:text-5xl">Seven products, one stack.</h2>
          <p class="mt-3 max-w-xl text-zinc-400">Every demo is a working Vue 3 + FastAPI app with its own API, data and admin. <span v-if="projects" class="text-zinc-300">{{ liveCount }}/{{ projects.length }} running right now.</span></p>
        </div>
        <div class="flex flex-wrap gap-2">
          <button v-for="c in categories" :key="c" class="rounded-full border px-4 py-1.5 text-sm transition" :class="filter === c ? 'border-white bg-white text-black' : 'border-white/10 hover:border-white/30'" @click="filter = c">{{ c }}</button>
        </div>
      </div>
      <TransitionGroup tag="div" class="mt-12 grid gap-6 md:grid-cols-2" move-class="transition duration-500" enter-from-class="opacity-0 translate-y-4" enter-active-class="transition duration-500">
        <ProjectCard v-for="(p, i) in shown" :key="p.slug" :project="p" :live="status[p.slug]" :large="i === 0 && filter === 'All'" :class="{ 'md:col-span-2': i === 0 && filter === 'All' }" />
      </TransitionGroup>
    </section>

    <!-- Services / skills -->
    <section id="services" class="scroll-mt-20 border-y border-white/5 bg-white/[.015] py-24">
      <div class="mx-auto max-w-7xl px-6">
        <p class="font-mono text-sm text-brand-400">02 — Services & stack</p>
        <h2 class="mt-3 max-w-2xl text-4xl font-semibold tracking-tight text-white sm:text-5xl">From idea to a product people pay for.</h2>
        <div class="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <div v-for="(items, group) in me?.skills" :key="group" class="rounded-3xl border border-white/10 p-6">
            <p class="font-semibold text-white">{{ group }}</p>
            <ul class="mt-4 space-y-2 text-sm"><li v-for="s in items" :key="s" class="flex items-center gap-2"><Check class="size-4 text-brand-400" />{{ s }}</li></ul>
          </div>
        </div>
        <div class="mt-6 rounded-3xl border border-white/10 p-6 text-sm text-zinc-400">
          <p class="font-semibold text-white">Architecture used in every project</p>
          <div class="mt-4 grid gap-3 font-mono text-xs md:grid-cols-3">
            <div class="rounded-xl bg-white/5 p-4"><p class="text-brand-300">models.py</p><p class="mt-1">Pydantic schemas + repository (the data)</p></div>
            <div class="rounded-xl bg-white/5 p-4"><p class="text-brand-300">service.py</p><p class="mt-1">Business rules — pricing, slots, scoring…</p></div>
            <div class="rounded-xl bg-white/5 p-4"><p class="text-brand-300">controller.py → Vue views</p><p class="mt-1">HTTP routes, consumed by per-module Vue pages</p></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing -->
    <section id="pricing" class="mx-auto max-w-7xl scroll-mt-20 px-6 py-24">
      <p class="font-mono text-sm text-brand-400">03 — Pricing</p>
      <h2 class="mt-3 text-4xl font-semibold tracking-tight text-white sm:text-5xl">Clear packages. No surprises.</h2>
      <div class="mt-12 grid gap-6 lg:grid-cols-3">
        <div v-for="p in me?.packages" :key="p.name" class="relative flex flex-col rounded-3xl border p-8" :class="p.popular ? 'border-brand-400 bg-brand-400/5' : 'border-white/10'">
          <span v-if="p.popular" class="absolute -top-3 left-8 rounded-full bg-brand-400 px-3 py-1 text-xs font-bold text-black">Most requested</span>
          <p class="text-lg font-semibold text-white">{{ p.name }}</p>
          <p class="text-sm text-zinc-500">{{ p.for }}</p>
          <p class="mt-6"><span class="text-sm text-zinc-500">{{ p.suffix }} </span><span class="text-5xl font-semibold tracking-tight text-white">{{ money(p.price) }}</span></p>
          <p class="mt-1 text-sm text-zinc-500">{{ p.timeline }}</p>
          <ul class="mt-8 flex-1 space-y-3 text-sm"><li v-for="f in p.features" :key="f" class="flex gap-2"><Check class="size-5 shrink-0 text-brand-400" />{{ f }}</li></ul>
          <a href="#contact" class="mt-8 inline-flex justify-center rounded-full py-3 font-semibold" :class="p.popular ? 'bg-brand-400 text-black hover:bg-brand-300' : 'border border-white/15 text-white hover:bg-white/5'">Get a quote</a>
        </div>
      </div>
      <div class="mt-6 grid gap-6 md:grid-cols-2">
        <div v-for="r in me?.retainers" :key="r.name" class="flex flex-wrap items-center gap-4 rounded-3xl border border-white/10 p-6">
          <Wrench class="size-6 text-brand-400" />
          <div class="flex-1"><p class="font-semibold text-white">{{ r.name }} retainer</p><p class="text-sm text-zinc-500">{{ r.features.join(' · ') }}</p></div>
          <p class="text-2xl font-semibold text-white">{{ money(r.price) }}<span class="text-sm text-zinc-500">/mo</span></p>
        </div>
      </div>
    </section>

    <!-- Process -->
    <section id="process" class="scroll-mt-20 border-y border-white/5 bg-white/[.015] py-24">
      <div class="mx-auto max-w-7xl px-6">
        <p class="font-mono text-sm text-brand-400">04 — Process</p>
        <h2 class="mt-3 text-4xl font-semibold tracking-tight text-white sm:text-5xl">How we'll work together</h2>
        <div class="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <div v-for="(s, i) in PROCESS" :key="s.title" class="rounded-3xl border border-white/10 p-6">
            <div class="flex items-center justify-between"><component :is="s.icon" class="size-6 text-brand-400" /><span class="font-mono text-sm text-zinc-600">0{{ i + 1 }}</span></div>
            <p class="mt-6 text-lg font-semibold text-white">{{ s.title }}</p><p class="mt-2 text-sm text-zinc-400">{{ s.text }}</p>
          </div>
        </div>
        <div class="mt-16 grid gap-6 md:grid-cols-3">
          <figure v-for="t in me?.testimonials" :key="t.quote" class="rounded-3xl bg-white/[.03] p-7">
            <Quote class="size-6 text-brand-400" /><blockquote class="mt-4 text-zinc-300">{{ t.quote }}</blockquote>
            <figcaption class="mt-5 text-sm"><span class="font-semibold text-white">{{ t.name }}</span> · <span class="text-zinc-500">{{ t.company }}</span></figcaption>
          </figure>
        </div>
      </div>
    </section>

    <!-- Contact -->
    <section id="contact" class="mx-auto max-w-7xl scroll-mt-20 px-6 py-24">
      <p class="font-mono text-sm text-brand-400">05 — Contact</p>
      <h2 class="mt-3 text-4xl font-semibold tracking-tight text-white sm:text-5xl">Let's build yours.</h2>
      <p class="mt-3 text-zinc-400">Price it in 10 seconds, then send it over. Or email <a :href="`mailto:${me?.email}`" class="text-white underline decoration-brand-400 underline-offset-4">{{ me?.email }}</a>.</p>
      <div class="mt-12"><EstimateContact /></div>
    </section>
  </div>
</template>
