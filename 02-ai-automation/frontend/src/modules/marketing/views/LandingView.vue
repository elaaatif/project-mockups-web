<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import {
  ArrowRight, BarChart3, Bot, Check, FileScan, Mail, MessageCircle, Plug, Rocket, Search, Sparkles, Workflow,
} from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { pricingService } from '../pricing.service'

const { data: plans } = useResource(pricingService.plans)

const solutions = [
  { icon: Bot, title: 'AI customer support', text: 'A chatbot trained on your policies and order data that resolves 70% of tickets on web and WhatsApp — and hands off gracefully.', to: '/app/chatbot', tone: 'from-violet-500 to-fuchsia-500' },
  { icon: FileScan, title: 'Document & PDF extraction', text: 'Invoices, receipts, contracts and POs turned into structured data with confidence scores, ready for your ERP.', to: '/app/extraction', tone: 'from-sky-500 to-indigo-500' },
  { icon: BarChart3, title: 'Automated reporting', text: 'KPI reports with charts and a written AI summary, delivered by email, Slack or WhatsApp on your schedule.', to: '/app/reports', tone: 'from-emerald-500 to-teal-500' },
  { icon: Workflow, title: 'Email & WhatsApp workflows', text: 'Visual workflows that read, classify, reply and update your CRM — without anyone copy-pasting.', to: '/app/workflows', tone: 'from-amber-500 to-orange-500' },
]
const steps = [
  { icon: Search, title: 'Audit', text: 'We map your repetitive work and estimate hours saved.' },
  { icon: Plug, title: 'Connect', text: 'Email, WhatsApp, CRM, ERP and drives — connected in days.' },
  { icon: Rocket, title: 'Automate', text: 'Go live with monitoring, human review and clear ROI.' },
]

// Animated chat preview in the hero
const script = [
  { from: 'user', text: 'Hi! Where is my order #10482?' },
  { from: 'bot', text: 'It\'s out for delivery with DHL — arriving today before 6 pm 📦' },
  { from: 'user', text: 'Great, and can I return the lamp if it doesn\'t fit?' },
  { from: 'bot', text: 'Of course — 30-day free returns. I\'ve emailed you a prepaid label ✓' },
]
const shown = ref(1)
let timer
onMounted(() => { timer = setInterval(() => { shown.value = shown.value >= script.length ? 1 : shown.value + 1 }, 1800) })
onUnmounted(() => clearInterval(timer))
</script>

