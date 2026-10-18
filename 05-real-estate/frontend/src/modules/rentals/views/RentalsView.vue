<script setup>
import { computed, ref } from 'vue'
import { AlertTriangle, Building, PoundSterling, Plus, Wrench } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard from '@/components/ui/StatCard.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date, humanize, money } from '@/core/format'
import { rentalsService } from '../rentals.service'

const { data, error, reload } = useResource(rentalsService.overview)
const tab = ref('units')
const latestMonth = computed(() => data.value?.payments[0]?.month)
const current = computed(() => data.value?.payments.filter((p) => p.month === latestMonth.value) ?? [])
const PRIORITY = { urgent: 'urgent', medium: 'pending', low: 'draft' }

async function markPaid(p) { const r = await act(() => rentalsService.markPaid(p.id), `Rent recorded for ${p.tenant}`); if (r) reload() }
async function setTicket(t, s) { const r = await act(() => rentalsService.setTicket(t.id, s), 'Ticket updated'); if (r) Object.assign(t, r) }

const showTicket = ref(false)
const ticket = ref({ unit_id: 1, title: '', priority: 'medium' })
async function createTicket() {
  if (await act(() => rentalsService.openTicket(ticket.value), 'Maintenance ticket opened')) { showTicket.value = false; ticket.value.title = ''; reload(); tab.value = 'maintenance' }
}
</script>

<template>
  <div>
    <PageHeader title="Rental management" subtitle="Units, rent collection and maintenance for managed landlords">
      <button class="btn btn-primary" @click="showTicket = true"><Plus class="size-4" /> Maintenance ticket</button>
    </PageHeader>
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Occupancy" :value="data.kpis.occupancy + '%'" :icon="Building" :hint="`${data.kpis.units} managed units`" />
        <StatCard label="Monthly rent roll" :value="money(data.kpis.monthly_rent)" :icon="PoundSterling" tone="emerald" />
        <StatCard label="Collected this month" :value="money(data.kpis.collected)" :icon="PoundSterling" tone="sky" :hint="`arrears ${money(data.kpis.arrears)}`" />
        <StatCard label="Open maintenance" :value="data.kpis.open_tickets" :icon="Wrench" tone="amber" />
      </div>

      <div class="mt-6 inline-flex rounded-xl bg-slate-200/60 p-1">
        <button v-for="t in ['units', 'rent', 'maintenance']" :key="t" class="tab capitalize" :class="{ 'tab-active': tab === t }" @click="tab = t">{{ t === 'rent' ? 'Rent ledger' : t }}</button>
      </div>

      <div v-if="tab === 'units'" class="card mt-4 overflow-x-auto">
        <table class="table-base">
          <thead><tr><th>Unit</th><th>Tenant</th><th class="text-right">Rent</th><th>Lease ends</th><th class="text-right">Deposit</th><th>Status</th></tr></thead>
          <tbody>
            <tr v-for="u in data.units" :key="u.id">
              <td class="font-semibold">{{ u.address }}</td><td>{{ u.tenant ?? '—' }}</td><td class="text-right">{{ money(u.rent) }}</td>
              <td :class="u.lease_end && u.lease_end < new Date(Date.now() + 60 * 864e5).toISOString().slice(0, 10) ? 'font-semibold text-amber-600' : 'text-slate-500'">{{ date(u.lease_end) }}</td>
              <td class="text-right text-slate-500">{{ u.deposit ? money(u.deposit) : '—' }}</td><td><StatusBadge :status="u.status" /></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="tab === 'rent'" class="card mt-4 overflow-x-auto">
        <div v-if="current.some((p) => p.status === 'late')" class="flex items-center gap-2 border-b border-rose-100 bg-rose-50 px-5 py-3 text-sm text-rose-700"><AlertTriangle class="size-4" /> Late payments this month — automatic reminders have been sent.</div>
        <table class="table-base">
          <thead><tr><th>Month</th><th>Unit</th><th>Tenant</th><th class="text-right">Amount</th><th>Status</th><th /></tr></thead>
          <tbody>
            <tr v-for="p in data.payments" :key="p.id">
              <td class="font-mono text-xs">{{ p.month }}</td><td class="max-w-64 truncate">{{ p.address }}</td><td>{{ p.tenant }}</td>
              <td class="text-right font-semibold">{{ money(p.amount) }}</td><td><StatusBadge :status="p.status === 'late' ? 'overdue' : p.status" :label="humanize(p.status)" /></td>
              <td class="text-right"><button v-if="p.status !== 'paid'" class="btn btn-sm btn-success" @click="markPaid(p)">Record payment</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="mt-4 grid gap-4 md:grid-cols-2">
        <div v-for="t in data.tickets" :key="t.id" class="card p-5">
          <div class="flex items-start justify-between gap-2"><p class="font-bold">{{ t.title }}</p><StatusBadge :status="PRIORITY[t.priority]" :label="humanize(t.priority)" /></div>
          <p class="mt-1 text-sm text-slate-500">{{ t.address }}</p>
          <p class="mt-3 text-xs text-slate-400">Opened {{ date(t.created) }}{{ t.contractor ? ` · ${t.contractor}` : '' }}</p>
          <div class="mt-4 flex items-center gap-2 border-t border-slate-100 pt-3">
            <StatusBadge :status="t.status" />
            <button v-if="t.status === 'open'" class="btn btn-sm btn-secondary ml-auto" @click="setTicket(t, 'in_progress')">Assign contractor</button>
            <button v-if="t.status === 'in_progress'" class="btn btn-sm btn-success ml-auto" @click="setTicket(t, 'completed')">Mark completed</button>
          </div>
        </div>
      </div>
    </template>

    <Modal :open="showTicket" title="New maintenance ticket" @close="showTicket = false">
      <form class="space-y-4" @submit.prevent="createTicket">
        <div><label class="label">Unit</label><select v-model.number="ticket.unit_id" class="input"><option v-for="u in data?.units" :key="u.id" :value="u.id">{{ u.address }}</option></select></div>
        <div><label class="label">Issue</label><input v-model="ticket.title" required minlength="3" class="input" placeholder="e.g. Leaking shower" /></div>
        <div><label class="label">Priority</label><select v-model="ticket.priority" class="input"><option value="low">Low</option><option value="medium">Medium</option><option value="urgent">Urgent</option></select></div>
        <div class="flex justify-end gap-2"><button type="button" class="btn btn-ghost" @click="showTicket = false">Cancel</button><button class="btn btn-primary">Open ticket</button></div>
      </form>
    </Modal>
  </div>
</template>
