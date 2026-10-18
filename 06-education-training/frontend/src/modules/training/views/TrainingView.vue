<script setup>
import { computed, ref } from 'vue'
import { Bar } from 'vue-chartjs'
import { AlertTriangle, BellRing, BookOpen, Clock, Plus, ShieldCheck, Users } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard from '@/components/ui/StatCard.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date } from '@/core/format'
import { trainingService } from '../training.service'

const { data, error, reload } = useResource(trainingService.overview)
const { data: courses } = useResource(trainingService.courses)
const filter = ref('all')
const rows = computed(() => data.value.assignments.filter((a) => filter.value === 'all' || a.status === filter.value))

const bar = computed(() => ({
  labels: data.value.teams.map((t) => t.team),
  datasets: [{ label: 'Mandatory compliance %', data: data.value.teams.map((t) => t.compliance), borderRadius: 8,
    backgroundColor: data.value.teams.map((t) => (t.compliance >= 80 ? '#10b981' : t.compliance >= 60 ? '#f59e0b' : '#f43f5e')) }],
}))
const barOpts = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { max: 100, ticks: { callback: (v) => v + '%' }, grid: { color: '#f1f5f9' } }, x: { grid: { display: false } } } }

async function remind(a) { await act(() => trainingService.remind(a.id), `Reminder sent to ${a.employee}`) }
async function remindAllOverdue() {
  const overdue = data.value.assignments.filter((a) => a.status === 'overdue')
  await Promise.all(overdue.map((a) => trainingService.remind(a.id)))
  act(async () => true, `${overdue.length} reminders sent`)
}

const showAssign = ref(false)
const form = ref({ course_id: 3, team: 'Sales', due_in_days: 30 })
async function assign() {
  const r = await act(() => trainingService.assign(form.value))
  if (r) { act(async () => true, `${r.course} assigned to ${r.created} people${r.skipped ? ` (${r.skipped} already had it)` : ''}`); showAssign.value = false; reload() }
}
</script>

<template>
  <div>
    <PageHeader title="Employee training" subtitle="Northwind Co. · assign courses, track compliance and chase overdue training">
      <button class="btn btn-secondary" :disabled="!data" @click="remindAllOverdue"><BellRing class="size-4" /> Remind overdue</button>
      <button class="btn btn-primary" @click="showAssign = true"><Plus class="size-4" /> Assign training</button>
    </PageHeader>
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Mandatory compliance" :value="data.kpis.compliance + '%'" :icon="ShieldCheck" tone="emerald" hint="GDPR + Cyber Security" />
        <StatCard label="Overdue assignments" :value="data.kpis.overdue" :icon="AlertTriangle" tone="rose" />
        <StatCard label="Employees" :value="data.kpis.employees" :icon="Users" :hint="`${data.kpis.assignments} assignments`" />
        <StatCard label="Learning hours" :value="data.kpis.hours_learned + ' h'" :icon="Clock" tone="sky" hint="this quarter" />
      </div>
      <div class="mt-6 grid gap-6 xl:grid-cols-5">
        <div class="card p-6 xl:col-span-3"><h3 class="font-bold">Compliance by team</h3><div class="mt-4 h-64"><Bar :data="bar" :options="barOpts" /></div></div>
        <div class="card p-6 xl:col-span-2">
          <h3 class="font-bold">Teams at a glance</h3>
          <ul class="mt-4 space-y-3">
            <li v-for="t in data.teams" :key="t.team" class="flex items-center gap-3 text-sm">
              <span class="w-32 font-medium">{{ t.team }}</span>
              <div class="h-2 flex-1 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full" :class="t.compliance >= 80 ? 'bg-emerald-500' : t.compliance >= 60 ? 'bg-amber-400' : 'bg-rose-500'" :style="{ width: t.compliance + '%' }" /></div>
              <span class="w-10 text-right font-bold">{{ t.compliance }}%</span>
              <span v-if="t.overdue" class="rounded-full bg-rose-50 px-2 text-xs font-bold text-rose-600">{{ t.overdue }} late</span>
            </li>
          </ul>
        </div>
      </div>
      <div class="card mt-6 overflow-hidden">
        <div class="flex flex-wrap items-center gap-2 border-b border-slate-100 p-4">
          <div class="inline-flex rounded-xl bg-slate-100 p-1">
            <button v-for="s in [['all', 'All'], ['overdue', 'Overdue'], ['in_progress', 'In progress'], ['not_started', 'Not started'], ['completed', 'Completed']]" :key="s[0]" class="tab" :class="{ 'tab-active': filter === s[0] }" @click="filter = s[0]">{{ s[1] }}</button>
          </div>
        </div>
        <div class="max-h-[520px] overflow-auto">
          <table class="table-base">
            <thead class="sticky top-0"><tr><th>Employee</th><th>Course</th><th class="w-48">Progress</th><th>Due</th><th>Status</th><th /></tr></thead>
            <tbody>
              <tr v-for="a in rows" :key="a.id">
                <td><p class="font-semibold">{{ a.employee }}</p><p class="text-xs text-slate-500">{{ a.team }}</p></td>
                <td><p>{{ a.course }}</p><p v-if="a.mandatory" class="text-xs font-semibold text-rose-600">Mandatory</p></td>
                <td><div class="flex items-center gap-2"><div class="h-1.5 flex-1 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-brand-600" :style="{ width: a.progress + '%' }" /></div><span class="w-9 text-right text-xs font-semibold">{{ a.progress }}%</span></div></td>
                <td class="whitespace-nowrap" :class="a.status === 'overdue' ? 'font-semibold text-rose-600' : 'text-slate-500'">{{ date(a.due) }}</td>
                <td><StatusBadge :status="a.status" /></td>
                <td class="text-right"><button v-if="a.status !== 'completed'" class="btn btn-sm btn-ghost" @click="remind(a)"><BellRing class="size-3.5" /></button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <Modal :open="showAssign" title="Assign training" subtitle="Employees get an email and the course appears in their learning" @close="showAssign = false">
      <form class="space-y-4" @submit.prevent="assign">
        <div><label class="label">Course</label><select v-model.number="form.course_id" class="input"><option v-for="c in courses" :key="c.id" :value="c.id">{{ c.title }}</option></select></div>
        <div><label class="label">Team</label><select v-model="form.team" class="input"><option v-for="t in data?.teams" :key="t.team" :value="t.team">{{ t.team }} ({{ t.people }} people)</option></select></div>
        <div><label class="label">Due in</label><select v-model.number="form.due_in_days" class="input"><option :value="14">2 weeks</option><option :value="30">30 days</option><option :value="60">60 days</option><option :value="90">90 days</option></select></div>
        <div class="flex justify-end gap-2"><button type="button" class="btn btn-ghost" @click="showAssign = false">Cancel</button><button class="btn btn-primary"><BookOpen class="size-4" /> Assign</button></div>
      </form>
    </Modal>
  </div>
</template>
