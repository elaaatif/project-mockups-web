<script setup>
import { computed, ref } from 'vue'
import { Banknote, CalendarPlus, Check, Mail, Play, X } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { avatarGradient, date, initials, money } from '@/core/format'
import { hrService } from '../hr.service'

const tab = ref('employees')
const { data: employees, error, reload } = useResource(hrService.employees)
const { data: leaveData, reload: reloadLeaves } = useResource(hrService.leaves)
const { data: runs, reload: reloadRuns } = useResource(hrService.payrollRuns, [])

const pendingCount = computed(() => leaveData.value?.leaves.filter((l) => l.status === 'pending').length ?? 0)

async function decide(leave, status) {
  if (await act(() => hrService.decideLeave(leave.id, status), `Leave ${status} for ${leave.name}`)) {
    reloadLeaves(); reload()
  }
}

const showLeave = ref(false)
const leaveForm = ref({ employee_id: '', type: 'Annual', start: '', end: '', reason: '' })
async function submitLeave() {
  if (await act(() => hrService.requestLeave(leaveForm.value), 'Leave request submitted')) {
    showLeave.value = false; reloadLeaves(); tab.value = 'leave'
  }
}

const month = ref(new Date().toISOString().slice(0, 7))
const running = ref(false)
async function runPayroll() {
  running.value = true
  await new Promise((r) => setTimeout(r, 700)) // let the progress state be visible
  if (await act(() => hrService.runPayroll(month.value), `Payroll for ${month.value} processed`)) reloadRuns()
  running.value = false
}
const latest = computed(() => runs.value?.[0])
</script>