<template>
  <div class="min-h-screen bg-[#07060d] text-slate-300">
    <!-- Nav -->
    <header class="sticky top-0 z-30 border-b border-white/5 bg-[#07060d]/70 backdrop-blur-xl">
      <div class="mx-auto flex h-16 max-w-7xl items-center gap-8 px-6">
        <a href="#" class="flex items-center gap-2.5 text-lg font-bold text-white">
          <span class="grid size-9 place-items-center rounded-xl bg-gradient-to-br from-brand-400 to-fuchsia-600"><Sparkles class="size-5" /></span> Autom8
        </a>
        <nav class="hidden gap-7 text-sm md:flex">
          <a href="#solutions" class="hover:text-white">Solutions</a><a href="#how" class="hover:text-white">How it works</a><a href="#pricing" class="hover:text-white">Pricing</a>
        </nav>
        <RouterLink to="/app" class="btn btn-primary ml-auto">Open console <ArrowRight class="size-4" /></RouterLink>
      </div>
    </header>

    <!-- Hero -->
    <section class="relative overflow-hidden">
      <div class="pointer-events-none absolute -top-40 left-1/2 size-[50rem] -translate-x-1/2 rounded-full bg-brand-600/25 blur-[120px]" />
      <div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,.04)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,.04)_1px,transparent_1px)] bg-[size:56px_56px] [mask-image:radial-gradient(ellipse_at_center,black,transparent_75%)]" />
      <div class="relative mx-auto grid max-w-7xl items-center gap-16 px-6 py-24 lg:grid-cols-2">
        <div>
          <span class="inline-flex items-center gap-2 rounded-full border border-brand-500/30 bg-brand-500/10 px-3 py-1 text-xs font-medium text-brand-200">
            <span class="size-1.5 animate-pulse rounded-full bg-brand-400" /> AI integration demand up 178% in 2026
          </span>
          <h1 class="mt-6 text-5xl leading-[1.05] font-extrabold tracking-tight text-white sm:text-6xl">
            Put your repetitive work on <span class="bg-gradient-to-r from-brand-300 via-fuchsia-400 to-amber-300 bg-clip-text text-transparent">autopilot</span>
          </h1>
          <p class="mt-6 max-w-xl text-lg text-slate-400">Autom8 builds AI chatbots, document extraction, automated reports and email & WhatsApp workflows that plug into the tools you already use.</p>
          <div class="mt-9 flex flex-wrap gap-3">
            <RouterLink to="/app/chatbot" class="btn btn-primary !px-6 !py-3.5 !text-base">Try the live chatbot <ArrowRight class="size-4" /></RouterLink>
            <RouterLink to="/app/extraction" class="btn !px-6 !py-3.5 !text-base bg-white/5 text-white ring-1 ring-white/10 hover:bg-white/10">Extract a PDF</RouterLink>
          </div>
          <div class="mt-10 flex gap-10">
            <div><p class="text-3xl font-bold text-white">70%</p><p class="text-sm">tickets resolved by AI</p></div>
            <div><p class="text-3xl font-bold text-white">12×</p><p class="text-sm">faster invoice entry</p></div>
            <div><p class="text-3xl font-bold text-white">540h</p><p class="text-sm">saved per month</p></div>
          </div>
        </div>

        <div class="relative">
          <div class="absolute -inset-6 rounded-[2rem] bg-gradient-to-br from-brand-500/30 to-fuchsia-500/10 blur-2xl" />
          <div class="relative rounded-3xl border border-white/10 bg-white/[.03] p-5 shadow-2xl backdrop-blur">
            <div class="flex items-center gap-3 border-b border-white/5 pb-4">
              <span class="grid size-10 place-items-center rounded-full bg-gradient-to-br from-brand-500 to-fuchsia-500"><Bot class="size-5 text-white" /></span>
              <div><p class="font-semibold text-white">Nova · Lumen Home</p><p class="flex items-center gap-1.5 text-xs text-emerald-400"><span class="size-1.5 rounded-full bg-emerald-400" />Online · replies instantly</p></div>
              <MessageCircle class="ml-auto size-5 text-emerald-400" />
            </div>
            <TransitionGroup tag="div" class="min-h-72 space-y-3 py-5" enter-from-class="opacity-0 translate-y-2" enter-active-class="transition duration-500">
              <div v-for="(m, i) in script.slice(0, shown)" :key="i" class="flex" :class="m.from === 'user' ? 'justify-end' : ''">
                <p class="max-w-[80%] rounded-2xl px-4 py-2.5 text-sm" :class="m.from === 'user' ? 'rounded-br-md bg-brand-600 text-white' : 'rounded-bl-md bg-white/10 text-slate-100'">{{ m.text }}</p>
              </div>
            </TransitionGroup>
            <div class="flex flex-wrap gap-2 border-t border-white/5 pt-4 text-xs">
              <span class="rounded-full bg-white/5 px-2.5 py-1 font-mono text-brand-200">intent: order_status</span>
              <span class="rounded-full bg-white/5 px-2.5 py-1 font-mono text-emerald-300">confidence 0.97</span>
              <span class="rounded-full bg-white/5 px-2.5 py-1 font-mono text-amber-200">180 ms</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Solutions -->
    <section id="solutions" class="mx-auto max-w-7xl px-6 py-24">
      <p class="text-sm font-semibold tracking-widest text-brand-400 uppercase">Solutions</p>
      <h2 class="mt-2 max-w-2xl text-4xl font-bold tracking-tight text-white">Four automations that pay for themselves in the first quarter</h2>
      <div class="mt-12 grid gap-5 md:grid-cols-2">
        <RouterLink v-for="s in solutions" :key="s.title" :to="s.to" class="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/[.03] p-8 transition hover:border-brand-500/40 hover:bg-white/[.05]">
          <span class="grid size-12 place-items-center rounded-2xl bg-gradient-to-br text-white shadow-lg" :class="s.tone"><component :is="s.icon" class="size-6" /></span>
          <h3 class="mt-6 text-xl font-semibold text-white">{{ s.title }}</h3>
          <p class="mt-2 text-slate-400">{{ s.text }}</p>
          <span class="mt-5 inline-flex items-center gap-1 text-sm font-semibold text-brand-300">Open live demo <ArrowRight class="size-4 transition group-hover:translate-x-1" /></span>
        </RouterLink>
      </div>
    </section>

    <!-- How -->
    <section id="how" class="border-y border-white/5 bg-white/[.02] py-24">
      <div class="mx-auto max-w-7xl px-6">
        <h2 class="text-center text-4xl font-bold tracking-tight text-white">From audit to autopilot in 3 weeks</h2>
        <div class="mt-14 grid gap-8 md:grid-cols-3">
          <div v-for="(s, i) in steps" :key="s.title" class="relative text-center">
            <span class="mx-auto grid size-16 place-items-center rounded-2xl border border-brand-500/30 bg-brand-500/10 text-brand-300"><component :is="s.icon" class="size-7" /></span>
            <p class="mt-5 font-mono text-xs text-brand-400">STEP 0{{ i + 1 }}</p>
            <h3 class="mt-1 text-xl font-semibold text-white">{{ s.title }}</h3>
            <p class="mt-2 text-slate-400">{{ s.text }}</p>
          </div>
        </div>
        <div class="mt-14 flex flex-wrap items-center justify-center gap-3 text-sm">
          <span v-for="t in ['Gmail', 'Outlook', 'WhatsApp Business', 'HubSpot', 'Salesforce', 'Shopify', 'Xero', 'SAP', 'Google Sheets', 'Slack']" :key="t" class="rounded-full border border-white/10 px-4 py-1.5">{{ t }}</span>
        </div>
      </div>
    </section>

    <!-- Pricing -->
    <section id="pricing" class="mx-auto max-w-7xl px-6 py-24">
      <h2 class="text-center text-4xl font-bold tracking-tight text-white">Pricing that tracks the value</h2>
      <p class="mt-3 text-center text-slate-400">One-time setup + a monthly platform fee. Cancel anytime.</p>
      <div class="mt-12 grid gap-6 lg:grid-cols-3">
        <div v-for="p in plans" :key="p.name" class="relative rounded-3xl border p-8" :class="p.popular ? 'border-brand-500 bg-gradient-to-b from-brand-600/20 to-transparent' : 'border-white/10 bg-white/[.03]'">
          <span v-if="p.popular" class="absolute -top-3 left-8 rounded-full bg-brand-500 px-3 py-1 text-xs font-bold text-white">Most popular</span>
          <h3 class="text-lg font-semibold text-white">{{ p.name }}</h3>
          <p class="mt-4"><span class="text-5xl font-bold text-white">{{ p.price }}</span><span class="text-slate-500">{{ p.period }}</span></p>
          <p class="mt-1 text-sm text-brand-300">{{ p.setup }}</p>
          <ul class="mt-8 space-y-3 text-sm">
            <li v-for="f in p.features" :key="f" class="flex gap-2.5"><Check class="size-5 shrink-0 text-brand-400" />{{ f }}</li>
          </ul>
          <RouterLink to="/app" class="btn mt-8 w-full" :class="p.popular ? 'btn-primary' : 'bg-white/5 text-white ring-1 ring-white/10 hover:bg-white/10'">Book a demo</RouterLink>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-5xl px-6 pb-24">
      <div class="rounded-3xl bg-gradient-to-br from-brand-600 via-fuchsia-600 to-amber-500 p-px">
        <div class="rounded-3xl bg-[#0c0a17] p-12 text-center">
          <Mail class="mx-auto size-10 text-brand-300" />
          <h2 class="mt-4 text-3xl font-bold text-white">Get a free automation audit</h2>
          <p class="mt-2 text-slate-400">We'll show you the 3 workflows with the highest ROI in your business.</p>
          <form class="mx-auto mt-8 flex max-w-md gap-2" @submit.prevent>
            <input class="input !border-white/10 !bg-white/5 !text-white" placeholder="you@company.com" type="email" />
            <button class="btn btn-primary shrink-0">Request audit</button>
          </form>
        </div>
      </div>
    </section>
    <footer class="border-t border-white/5 py-10 text-center text-sm text-slate-500">© 2026 Autom8 Labs · Built with Vue 3 + FastAPI</footer>
  </div>
</template>
