<script setup>
import { computed, ref } from 'vue'
import { AlertCircle, CheckCircle2, Clock, Plus, Printer, Trash2, Workflow } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard from '@/components/ui/StatCard.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date, money } from '@/core/format'
import { invoicesService } from '../invoices.service'

const { data, error, reload } = useResource(invoicesService.list)
const tab = ref('all')
const tabs = ['all', 'pending', 'overdue', 'paid']
const rows = computed(() => (tab.value === 'all' ? data.value.invoices : data.value.invoices.filter((i) => i.status === tab.value)))

// Preview
const selected = ref(null)
const print = () => window.print()
async function markPaid(inv) {
  const updated = await act(() => invoicesService.markPaid(inv.id), `${inv.id} marked as paid`)
  if (updated) { selected.value = updated; reload() }
}

// Create
const showNew = ref(false)
const blank = () => ({ client: '', due_in_days: 30, tax_rate: 0.1, lines: [{ description: '', qty: 1, price: 0 }] })
const form = ref(blank())
const subtotal = computed(() => form.value.lines.reduce((s, l) => s + l.qty * l.price, 0))
async function create() {
  const inv = await act(() => invoicesService.create(form.value), 'Invoice created and sent')
  if (inv) { showNew.value = false; form.value = blank(); reload(); selected.value = inv }
}
</script>

