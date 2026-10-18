<script setup>
import { computed, ref } from 'vue'
import { Bar, Line } from 'vue-chartjs'
import { CalendarClock, Hash, Headphones, Landmark, Mail, MessageCircle, Play, Printer, Sparkles, Trash2, TrendingDown, TrendingUp } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import { act, useResource } from '@/core/resource'
import { reportsService } from '../reports.service'

const ICONS = { TrendingUp, Headphones, Landmark }
const CHANNEL_ICONS = { email: Mail, whatsapp: MessageCircle, slack: Hash }

const { data: templates } = useResource(reportsService.templates)
const { data: schedules, reload: reloadSchedules } = useResource(reportsService.schedules, [])
const templateId = ref('sales')
const period = ref('30d')
const loading = ref(false)
const report = ref(null)

async function generate() {
  loading.value = true
  const [r] = await Promise.all([act(() => reportsService.generate(templateId.value, period.value)), new Promise((res) => setTimeout(res, 900))])
  report.value = r
  loading.value = false
}
generate()

const lineData = computed(() => ({
  labels: report.value.series.labels,
  datasets: [
    { label: 'This period', data: report.value.series.current, borderColor: '#7c3aed', backgroundColor: 'rgba(124,58,237,.1)', fill: true, tension: 0.4, pointRadius: 0, borderWidth: 2.5 },
    { label: 'Previous period', data: report.value.series.previous, borderColor: '#cbd5e1', tension: 0.4, pointRadius: 0, borderWidth: 2, borderDash: [5, 5] },
  ],
}))
const barData = computed(() => ({
  labels: report.value.breakdown.labels,
  datasets: [{ data: report.value.breakdown.values, backgroundColor: ['#7c3aed', '#a78bfa', '#c4b5fd', '#ddd6fe'], borderRadius: 8 }],
}))
const chartOpts = { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top', align: 'end', labels: { usePointStyle: true, boxWidth: 8 } } }, scales: { x: { grid: { display: false } }, y: { grid: { color: '#f1f5f9' } } } }
const barOpts = { ...chartOpts, indexAxis: 'y', plugins: { legend: { display: false } } }

const form = ref({ frequency: 'weekly', channel: 'email', recipient: '' })
async function schedule() {
  if (await act(() => reportsService.schedule({ template_id: templateId.value, ...form.value }), 'Report scheduled')) {
    form.value.recipient = ''
    reloadSchedules()
  }
}
async function remove(s) {
  await act(() => reportsService.unschedule(s.id), 'Schedule removed')
  reloadSchedules()
}
const print = () => window.print()
</script>

<template>
  <div>
    <PageHeader title="Automated reporting" subtitle="Generate a report on demand or schedule it for email, Slack or WhatsApp">
      <button v-if="report" class="btn btn-secondary" @click="print"><Printer class="size-4" /> Export PDF</button>
    </PageHeader>

    <div class="grid gap-4 md:grid-cols-3">
      <button v-for="t in templates" :key="t.id" class="card flex items-start gap-4 p-5 text-left transition" :class="templateId === t.id ? 'ring-2 ring-brand-500' : 'hover:shadow-md'" @click="templateId = t.id; generate()">
        <span class="grid size-11 shrink-0 place-items-center rounded-xl" :class="templateId === t.id ? 'bg-brand-600 text-white' : 'bg-brand-50 text-brand-600'"><component :is="ICONS[t.icon]" class="size-5" /></span>
        <div><p class="font-bold">{{ t.name }}</p><p class="text-sm text-slate-500">{{ t.description }}</p></div>
      </button>
    </div>

    <div class="mt-6 flex flex-wrap items-center gap-3">
      <div class="inline-flex rounded-xl bg-slate-200/60 p-1">
        <button v-for="p in [['7d', 'Last 7 days'], ['30d', 'Last 30 days'], ['90d', 'Last quarter']]" :key="p[0]" class="tab" :class="{ 'tab-active': period === p[0] }" @click="period = p[0]; generate()">{{ p[1] }}</button>
      </div>
      <button class="btn btn-primary" :disabled="loading" @click="generate"><Play class="size-4" /> {{ loading ? 'Generating…' : 'Regenerate' }}</button>
    </div>

    <div v-if="loading || !report" class="mt-6 grid gap-4 md:grid-cols-4"><div v-for="i in 4" :key="i" class="h-28 animate-pulse rounded-2xl bg-slate-200/60" /><div class="h-80 animate-pulse rounded-2xl bg-slate-200/60 md:col-span-4" /></div>
    <template v-else>
      <div class="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <div v-for="k in report.kpis" :key="k.label" class="card p-5">
          <p class="text-sm text-slate-500">{{ k.label }}</p>
          <p class="mt-2 text-2xl font-extrabold">{{ k.value }}</p>
          <p class="mt-1 inline-flex items-center gap-1 text-xs font-semibold" :class="k.delta >= 0 ? 'text-emerald-600' : 'text-rose-600'">
            <component :is="k.delta >= 0 ? TrendingUp : TrendingDown" class="size-3.5" />{{ Math.abs(k.delta) }}% vs previous
          </p>
        </div>
      </div>
      <div class="mt-6 grid gap-6 xl:grid-cols-3">
        <div class="card p-6 xl:col-span-2"><h3 class="font-bold">{{ report.title }} — trend</h3><div class="mt-4 h-72"><Line :data="lineData" :options="chartOpts" /></div></div>
        <div class="card p-6"><h3 class="font-bold">Breakdown</h3><div class="mt-4 h-72"><Bar :data="barData" :options="barOpts" /></div></div>
      </div>
      <div class="mt-6 rounded-3xl border border-brand-100 bg-gradient-to-br from-brand-50 via-white to-fuchsia-50 p-6">
        <p class="flex items-center gap-2 font-bold text-brand-700"><Sparkles class="size-5" /> AI summary <span class="text-xs font-normal text-slate-400">· generated {{ report.generated_at }}</span></p>
        <ul class="mt-4 space-y-2.5">
          <li v-for="(n, i) in report.narrative" :key="i" class="flex gap-3 text-slate-700"><span class="mt-2 size-1.5 shrink-0 rounded-full bg-brand-500" />{{ n }}</li>
        </ul>
      </div>
    </template>

    <div class="card mt-6 overflow-hidden">
      <div class="flex items-center gap-2 border-b border-slate-100 px-6 py-4"><CalendarClock class="size-5 text-brand-600" /><h3 class="font-bold">Scheduled deliveries</h3></div>
      <form class="flex flex-wrap gap-3 border-b border-slate-100 bg-slate-50/60 px-6 py-4" @submit.prevent="schedule">
        <select v-model="form.frequency" class="input !w-auto"><option value="daily">Daily</option><option value="weekly">Weekly</option><option value="monthly">Monthly</option></select>
        <select v-model="form.channel" class="input !w-auto"><option value="email">Email</option><option value="slack">Slack</option><option value="whatsapp">WhatsApp</option></select>
        <input v-model="form.recipient" required class="input min-w-56 flex-1" :placeholder="form.channel === 'email' ? 'team@company.com' : form.channel === 'slack' ? '#channel' : '+44 7700 900000'" />
        <button class="btn btn-primary">Schedule “{{ templates?.find((t) => t.id === templateId)?.name }}”</button>
      </form>
      <table class="table-base">
        <thead><tr><th>Report</th><th>Frequency</th><th>Channel</th><th>Recipient</th><th>Next run</th><th /></tr></thead>
        <tbody>
          <tr v-for="s in schedules" :key="s.id">
            <td class="font-semibold">{{ s.template }}</td><td class="capitalize">{{ s.frequency }}</td>
            <td><span class="inline-flex items-center gap-1.5 capitalize"><component :is="CHANNEL_ICONS[s.channel]" class="size-4 text-brand-600" />{{ s.channel }}</span></td>
            <td class="font-mono text-xs">{{ s.recipient }}</td><td class="text-slate-500">{{ s.next_run }}</td>
            <td class="text-right"><button class="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600" @click="remove(s)"><Trash2 class="size-4" /></button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