<template>
  <div>
    <PageHeader title="People & Payroll" subtitle="Employee records, leave approvals and monthly payroll in one flow">
      <button class="btn btn-secondary" @click="showLeave = true"><CalendarPlus class="size-4" /> Request leave</button>
    </PageHeader>

    <div class="mb-6 inline-flex rounded-xl bg-slate-200/60 p-1">
      <button class="tab" :class="{ 'tab-active': tab === 'employees' }" @click="tab = 'employees'">Employees</button>
      <button class="tab" :class="{ 'tab-active': tab === 'leave' }" @click="tab = 'leave'">Leave requests <span v-if="pendingCount" class="ml-1 rounded-full bg-amber-400 px-1.5 text-[11px] text-white">{{ pendingCount }}</span></button>
      <button class="tab" :class="{ 'tab-active': tab === 'payroll' }" @click="tab = 'payroll'">Payroll</button>
    </div>

    <LoadingState v-if="!employees" :error="error" @retry="reload" />

    <!-- Employees -->
    <div v-else-if="tab === 'employees'" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      <div v-for="e in employees" :key="e.id" class="card p-5 transition hover:shadow-md">
        <div class="flex items-center gap-4">
          <span class="grid size-12 place-items-center rounded-2xl bg-gradient-to-br text-sm font-bold text-white" :class="avatarGradient(e.name)">{{ initials(e.name) }}</span>
          <div class="min-w-0 flex-1"><p class="truncate font-bold text-slate-900">{{ e.name }}</p><p class="truncate text-sm text-slate-500">{{ e.role }}</p></div>
          <StatusBadge :status="e.status" />
        </div>
        <div class="mt-5 grid grid-cols-3 gap-2 rounded-xl bg-slate-50 p-3 text-center text-xs">
          <div><p class="text-slate-500">Dept</p><p class="mt-0.5 font-semibold text-slate-800">{{ e.department }}</p></div>
          <div><p class="text-slate-500">Salary</p><p class="mt-0.5 font-semibold text-slate-800">{{ money(e.salary) }}</p></div>
          <div><p class="text-slate-500">Leave left</p><p class="mt-0.5 font-semibold text-slate-800">{{ e.leave_balance }} days</p></div>
        </div>
        <p class="mt-3 flex items-center gap-1.5 text-xs text-slate-500"><Mail class="size-3.5" /> {{ e.email }} · joined {{ date(e.joined) }}</p>
      </div>
    </div>

    <!-- Leave -->
    <div v-else-if="tab === 'leave'" class="card overflow-x-auto">
      <table class="table-base">
        <thead><tr><th>Employee</th><th>Type</th><th>Dates</th><th>Days</th><th>Reason</th><th>Status</th><th class="text-right">Decision</th></tr></thead>
        <tbody>
          <tr v-for="l in leaveData?.leaves" :key="l.id">
            <td class="font-semibold">{{ l.name }}</td>
            <td>{{ l.type }}</td>
            <td class="text-slate-500">{{ date(l.start) }} → {{ date(l.end) }}</td>
            <td>{{ l.days }}</td>
            <td class="text-slate-500">{{ l.reason }}</td>
            <td><StatusBadge :status="l.status" /></td>
            <td>
              <div v-if="l.status === 'pending'" class="flex justify-end gap-1">
                <button class="btn btn-sm btn-success" @click="decide(l, 'approved')"><Check class="size-3.5" /> Approve</button>
                <button class="btn btn-sm btn-danger" @click="decide(l, 'rejected')"><X class="size-3.5" /> Reject</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Payroll -->
    <div v-else class="space-y-6">
      <div class="card flex flex-wrap items-end gap-4 p-6">
        <div><label class="label">Pay period</label><input v-model="month" type="month" class="input" /></div>
        <button class="btn btn-primary" :disabled="running" @click="runPayroll">
          <Play v-if="!running" class="size-4" /><span v-else class="size-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
          {{ running ? 'Calculating…' : `Run payroll for ${employees.length} employees` }}
        </button>
        <p class="text-sm text-slate-500">Gross → progressive income tax → 7% social security → net pay</p>
      </div>
      <div v-if="latest" class="card overflow-hidden">
        <div class="grid gap-4 border-b border-slate-100 p-6 sm:grid-cols-4">
          <div v-for="k in ['gross', 'tax', 'social', 'net']" :key="k">
            <p class="text-xs font-semibold text-slate-500 uppercase">{{ k === 'social' ? 'Social security' : k }}</p>
            <p class="mt-1 text-2xl font-extrabold" :class="k === 'net' ? 'text-emerald-600' : 'text-slate-900'">{{ money(latest.totals[k]) }}</p>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="table-base">
            <thead><tr><th>Employee</th><th class="text-right">Gross</th><th class="text-right">Income tax</th><th class="text-right">Social</th><th class="text-right">Net pay</th></tr></thead>
            <tbody>
              <tr v-for="s in latest.slips" :key="s.employee">
                <td><p class="font-semibold">{{ s.employee }}</p><p class="text-xs text-slate-500">{{ s.role }}</p></td>
                <td class="text-right tabular-nums">{{ money(s.gross, 2) }}</td>
                <td class="text-right text-rose-600 tabular-nums">-{{ money(s.tax, 2) }}</td>
                <td class="text-right text-rose-600 tabular-nums">-{{ money(s.social, 2) }}</td>
                <td class="text-right font-bold tabular-nums">{{ money(s.net, 2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else class="card grid place-items-center gap-2 p-14 text-center">
        <Banknote class="size-10 text-slate-300" />
        <p class="font-semibold">No payroll runs yet</p>
        <p class="text-sm text-slate-500">Choose a period and run payroll to generate payslips.</p>
      </div>
    </div>

    <Modal :open="showLeave" title="Request leave" @close="showLeave = false">
      <form class="grid grid-cols-2 gap-4" @submit.prevent="submitLeave">
        <div class="col-span-2"><label class="label">Employee</label>
          <select v-model.number="leaveForm.employee_id" required class="input"><option value="" disabled>Select employee</option><option v-for="e in employees" :key="e.id" :value="e.id">{{ e.name }}</option></select></div>
        <div class="col-span-2"><label class="label">Leave type</label><select v-model="leaveForm.type" class="input"><option v-for="t in leaveData?.types" :key="t">{{ t }}</option></select></div>
        <div><label class="label">From</label><input v-model="leaveForm.start" type="date" required class="input" /></div>
        <div><label class="label">To</label><input v-model="leaveForm.end" type="date" required class="input" /></div>
        <div class="col-span-2"><label class="label">Reason</label><textarea v-model="leaveForm.reason" rows="2" class="input" /></div>
        <div class="col-span-2 flex justify-end gap-2"><button type="button" class="btn btn-ghost" @click="showLeave = false">Cancel</button><button class="btn btn-primary">Submit request</button></div>
      </form>
    </Modal>
  </div>
</template>
