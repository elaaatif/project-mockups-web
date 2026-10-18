<script setup>
import { reactive, ref, watch } from 'vue'
import { AlertTriangle, Boxes, DollarSign, Minus, Package, Plus, Search } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard from '@/components/ui/StatCard.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { money, number } from '@/core/format'
import { inventoryService } from '../inventory.service'

const filters = reactive({ q: '', category: '' })
const { data, error, reload } = useResource(() => inventoryService.list(filters))
let timer
watch(filters, () => { clearTimeout(timer); timer = setTimeout(reload, 250) })

const stockStatus = (i) => (i.qty === 0 ? 'out_of_stock' : i.qty <= i.reorder_level ? 'low_stock' : 'in_stock')
const fill = (i) => Math.min(100, (i.qty / (i.reorder_level * 4 || 1)) * 100)

async function adjust(item, delta) {
  const updated = await act(() => inventoryService.adjust(item.sku, delta))
  if (updated) Object.assign(item, updated)
}

const showAdd = ref(false)
const blank = () => ({ name: '', category: 'Raw Materials', qty: 0, reorder_level: 20, unit_cost: 1, location: 'Warehouse A', supplier: '' })
const form = ref(blank())
async function save() {
  if (await act(() => inventoryService.create(form.value), `${form.value.name} added to inventory`)) {
    showAdd.value = false
    form.value = blank()
    reload()
  }
}
</script>

<template>
  <div>
    <PageHeader title="Inventory" subtitle="Track stock across warehouses and catch shortages before they happen">
      <button class="btn btn-primary" @click="showAdd = true"><Plus class="size-4" /> Add item</button>
    </PageHeader>

    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-3">
        <StatCard label="Active SKUs" :value="data.items.length" :icon="Package" hint="in current filter" />
        <StatCard label="Total stock value" :value="money(data.stock_value)" :icon="DollarSign" tone="emerald" hint="at unit cost" />
        <StatCard label="Below reorder level" :value="data.low_stock" :icon="AlertTriangle" tone="rose" hint="create a PO in Purchasing" />
      </div>

      <div class="card mt-6 overflow-hidden">
        <div class="flex flex-wrap gap-3 border-b border-slate-100 p-4">
          <div class="relative min-w-60 flex-1">
            <Search class="absolute top-1/2 left-3.5 size-4 -translate-y-1/2 text-slate-400" />
            <input v-model="filters.q" class="input pl-10" placeholder="Search by name or SKU" />
          </div>
          <select v-model="filters.category" class="input !w-auto">
            <option value="">All categories</option>
            <option v-for="c in data.categories" :key="c">{{ c }}</option>
          </select>
        </div>
        <div class="overflow-x-auto">
          <table class="table-base">
            <thead><tr><th>Item</th><th>Location</th><th>Supplier</th><th class="w-56">Stock level</th><th>Unit cost</th><th>Value</th><th>Status</th><th class="text-right">Adjust</th></tr></thead>
            <tbody>
              <tr v-for="i in data.items" :key="i.sku" class="hover:bg-slate-50/60">
                <td>
                  <div class="flex items-center gap-3">
                    <span class="grid size-10 place-items-center rounded-xl bg-brand-50 text-brand-600"><Boxes class="size-5" /></span>
                    <div><p class="font-semibold text-slate-800">{{ i.name }}</p><p class="text-xs text-slate-500">{{ i.sku }} · {{ i.category }}</p></div>
                  </div>
                </td>
                <td class="text-slate-600">{{ i.location }}</td>
                <td class="text-slate-600">{{ i.supplier }}</td>
                <td>
                  <div class="flex items-center gap-3">
                    <div class="h-2 flex-1 overflow-hidden rounded-full bg-slate-100">
                      <div class="h-full rounded-full transition-all" :class="i.qty <= i.reorder_level ? 'bg-rose-500' : 'bg-emerald-500'" :style="{ width: fill(i) + '%' }" />
                    </div>
                    <span class="w-16 text-right font-semibold tabular-nums">{{ number(i.qty) }}</span>
                  </div>
                  <p class="mt-1 text-xs text-slate-400">Reorder at {{ i.reorder_level }}</p>
                </td>
                <td class="tabular-nums">{{ money(i.unit_cost, 2) }}</td>
                <td class="font-semibold tabular-nums">{{ money(i.qty * i.unit_cost) }}</td>
                <td><StatusBadge :status="stockStatus(i)" /></td>
                <td>
                  <div class="flex justify-end gap-1">
                    <button class="btn btn-sm btn-secondary !px-2" title="Remove 10" @click="adjust(i, -10)"><Minus class="size-3.5" /></button>
                    <button class="btn btn-sm btn-secondary !px-2" title="Add 10" @click="adjust(i, 10)"><Plus class="size-3.5" /></button>
                  </div>
                </td>
              </tr>
              <tr v-if="!data.items.length"><td colspan="8" class="py-12 text-center text-slate-500">No items match your filters.</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <Modal :open="showAdd" title="Add inventory item" subtitle="New SKUs are numbered automatically" @close="showAdd = false">
      <form class="grid grid-cols-2 gap-4" @submit.prevent="save">
        <div class="col-span-2"><label class="label">Item name</label><input v-model="form.name" required class="input" placeholder="e.g. Steel Bolt M8" /></div>
        <div><label class="label">Category</label><select v-model="form.category" class="input"><option v-for="c in data?.categories" :key="c">{{ c }}</option></select></div>
        <div><label class="label">Supplier</label><input v-model="form.supplier" class="input" placeholder="Supplier name" /></div>
        <div><label class="label">Quantity</label><input v-model.number="form.qty" type="number" min="0" class="input" /></div>
        <div><label class="label">Reorder level</label><input v-model.number="form.reorder_level" type="number" min="0" class="input" /></div>
        <div><label class="label">Unit cost ($)</label><input v-model.number="form.unit_cost" type="number" step="0.01" min="0.01" class="input" /></div>
        <div><label class="label">Location</label><select v-model="form.location" class="input"><option>Warehouse A</option><option>Warehouse B</option><option>Store Room</option></select></div>
        <div class="col-span-2 mt-2 flex justify-end gap-2">
          <button type="button" class="btn btn-ghost" @click="showAdd = false">Cancel</button>
          <button class="btn btn-primary">Save item</button>
        </div>
      </form>
    </Modal>
  </div>
</template>
