<script setup>
import { ref } from 'vue'
import {
  ArrowRight, BadgeCheck, Boxes, Check, FileCheck, Headphones, PlayCircle, Receipt, ShieldCheck, Truck, Users, Workflow, Zap,
} from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { money } from '@/core/format'
import { billingService } from '../billing.service'

const annual = ref(true)
const { data: catalog } = useResource(billingService.plans)

const modules = [
  { icon: Boxes, title: 'Inventory, invoicing & purchasing', text: 'Live stock levels, reorder alerts, purchase orders that update stock on receipt, and invoices that chase themselves.', tone: 'from-indigo-500 to-blue-500' },
  { icon: Users, title: 'HR, leave & payroll', text: 'Employee records, self-service leave with approval flows, and one-click payroll runs with tax and social deductions.', tone: 'from-emerald-500 to-teal-500' },
  { icon: Truck, title: 'Fleet, maintenance & insurance', text: 'Service intervals by mileage, maintenance logs, and insurance renewals tracked before they lapse.', tone: 'from-amber-500 to-orange-500' },
  { icon: FileCheck, title: 'Documents & approvals', text: 'Multi-step approval chains for contracts, policies and purchase requests — with a full audit trail.', tone: 'from-rose-500 to-pink-500' },
]
const faqs = [
  ['How long does onboarding take?', 'Most teams are live in under two weeks. Growth and Enterprise include a guided setup where we import your products, staff and vehicles.'],
  ['Can I pay monthly?', 'Yes. Monthly plans can be cancelled anytime; annual plans save 20%.'],
  ['What does the support contract cover?', 'Response-time guarantees, configuration help, and for Premium a named engineer who knows your setup.'],
]
</script>

