<script setup>
import { computed } from 'vue'
import { Line, Doughnut } from 'vue-chartjs'
import { AlertTriangle, Boxes, Clock, DollarSign, FileCheck, Receipt, ShieldAlert, Truck, Users, Wallet, Wrench } from 'lucide-vue-next'
import StatCard from '@/components/ui/StatCard.vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { useResource } from '@/core/resource'
import { money } from '@/core/format'
import { dashboardService } from '../dashboard.service'

const { data, error, reload } = useResource(dashboardService.overview)
const today = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })

const lineData = computed(() => ({
  labels: data.value.revenue_series.labels,
  datasets: [
    { label: 'Revenue', data: data.value.revenue_series.revenue, borderColor: '#4f46e5', backgroundColor: 'rgba(79,70,229,.12)', fill: true, tension: 0.4, pointRadius: 0, borderWidth: 2.5 },
    { label: 'Expenses', data: data.value.revenue_series.expenses, borderColor: '#f59e0b', backgroundColor: 'transparent', tension: 0.4, pointRadius: 0, borderWidth: 2, borderDash: [6, 4] },
  ],
}))
const lineOptions = {
  responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
  plugins: { legend: { position: 'top', align: 'end', labels: { usePointStyle: true, boxWidth: 8 } } },
  scales: { x: { grid: { display: false } }, y: { grid: { color: '#f1f5f9' }, ticks: { callback: (v) => '$' + v / 1000 + 'k' } } },
}
const donutData = computed(() => ({
  labels: data.value.expense_breakdown.labels,
  datasets: [{ data: data.value.expense_breakdown.values, backgroundColor: ['#4f46e5', '#818cf8', '#f59e0b', '#10b981', '#f43f5e'], borderWidth: 0, hoverOffset: 6 }],
}))
const donutOptions = { responsive: true, maintainAspectRatio: false, cutout: '72%', plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, boxWidth: 8, padding: 14 } } } }

const alertIcon = { stock: Boxes, invoice: Receipt, service: Wrench, insurance: ShieldAlert }
const shortcuts = [
  { to: '/app/invoices', label: 'New invoice', icon: Receipt, tone: 'bg-brand-50 text-brand-600' },
  { to: '/app/purchasing', label: 'Reorder stock', icon: Boxes, tone: 'bg-emerald-50 text-emerald-600' },
  { to: '/app/hr', label: 'Run payroll', icon: Users, tone: 'bg-amber-50 text-amber-600' },
  { to: '/app/fleet', label: 'Log service', icon: Truck, tone: 'bg-sky-50 text-sky-600' },
  { to: '/app/documents', label: 'Approvals', icon: FileCheck, tone: 'bg-rose-50 text-rose-600' },
]
</script>

<template>
  <div>
    <PageHeader title="Good morning, Amira 👋" :subtitle="`${today} · here's what needs your attention`">
      <RouterLink to="/app/invoices" class="btn btn-primary"><Receipt class="size-4" /> Create invoice</RouterLink>
    </PageHeader>

    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Revenue this month" :value="money(data.kpis.revenue)" :icon="DollarSign" :delta="data.kpis.revenue_delta" hint="vs last month" />
        <StatCard label="Outstanding invoices" :value="money(data.kpis.outstanding)" :icon="Wallet" tone="amber" hint="pending + overdue" />
        <StatCard label="Stock value" :value="money(data.kpis.stock_value)" :icon="Boxes" tone="emerald" :hint="`${data.kpis.low_stock} items below reorder level`" />
        <StatCard label="Pending approvals" :value="data.kpis.pending_approvals" :icon="Clock" tone="rose" hint="leave, POs & documents" />
      </div>

      <div class="mt-6 grid gap-6 xl:grid-cols-3">
        <div class="card p-6 xl:col-span-2">
          <h3 class="font-bold text-slate-900">Revenue vs expenses</h3>
          <p class="text-sm text-slate-500">Last 12 months</p>
          <div class="mt-4 h-72"><Line :data="lineData" :options="lineOptions" /></div>
        </div>
        <div class="card p-6">
          <h3 class="font-bold text-slate-900">Where money goes</h3>
          <p class="text-sm text-slate-500">Expense share, this quarter</p>
          <div class="mt-4 h-72"><Doughnut :data="donutData" :options="donutOptions" /></div>
        </div>
      </div>

      <div class="mt-6 grid gap-6 xl:grid-cols-3">
        <div class="card p-6 xl:col-span-2">
          <div class="flex items-center gap-2"><AlertTriangle class="size-5 text-amber-500" /><h3 class="font-bold text-slate-900">Needs attention</h3>
            <span class="rounded-full bg-amber-100 px-2 text-xs font-bold text-amber-700">{{ data.alerts.length }}</span></div>
          <ul class="mt-4 divide-y divide-slate-100">
            <li v-for="(a, i) in data.alerts" :key="i" class="flex items-center gap-3 py-3 text-sm">
              <span class="grid size-9 place-items-center rounded-xl bg-slate-100 text-slate-600"><component :is="alertIcon[a.type]" class="size-4" /></span>
              <span class="flex-1 text-slate-700">{{ a.message }}</span>
              <span class="text-xs font-semibold text-slate-400 uppercase">{{ a.type }}</span>
            </li>
          </ul>
        </div>
        <div class="card p-6">
          <h3 class="font-bold text-slate-900">Quick actions</h3>
          <div class="mt-4 grid grid-cols-2 gap-3">
            <RouterLink v-for="s in shortcuts" :key="s.to" :to="s.to" class="flex flex-col items-start gap-3 rounded-2xl border border-slate-100 p-4 transition hover:border-brand-200 hover:bg-brand-50/40">
              <span class="grid size-9 place-items-center rounded-xl" :class="s.tone"><component :is="s.icon" class="size-4" /></span>
              <span class="text-sm font-semibold text-slate-700">{{ s.label }}</span>
            </RouterLink>
          </div>
          <p class="mt-4 text-xs text-slate-500">{{ data.kpis.employees }} employees · synced just now</p>
        </div>
      </div>
    </template>
  </div>
</template>
