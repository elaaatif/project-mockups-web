<script setup>
import { computed } from 'vue'
import { Bar, Doughnut } from 'vue-chartjs'
import { AlertTriangle, DollarSign, FileText, ShoppingCart, Store } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard from '@/components/ui/StatCard.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { useResource } from '@/core/resource'
import { money } from '@/core/format'
import { adminService } from '../admin.service'

const { data, error, reload } = useResource(adminService.overview)
const barData = computed(() => ({ labels: data.value.daily.labels, datasets: [{ label: 'Revenue', data: data.value.daily.values, backgroundColor: '#10b981', borderRadius: 8 }] }))
const barOpts = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false } }, y: { grid: { color: '#f1f5f9' }, ticks: { callback: (v) => '$' + v / 1000 + 'k' } } } }
const donutData = computed(() => ({ labels: data.value.channels.labels, datasets: [{ data: data.value.channels.values, backgroundColor: ['#059669', '#f59e0b'], borderWidth: 0 }] }))
const donutOpts = { responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'bottom' } } }
</script>

<template>
  <div>
    <PageHeader title="Store dashboard" subtitle="Sales, channels and what needs restocking">
      <RouterLink to="/" class="btn btn-secondary"><Store class="size-4" /> View store</RouterLink>
    </PageHeader>
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Revenue (recent orders)" :value="money(data.kpis.revenue)" :icon="DollarSign" :delta="9.8" hint="vs prior period" />
        <StatCard label="Orders" :value="data.kpis.orders" :icon="ShoppingCart" tone="sky" :hint="`AOV ${money(data.kpis.aov, 2)}`" />
        <StatCard label="Open quote requests" :value="data.kpis.open_quotes" :icon="FileText" tone="amber" hint="awaiting a reply" />
        <StatCard label="Low-stock products" :value="data.kpis.low_stock" :icon="AlertTriangle" tone="rose" hint="under 15 units" />
      </div>
      <div class="mt-6 grid gap-6 xl:grid-cols-3">
        <div class="card p-6 xl:col-span-2"><h3 class="font-bold">Revenue · last 14 days</h3><div class="mt-4 h-72"><Bar :data="barData" :options="barOpts" /></div></div>
        <div class="card p-6"><h3 class="font-bold">Orders by channel</h3><div class="mt-4 h-72"><Doughnut :data="donutData" :options="donutOpts" /></div></div>
      </div>
      <div class="card mt-6 p-6">
        <h3 class="font-bold">Top products</h3>
        <ul class="mt-4 space-y-3">
          <li v-for="(p, i) in data.top_products" :key="p.name" class="flex items-center gap-4 text-sm">
            <span class="w-5 font-bold text-slate-400">{{ i + 1 }}</span><span class="w-56 truncate font-medium">{{ p.name }}</span>
            <div class="h-2 flex-1 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-brand-500" :style="{ width: (p.qty / data.top_products[0].qty) * 100 + '%' }" /></div>
            <span class="w-14 text-right font-semibold">{{ p.qty }} sold</span>
          </li>
        </ul>
      </div>
    </template>
  </div>
</template>
