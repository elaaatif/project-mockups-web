<script setup>
import { computed } from 'vue'
import { Bar, Doughnut } from 'vue-chartjs'
import { Bot, Clock, FileScan, PiggyBank, Workflow, Zap } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard from '@/components/ui/StatCard.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { useResource } from '@/core/resource'
import { money, number } from '@/core/format'
import { overviewService } from '../overview.service'

const { data, error, reload } = useResource(overviewService.get)

const barData = computed(() => ({
  labels: data.value.daily.labels,
  datasets: [{ label: 'Automated tasks', data: data.value.daily.values, backgroundColor: '#8b5cf6', hoverBackgroundColor: '#6d28d9', borderRadius: 6, barPercentage: 0.7 }],
}))
const barOptions = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false } }, y: { grid: { color: '#f1f5f9' } } } }
const donutData = computed(() => ({
  labels: data.value.channels.labels,
  datasets: [{ data: data.value.channels.values, backgroundColor: ['#7c3aed', '#10b981', '#38bdf8', '#f59e0b'], borderWidth: 0 }],
}))
const donutOptions = { responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, boxWidth: 8 } } } }
const roi = computed(() => Math.round(data.value.savings.manual_cost / data.value.savings.platform_cost))
</script>

<template>
  <div>
    <PageHeader title="Automation overview" subtitle="What your AI workforce did over the last 30 days">
      <RouterLink to="/app/workflows" class="btn btn-primary"><Workflow class="size-4" /> New workflow</RouterLink>
    </PageHeader>

    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Hours saved" :value="number(data.kpis.hours_saved) + ' h'" :icon="Clock" :delta="22.4" hint="vs last month" />
        <StatCard label="Tasks automated" :value="number(data.kpis.tasks_automated)" :icon="Zap" tone="amber" :hint="`${data.kpis.active_workflows} active workflows`" />
        <StatCard label="AI resolution rate" :value="data.kpis.ai_resolution + '%'" :icon="Bot" tone="emerald" hint="support conversations" />
        <StatCard label="Documents processed" :value="number(data.kpis.documents_processed)" :icon="FileScan" tone="sky" hint="invoices, receipts, contracts" />
      </div>

      <div class="mt-6 grid gap-6 xl:grid-cols-3">
        <div class="card p-6 xl:col-span-2">
          <h3 class="font-bold">Automated tasks per day</h3>
          <p class="text-sm text-slate-500">Across all workflows and channels</p>
          <div class="mt-4 h-72"><Bar :data="barData" :options="barOptions" /></div>
        </div>
        <div class="card p-6">
          <h3 class="font-bold">By channel</h3>
          <p class="text-sm text-slate-500">Share of automated volume</p>
          <div class="mt-4 h-72"><Doughnut :data="donutData" :options="donutOptions" /></div>
        </div>
      </div>

      <div class="mt-6 overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-brand-950 to-slate-950 p-8 text-white">
        <div class="flex flex-wrap items-center gap-8">
          <span class="grid size-14 place-items-center rounded-2xl bg-brand-500/20 text-brand-300"><PiggyBank class="size-7" /></span>
          <div class="flex-1">
            <p class="text-sm text-brand-200">Return on investment this month</p>
            <p class="mt-1 text-4xl font-extrabold">{{ roi }}× <span class="text-lg font-medium text-slate-400">your platform fee</span></p>
          </div>
          <div class="grid grid-cols-2 gap-8 text-sm">
            <div><p class="text-slate-400">Equivalent manual cost</p><p class="mt-1 text-2xl font-bold">{{ money(data.savings.manual_cost) }}</p></div>
            <div><p class="text-slate-400">Autom8 Scale plan</p><p class="mt-1 text-2xl font-bold">{{ money(data.savings.platform_cost) }}</p></div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
