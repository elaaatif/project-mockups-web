<script setup>
import { computed } from 'vue'
import { Bar, Doughnut } from 'vue-chartjs'
import { CalendarClock, Eye, Percent, Users, Wallet } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard from '@/components/ui/StatCard.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { useResource } from '@/core/resource'
import { img } from '@/core/media'
import { shortPrice } from '@/modules/listings/listings.service'
import { agentService } from '../agent.service'

const { data, error, reload } = useResource(agentService.overview)
const compact = (n) => (n >= 1e6 ? `£${(n / 1e6).toFixed(1)}m` : `£${Math.round(n / 1000)}k`)
const bar = computed(() => ({ labels: data.value.deals_by_month.labels, datasets: [{ data: data.value.deals_by_month.values, backgroundColor: '#0f172a', hoverBackgroundColor: '#d97706', borderRadius: 6 }] }))
const barOpts = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false } }, y: { grid: { color: '#f1f5f9' } } } }
const donut = computed(() => ({ labels: data.value.sources.labels, datasets: [{ data: data.value.sources.values, backgroundColor: ['#d97706', '#0f172a', '#64748b', '#fbbf24', '#10b981', '#0ea5e9', '#f43f5e'], borderWidth: 0 }] }))
const donutOpts = { responsive: true, maintainAspectRatio: false, cutout: '68%', plugins: { legend: { position: 'right', labels: { boxWidth: 10, usePointStyle: true } } } }
</script>

<template>
  <div>
    <PageHeader title="Good morning, Sophie" subtitle="Your pipeline, viewings and listing performance">
      <RouterLink to="/app/leads" class="btn btn-primary"><Users class="size-4" /> Open pipeline</RouterLink>
    </PageHeader>
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Active leads" :value="data.kpis.active_leads" :icon="Users" :delta="14" hint="vs last month" />
        <StatCard label="Upcoming viewings" :value="data.kpis.viewings_week" :icon="CalendarClock" tone="sky" />
        <StatCard label="Sales pipeline value" :value="compact(data.kpis.pipeline_value)" :icon="Wallet" tone="emerald" hint="active buyer budgets" />
        <StatCard label="Lead conversion" :value="data.kpis.conversion + '%'" :icon="Percent" tone="amber" hint="won / all leads" />
      </div>
      <div class="mt-6 grid gap-6 xl:grid-cols-5">
        <div class="card p-6 xl:col-span-3"><h3 class="font-bold">Deals completed per month</h3><div class="mt-4 h-64"><Bar :data="bar" :options="barOpts" /></div></div>
        <div class="card p-6 xl:col-span-2"><h3 class="font-bold">Lead sources</h3><div class="mt-4 h-64"><Doughnut :data="donut" :options="donutOpts" /></div></div>
      </div>
      <div class="card mt-6 p-6">
        <h3 class="font-bold">Most viewed listings</h3>
        <div class="mt-4 divide-y divide-slate-100">
          <RouterLink v-for="p in data.top_listings" :key="p.id" :to="`/property/${p.slug}`" class="flex items-center gap-4 py-3 hover:bg-slate-50">
            <img :src="img(p.images[0], 160)" :alt="p.title" class="h-12 w-16 rounded-lg object-cover" />
            <div class="flex-1"><p class="font-semibold">{{ p.title }}</p><p class="text-xs text-slate-500">{{ p.district }} · listed {{ p.listed_days }}d ago</p></div>
            <p class="font-semibold">{{ shortPrice(p) }}</p>
            <p class="flex w-20 items-center justify-end gap-1 text-sm text-slate-500"><Eye class="size-4" />{{ p.views.toLocaleString() }}</p>
          </RouterLink>
        </div>
      </div>
    </template>
  </div>
</template>
