<script setup>
import { computed, ref } from 'vue'
import { CalendarDays, DollarSign, GraduationCap, Percent, UserPlus } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard from '@/components/ui/StatCard.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { money } from '@/core/format'
import { academyService } from '../academy.service'

const { data, error, reload } = useResource(academyService.overview)
const cohort = ref(0)
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const TONES = ['bg-brand-100 text-brand-800 border-brand-500', 'bg-emerald-100 text-emerald-800 border-emerald-500', 'bg-amber-100 text-amber-800 border-amber-500', 'bg-fuchsia-100 text-fuchsia-800 border-fuchsia-500']
const slotsFor = (day) => data.value.cohorts.flatMap((c, i) => c.sessions.filter((s) => s.day === day).map((s) => ({ ...s, cohort: c, tone: TONES[i % 4] }))).sort((a, b) => a.start.localeCompare(b.start))
const students = computed(() => data.value.students.filter((s) => !cohort.value || s.cohort_id === cohort.value))
const cohortName = (id) => data.value.cohorts.find((c) => c.id === id)?.name

async function mark(s, status) { const r = await act(() => academyService.attendance(s.id, status), `${s.name}: ${status}`); if (r) Object.assign(s, r) }
async function pay(s) { const r = await act(() => academyService.pay(s.id), `Payment recorded for ${s.name}`); if (r) reload() }

const showAdd = ref(false)
const form = ref({ name: '', email: '', cohort_id: 4 })
async function add() {
  if (await act(() => academyService.addStudent(form.value), `${form.value.name} enrolled`)) { showAdd.value = false; form.value = { name: '', email: '', cohort_id: 4 }; reload() }
}
</script>

<template>
  <div>
    <PageHeader title="Training centre administration" subtitle="Cohorts, weekly timetable, attendance and student fees">
      <button class="btn btn-primary" @click="showAdd = true"><UserPlus class="size-4" /> Enrol student</button>
    </PageHeader>
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Active students" :value="data.kpis.students" :icon="GraduationCap" :hint="`${data.kpis.cohorts} cohorts`" />
        <StatCard label="Fees collected" :value="money(data.kpis.revenue)" :icon="DollarSign" tone="emerald" />
        <StatCard label="Outstanding fees" :value="money(data.kpis.outstanding)" :icon="DollarSign" tone="rose" />
        <StatCard label="Avg. attendance" :value="data.kpis.attendance + '%'" :icon="Percent" tone="sky" />
      </div>

      <div class="card mt-6 p-6">
        <h3 class="flex items-center gap-2 font-bold"><CalendarDays class="size-5 text-brand-600" /> Weekly timetable</h3>
        <div class="mt-4 grid gap-3 md:grid-cols-3 xl:grid-cols-6">
          <div v-for="d in DAYS" :key="d" class="min-h-40 rounded-2xl bg-slate-50 p-3">
            <p class="mb-2 text-xs font-bold tracking-wide text-slate-500 uppercase">{{ d }}</p>
            <div v-for="s in slotsFor(d)" :key="s.cohort.id + s.start" class="mb-2 rounded-xl border-l-4 p-2.5 text-xs" :class="s.tone">
              <p class="font-bold">{{ s.start }}–{{ s.end }}</p><p class="mt-0.5 font-semibold">{{ s.cohort.name }}</p><p class="opacity-75">{{ s.cohort.room }} · {{ s.cohort.trainer }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <button v-for="c in data.cohorts" :key="c.id" class="card p-5 text-left transition" :class="cohort === c.id ? 'ring-2 ring-brand-500' : 'hover:shadow-md'" @click="cohort = cohort === c.id ? 0 : c.id">
          <p class="font-bold">{{ c.name }}</p><p class="text-sm text-slate-500">{{ c.trainer }} · {{ c.weeks }} weeks · {{ money(c.fee) }}</p>
          <div class="mt-3 flex justify-between text-sm"><span>{{ c.enrolled }}/{{ c.capacity }} seats</span><span class="font-semibold">{{ c.attendance }}% attendance</span></div>
          <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-brand-600" :style="{ width: (c.enrolled / c.capacity) * 100 + '%' }" /></div>
        </button>
      </div>

      <div class="card mt-6 overflow-x-auto">
        <table class="table-base">
          <thead><tr><th>Student</th><th>Cohort</th><th class="w-40">Attendance</th><th>Today</th><th class="text-right">Fees</th><th /></tr></thead>
          <tbody>
            <tr v-for="s in students" :key="s.id">
              <td><p class="font-semibold">{{ s.name }}</p><p class="text-xs text-slate-500">{{ s.email }}</p></td>
              <td class="text-slate-600">{{ cohortName(s.cohort_id) }}</td>
              <td><div class="flex items-center gap-2"><div class="h-1.5 flex-1 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full" :class="s.attendance >= 85 ? 'bg-emerald-500' : 'bg-amber-400'" :style="{ width: s.attendance + '%' }" /></div><span class="text-xs font-semibold">{{ s.attendance }}%</span></div></td>
              <td><div class="flex gap-1"><button v-for="st in [['present', 'P', 'btn-success'], ['late', 'L', 'btn-secondary'], ['absent', 'A', 'btn-danger']]" :key="st[0]" class="btn btn-sm !px-2.5" :class="st[2]" :title="st[0]" @click="mark(s, st[0])">{{ st[1] }}</button></div></td>
              <td class="text-right"><span :class="s.paid < s.fee ? 'font-semibold text-rose-600' : 'text-emerald-600'">{{ money(s.paid) }} / {{ money(s.fee) }}</span></td>
              <td class="text-right"><button v-if="s.paid < s.fee" class="btn btn-sm btn-secondary" @click="pay(s)">Record payment</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <Modal :open="showAdd" title="Enrol a student" @close="showAdd = false">
      <form class="space-y-4" @submit.prevent="add">
        <input v-model="form.name" required minlength="2" class="input" placeholder="Full name" />
        <input v-model="form.email" required type="email" class="input" placeholder="Email" />
        <select v-model.number="form.cohort_id" class="input"><option v-for="c in data?.cohorts" :key="c.id" :value="c.id">{{ c.name }} ({{ c.enrolled }}/{{ c.capacity }})</option></select>
        <div class="flex justify-end gap-2"><button type="button" class="btn btn-ghost" @click="showAdd = false">Cancel</button><button class="btn btn-primary">Enrol</button></div>
      </form>
    </Modal>
  </div>
</template>
