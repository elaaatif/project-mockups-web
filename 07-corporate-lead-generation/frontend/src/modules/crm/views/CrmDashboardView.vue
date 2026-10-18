<script setup>
import { computed } from 'vue'
import { Doughnut, Line } from 'vue-chartjs'
import { CheckCircle2, FileSpreadsheet, Flame, Inbox, PoundSterling, Search, UserCheck, XCircle } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard from '@/components/ui/StatCard.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { useResource } from '@/core/resource'
import { crmService } from '../crm.service'

const { data, error, reload } = useResource(crmService.overview)
const { data: seo } = useResource(crmService.seoAudit)
const compact = (n) => (n >= 1e6 ? `£${(n / 1e6).toFixed(2)}m` : `£${Math.round(n / 1000)}k`)
const line = computed(() => ({
  labels: data.value.traffic.labels,
  datasets: [
    { label: 'Website visits', data: data.value.traffic.visits, borderColor: '#0f172a', backgroundColor: 'rgba(15,23,42,.06)', fill: true, tension: 0.4, pointRadius: 0, yAxisID: 'y' },
    { label: 'Leads', data: data.value.traffic.leads, borderColor: '#f97316', tension: 0.4, pointRadius: 0, borderWidth: 2.5, yAxisID: 'y1' },
  ],
}))
const lineOpts = { responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false }, plugins: { legend: { position: 'top', align: 'end', labels: { usePointStyle: true, boxWidth: 8 } } },
  scales: { x: { grid: { display: false } }, y: { grid: { color: '#f1f5f9' } }, y1: { position: 'right', grid: { display: false } } } }
const donut = computed(() => ({ labels: data.value.sources.labels, datasets: [{ data: data.value.sources.values, backgroundColor: ['#f97316', '#0f172a', '#64748b', '#fdba74', '#0ea5e9', '#10b981'], borderWidth: 0 }] }))
const donutOpts = { responsive: true, maintainAspectRatio: false, cutout: '68%', plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, usePointStyle: true } } } }
</script>

<template>
  <div>
    <PageHeader title="Lead generation dashboard" subtitle="Website → RFQ → order. Everything the corporate site generates, in one place." />
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Quote requests" :value="data.kpis.rfqs" :icon="FileSpreadsheet" :delta="18" :hint="`${data.kpis.hot} hot`" />
        <StatCard label="Open pipeline" :value="compact(data.kpis.pipeline)" :icon="PoundSterling" tone="emerald" :hint="`won ${compact(data.kpis.won_value)}`" />
        <StatCard label="Unread messages" :value="data.kpis.messages" :icon="Inbox" tone="sky" />
        <StatCard label="New applications" :value="data.kpis.applications" :icon="UserCheck" tone="amber" />
      </div>
      <div class="mt-6 grid gap-6 xl:grid-cols-3">
        <div class="card p-6 xl:col-span-2"><h3 class="font-bold">Traffic vs leads · 30 days</h3><div class="mt-4 h-72"><Line :data="line" :options="lineOpts" /></div></div>
        <div class="card p-6"><h3 class="font-bold">Lead sources</h3><div class="mt-4 h-72"><Doughnut :data="donut" :options="donutOpts" /></div></div>
      </div>
      <div class="mt-6 grid gap-6 lg:grid-cols-2">
        <div class="card p-6">
          <h3 class="flex items-center gap-2 font-bold"><Search class="size-5 text-brand-600" /> SEO health</h3>
          <p class="text-sm text-slate-500">{{ seo?.indexable_pages }} indexable pages · <a href="/api/seo/sitemap.xml" target="_blank" class="font-semibold text-brand-700">sitemap.xml</a></p>
          <ul class="mt-4 space-y-2.5 text-sm"><li v-for="c in seo?.checks" :key="c.label" class="flex items-center gap-2"><component :is="c.ok ? CheckCircle2 : XCircle" class="size-4" :class="c.ok ? 'text-emerald-500' : 'text-rose-500'" />{{ c.label }}</li></ul>
        </div>
        <div class="card flex flex-col justify-center gap-3 bg-slate-950 p-6 text-white">
          <Flame class="size-8 text-brand-500" />
          <p class="text-2xl font-bold">{{ data.kpis.hot }} hot RFQs need a reply</p>
          <p class="text-sm text-slate-400">Leads scored ≥ 70 by budget, timeline, business email and scope. Replying within 4 hours doubles win rate.</p>
          <RouterLink to="/app/rfqs" class="btn btn-primary mt-2 self-start">Open quote requests</RouterLink>
        </div>
      </div>
    </template>
  </div>
</template>