<template>
  <div class="bg-white">
    <!-- Nav -->
    <header class="sticky top-0 z-30 border-b border-slate-100 bg-white/80 backdrop-blur-xl">
      <div class="mx-auto flex h-16 max-w-7xl items-center gap-8 px-6">
        <a href="#" class="flex items-center gap-2.5 text-lg font-extrabold">
          <span class="grid size-9 place-items-center rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 text-white"><Workflow class="size-5" /></span> OpsFlow
        </a>
        <nav class="hidden gap-7 text-sm font-medium text-slate-600 md:flex">
          <a href="#modules" class="hover:text-slate-900">Modules</a>
          <a href="#pricing" class="hover:text-slate-900">Pricing</a>
          <a href="#support" class="hover:text-slate-900">Support</a>
          <a href="#faq" class="hover:text-slate-900">FAQ</a>
        </nav>
        <div class="ml-auto flex items-center gap-2">
          <RouterLink to="/app" class="btn btn-ghost hidden sm:inline-flex">Sign in</RouterLink>
          <RouterLink to="/app" class="btn btn-primary">Open live demo <ArrowRight class="size-4" /></RouterLink>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <section class="relative overflow-hidden">
      <div class="absolute inset-0 -z-10 bg-[radial-gradient(60rem_30rem_at_50%_-10%,var(--color-brand-100),transparent)]" />
      <div class="mx-auto max-w-7xl px-6 pt-20 pb-16 text-center">
        <span class="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-white px-3 py-1 text-xs font-semibold text-brand-700 shadow-sm">
          <Zap class="size-3.5" /> New: automated payroll runs & fleet insurance alerts
        </span>
        <h1 class="mx-auto mt-6 max-w-4xl text-5xl font-extrabold tracking-tight text-slate-900 sm:text-6xl">
          Run your entire operation from <span class="bg-gradient-to-r from-brand-600 to-violet-500 bg-clip-text text-transparent">one calm dashboard</span>
        </h1>
        <p class="mx-auto mt-6 max-w-2xl text-lg text-slate-600">
          OpsFlow replaces the spreadsheets behind your inventory, invoices, staff, vehicles and approvals — so recurring work runs itself.
        </p>
        <div class="mt-9 flex flex-wrap justify-center gap-3">
          <RouterLink to="/app" class="btn btn-primary !px-6 !py-3.5 !text-base">Start 14-day trial <ArrowRight class="size-4" /></RouterLink>
          <RouterLink to="/app" class="btn btn-secondary !px-6 !py-3.5 !text-base"><PlayCircle class="size-5 text-brand-600" /> Explore the demo</RouterLink>
        </div>
        <p class="mt-4 text-xs text-slate-500">No credit card · Cancel anytime · Data hosted in EU</p>

        <!-- Product mock -->
        <div class="relative mx-auto mt-16 max-w-5xl">
          <div class="absolute -inset-4 -z-10 rounded-[2rem] bg-gradient-to-r from-brand-400/30 via-violet-400/20 to-sky-400/30 blur-2xl" />
          <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white text-left shadow-2xl">
            <div class="flex items-center gap-1.5 border-b border-slate-100 bg-slate-50 px-4 py-3">
              <span class="size-3 rounded-full bg-rose-400" /><span class="size-3 rounded-full bg-amber-400" /><span class="size-3 rounded-full bg-emerald-400" />
              <span class="ml-4 rounded-md bg-white px-3 py-0.5 text-xs text-slate-400 ring-1 ring-slate-200">app.opsflow.io/dashboard</span>
            </div>
            <div class="grid grid-cols-12">
              <div class="col-span-3 hidden space-y-2 bg-slate-950 p-4 sm:block">
                <div v-for="(w, i) in [80, 64, 72, 56, 68, 60]" :key="i" class="h-7 rounded-lg" :class="i === 0 ? 'bg-brand-600' : 'bg-white/5'" :style="{ width: w + '%' }" />
              </div>
              <div class="col-span-12 space-y-4 p-5 sm:col-span-9">
                <div class="grid grid-cols-3 gap-3">
                  <div v-for="k in [['Revenue', '$71,240', 'text-emerald-600'], ['Outstanding', '$18,930', 'text-amber-600'], ['Approvals', '9 pending', 'text-brand-600']]" :key="k[0]" class="rounded-xl border border-slate-100 p-3">
                    <p class="text-[11px] text-slate-500">{{ k[0] }}</p><p class="mt-1 font-bold" :class="k[2]">{{ k[1] }}</p>
                  </div>
                </div>
                <div class="flex h-40 items-end gap-2 rounded-xl border border-slate-100 p-4">
                  <div v-for="(h, i) in [40, 55, 48, 62, 58, 70, 66, 78, 74, 85, 80, 94]" :key="i" class="flex-1 rounded-t-md bg-gradient-to-t from-brand-600 to-brand-400" :style="{ height: h + '%' }" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="mx-auto flex max-w-5xl flex-wrap items-center justify-center gap-x-12 gap-y-4 px-6 pb-16 text-lg font-bold text-slate-300">
        <span>NORTHWIND</span><span>acme/logistics</span><span>Cedar Health</span><span>SUMMIT FOODS</span><span>orion·build</span>
      </div>
    </section>

    <!-- Modules -->
    <section id="modules" class="bg-slate-50 py-24">
      <div class="mx-auto max-w-7xl px-6">
        <p class="text-sm font-bold tracking-widest text-brand-600 uppercase">Modules</p>
        <h2 class="mt-2 max-w-2xl text-4xl font-extrabold tracking-tight text-slate-900">Every recurring operational problem, solved in one place</h2>
        <div class="mt-12 grid gap-6 md:grid-cols-2">
          <div v-for="m in modules" :key="m.title" class="card group p-7 transition hover:-translate-y-1 hover:shadow-xl">
            <span class="grid size-12 place-items-center rounded-2xl bg-gradient-to-br text-white shadow-lg" :class="m.tone"><component :is="m.icon" class="size-6" /></span>
            <h3 class="mt-5 text-xl font-bold text-slate-900">{{ m.title }}</h3>
            <p class="mt-2 text-slate-600">{{ m.text }}</p>
            <RouterLink to="/app" class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-brand-600">See it live <ArrowRight class="size-4 transition group-hover:translate-x-1" /></RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing -->
    <section id="pricing" class="py-24">
      <div class="mx-auto max-w-7xl px-6">
        <div class="text-center">
          <p class="text-sm font-bold tracking-widest text-brand-600 uppercase">Pricing</p>
          <h2 class="mt-2 text-4xl font-extrabold tracking-tight text-slate-900">Simple subscriptions that scale with you</h2>
          <div class="mt-8 inline-flex rounded-xl bg-slate-100 p-1">
            <button class="tab" :class="{ 'tab-active': !annual }" @click="annual = false">Monthly</button>
            <button class="tab" :class="{ 'tab-active': annual }" @click="annual = true">Annual <span class="ml-1 rounded-full bg-emerald-100 px-1.5 text-[11px] text-emerald-700">-20%</span></button>
          </div>
        </div>
        <div v-if="catalog" class="mt-12 grid gap-6 lg:grid-cols-3">
          <div v-for="p in catalog.plans" :key="p.id" class="relative rounded-3xl p-8"
               :class="p.popular ? 'bg-slate-950 text-white shadow-2xl shadow-brand-900/30 ring-2 ring-brand-500' : 'card'">
            <span v-if="p.popular" class="absolute -top-3 left-8 rounded-full bg-brand-500 px-3 py-1 text-xs font-bold text-white">Most popular</span>
            <h3 class="text-lg font-bold">{{ p.name }}</h3>
            <p class="text-sm" :class="p.popular ? 'text-slate-400' : 'text-slate-500'">{{ p.users }}</p>
            <p class="mt-6 flex items-baseline gap-1"><span class="text-5xl font-extrabold tracking-tight">${{ annual ? p.annual : p.monthly }}</span><span class="text-sm opacity-60">/mo</span></p>
            <p class="mt-1 text-xs opacity-60">{{ annual ? 'billed annually' : 'billed monthly' }} · setup fee {{ p.setup_fee ? money(p.setup_fee) : 'waived' }}</p>
            <RouterLink to="/app" class="btn mt-6 w-full" :class="p.popular ? 'btn-primary' : 'btn-secondary'">Start with {{ p.name }}</RouterLink>
            <ul class="mt-8 space-y-3 text-sm">
              <li v-for="f in p.features" :key="f" class="flex gap-2.5"><Check class="size-5 shrink-0 text-brand-500" />{{ f }}</li>
            </ul>
          </div>
        </div>

        <!-- Support contracts -->
        <div id="support" class="mt-20 rounded-3xl bg-gradient-to-br from-brand-50 to-white p-8 ring-1 ring-brand-100 sm:p-10">
          <div class="flex items-center gap-3"><Headphones class="size-6 text-brand-600" /><h3 class="text-2xl font-bold">Support contracts</h3></div>
          <p class="mt-2 text-slate-600">Add guaranteed response times to any plan.</p>
          <div v-if="catalog" class="mt-6 grid gap-4 md:grid-cols-3">
            <div v-for="s in catalog.support" :key="s.name" class="rounded-2xl bg-white p-5 ring-1 ring-slate-200">
              <div class="flex items-center justify-between"><p class="font-bold">{{ s.name }}</p><p class="font-bold text-brand-600">{{ s.price ? money(s.price) + '/mo' : 'Included' }}</p></div>
              <p class="mt-3 flex items-center gap-2 text-sm text-slate-600"><ShieldCheck class="size-4 text-emerald-500" /> {{ s.response }} response</p>
              <p class="mt-1 flex items-center gap-2 text-sm text-slate-600"><BadgeCheck class="size-4 text-emerald-500" /> {{ s.channels }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ + CTA -->
    <section id="faq" class="bg-slate-50 py-24">
      <div class="mx-auto max-w-3xl px-6">
        <h2 class="text-center text-3xl font-extrabold tracking-tight">Frequently asked questions</h2>
        <div class="mt-10 space-y-3">
          <details v-for="f in faqs" :key="f[0]" class="card group p-5 open:shadow-md">
            <summary class="flex cursor-pointer list-none items-center justify-between font-semibold">{{ f[0] }}<span class="text-brand-600 transition group-open:rotate-45">+</span></summary>
            <p class="mt-3 text-slate-600">{{ f[1] }}</p>
          </details>
        </div>
      </div>
      <div class="mx-auto mt-20 max-w-5xl px-6">
        <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-brand-600 to-violet-700 p-10 text-center text-white shadow-2xl sm:p-14">
          <Receipt class="absolute -top-6 -right-6 size-40 opacity-10" />
          <h2 class="text-3xl font-extrabold sm:text-4xl">Stop chasing spreadsheets.</h2>
          <p class="mx-auto mt-3 max-w-xl text-brand-100">Join 1,200+ operations teams who closed their month 3× faster with OpsFlow.</p>
          <RouterLink to="/app" class="btn mt-8 bg-white !px-6 !py-3 text-brand-700 hover:bg-brand-50">Launch the live demo <ArrowRight class="size-4" /></RouterLink>
        </div>
      </div>
    </section>
    <footer class="border-t border-slate-100 py-10 text-center text-sm text-slate-500">© 2026 OpsFlow Inc. · Built with Vue 3 + FastAPI</footer>
  </div>
</template>