<template>
  <div>
    <PageHeader title="Invoicing" subtitle="Bill clients, track payments and follow up on overdue balances">
      <button class="btn btn-primary" @click="showNew = true"><Plus class="size-4" /> New invoice</button>
    </PageHeader>

    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-3">
        <StatCard label="Collected" :value="money(data.summary.paid)" :icon="CheckCircle2" tone="emerald" hint="paid invoices" />
        <StatCard label="Awaiting payment" :value="money(data.summary.pending)" :icon="Clock" tone="amber" hint="not yet due" />
        <StatCard label="Overdue" :value="money(data.summary.overdue)" :icon="AlertCircle" tone="rose" hint="reminders scheduled" />
      </div>

      <div class="card mt-6 overflow-hidden">
        <div class="border-b border-slate-100 p-4">
          <div class="inline-flex rounded-xl bg-slate-100 p-1">
            <button v-for="t in tabs" :key="t" class="tab capitalize" :class="{ 'tab-active': tab === t }" @click="tab = t">{{ t }}</button>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="table-base">
            <thead><tr><th>Invoice</th><th>Client</th><th>Issued</th><th>Due</th><th class="text-right">Amount</th><th>Status</th><th /></tr></thead>
            <tbody>
              <tr v-for="inv in rows" :key="inv.id" class="cursor-pointer hover:bg-slate-50/60" @click="selected = inv">
                <td class="font-semibold text-brand-700">{{ inv.id }}</td>
                <td class="font-medium">{{ inv.client }}</td>
                <td class="text-slate-500">{{ date(inv.issue_date) }}</td>
                <td class="text-slate-500">{{ date(inv.due_date) }}</td>
                <td class="text-right font-semibold tabular-nums">{{ money(inv.total, 2) }}</td>
                <td><StatusBadge :status="inv.status" /></td>
                <td class="text-right"><button v-if="inv.status !== 'paid'" class="btn btn-sm btn-success" @click.stop="markPaid(inv)">Mark paid</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- Invoice preview -->
    <Modal :open="!!selected" :title="selected?.id" subtitle="Invoice preview" wide @close="selected = null">
      <div v-if="selected" class="rounded-2xl border border-slate-200 p-8">
        <div class="flex items-start justify-between">
          <div class="flex items-center gap-2 text-lg font-extrabold"><span class="grid size-9 place-items-center rounded-xl bg-brand-600 text-white"><Workflow class="size-5" /></span> Northstar Ltd</div>
          <StatusBadge :status="selected.status" />
        </div>
        <div class="mt-8 grid grid-cols-3 gap-6 text-sm">
          <div><p class="label">Billed to</p><p class="font-semibold">{{ selected.client }}</p></div>
          <div><p class="label">Issued</p><p>{{ date(selected.issue_date) }}</p></div>
          <div><p class="label">Due</p><p>{{ date(selected.due_date) }}</p></div>
        </div>
        <table class="table-base mt-8">
          <thead><tr><th>Description</th><th class="text-right">Qty</th><th class="text-right">Price</th><th class="text-right">Total</th></tr></thead>
          <tbody>
            <tr v-for="(l, i) in selected.lines" :key="i"><td>{{ l.description }}</td><td class="text-right">{{ l.qty }}</td><td class="text-right">{{ money(l.price, 2) }}</td><td class="text-right font-semibold">{{ money(l.qty * l.price, 2) }}</td></tr>
          </tbody>
        </table>
        <div class="mt-6 ml-auto max-w-xs space-y-2 text-sm">
          <div class="flex justify-between text-slate-500"><span>Subtotal</span><span>{{ money(selected.subtotal, 2) }}</span></div>
          <div class="flex justify-between text-slate-500"><span>Tax</span><span>{{ money(selected.tax, 2) }}</span></div>
          <div class="flex justify-between border-t border-slate-200 pt-2 text-lg font-extrabold"><span>Total</span><span>{{ money(selected.total, 2) }}</span></div>
        </div>
      </div>
      <div class="mt-5 flex justify-end gap-2">
        <button class="btn btn-secondary" @click="print"><Printer class="size-4" /> Print</button>
        <button v-if="selected?.status !== 'paid'" class="btn btn-primary" @click="markPaid(selected)"><CheckCircle2 class="size-4" /> Record payment</button>
      </div>
    </Modal>

    <!-- New invoice -->
    <Modal :open="showNew" title="New invoice" subtitle="Line items are totalled automatically" wide @close="showNew = false">
      <form class="space-y-5" @submit.prevent="create">
        <div class="grid gap-4 sm:grid-cols-3">
          <div><label class="label">Client</label><select v-model="form.client" required class="input"><option value="" disabled>Select client</option><option v-for="c in data?.clients" :key="c">{{ c }}</option></select></div>
          <div><label class="label">Payment terms</label><select v-model.number="form.due_in_days" class="input"><option :value="7">Net 7</option><option :value="14">Net 14</option><option :value="30">Net 30</option><option :value="60">Net 60</option></select></div>
          <div><label class="label">Tax rate</label><select v-model.number="form.tax_rate" class="input"><option :value="0">0%</option><option :value="0.05">5%</option><option :value="0.1">10%</option><option :value="0.2">20%</option></select></div>
        </div>
        <div>
          <label class="label">Line items</label>
          <div v-for="(l, i) in form.lines" :key="i" class="mb-2 grid grid-cols-12 gap-2">
            <input v-model="l.description" required class="input col-span-6" placeholder="Description" />
            <input v-model.number="l.qty" type="number" min="1" step="any" class="input col-span-2" />
            <input v-model.number="l.price" type="number" min="0" step="0.01" class="input col-span-3" placeholder="Price" />
            <button type="button" class="btn btn-ghost col-span-1 !px-0" :disabled="form.lines.length === 1" @click="form.lines.splice(i, 1)"><Trash2 class="size-4" /></button>
          </div>
          <button type="button" class="btn btn-sm btn-ghost text-brand-600" @click="form.lines.push({ description: '', qty: 1, price: 0 })"><Plus class="size-3.5" /> Add line</button>
        </div>
        <div class="flex items-center justify-between rounded-2xl bg-slate-50 p-4">
          <div class="text-sm text-slate-500">Subtotal {{ money(subtotal, 2) }} · Tax {{ money(subtotal * form.tax_rate, 2) }}</div>
          <div class="text-xl font-extrabold">{{ money(subtotal * (1 + form.tax_rate), 2) }}</div>
        </div>
        <div class="flex justify-end gap-2"><button type="button" class="btn btn-ghost" @click="showNew = false">Cancel</button><button class="btn btn-primary">Create & send</button></div>
      </form>
    </Modal>
  </div>
</template>
