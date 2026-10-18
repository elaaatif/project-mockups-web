<script setup>
import { computed, ref } from 'vue'
import { ArrowRight, CalendarDays, PackageCheck, Sparkles } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date, humanize, money } from '@/core/format'
import { purchasingService } from '../purchasing.service'

const { data, error, reload } = useResource(purchasingService.list)

const COLUMNS = {
  draft: { tone: 'bg-slate-400', action: 'Submit for approval' },
  pending_approval: { tone: 'bg-amber-400', action: 'Approve' },
  approved: { tone: 'bg-sky-500', action: 'Mark received' },
  received: { tone: 'bg-emerald-500', action: null },
}
const byStatus = (s) => data.value.orders.filter((o) => o.status === s)

async function advance(po) {
  const next = await act(() => purchasingService.advance(po.id))
  if (next) {
    Object.assign(po, next)
    if (next.status === 'received') reload() // stock changed → refresh suggestions
  }
}

// Reorder suggestions grouped by supplier
const picked = ref(new Set())
const groups = computed(() => {
  const g = {}
  for (const s of data.value?.suggestions ?? []) (g[s.supplier] ??= []).push(s)
  return g
})
function toggle(sku) {
  picked.value.has(sku) ? picked.value.delete(sku) : picked.value.add(sku)
  picked.value = new Set(picked.value)
}
async function createPo(supplier, items) {
  const lines = items.filter((i) => picked.value.has(i.sku)).map((i) => ({ sku: i.sku, qty: i.suggested_qty }))
  if (!lines.length) return
  if (await act(() => purchasingService.create({ supplier, lines }), `Purchase order sent to ${supplier} for approval`)) {
    picked.value = new Set()
    reload()
  }
}
</script>

<template>
  <div>
    <PageHeader title="Purchasing" subtitle="From reorder suggestion to goods receipt — receiving a PO updates stock automatically" />

    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div v-if="data.suggestions.length" class="card mb-6 overflow-hidden">
        <div class="flex items-center gap-2 border-b border-slate-100 bg-gradient-to-r from-brand-50 to-white px-6 py-4">
          <Sparkles class="size-5 text-brand-600" />
          <h3 class="font-bold">Smart reorder suggestions</h3>
          <span class="text-sm text-slate-500">· {{ data.suggestions.length }} items below reorder level</span>
        </div>
        <div class="grid gap-4 p-6 md:grid-cols-2 xl:grid-cols-3">
          <div v-for="(items, supplier) in groups" :key="supplier" class="rounded-2xl border border-slate-200 p-4">
            <p class="font-semibold">{{ supplier }}</p>
            <label v-for="i in items" :key="i.sku" class="mt-3 flex cursor-pointer items-center gap-3 text-sm">
              <input type="checkbox" class="size-4 accent-brand-600" :checked="picked.has(i.sku)" @change="toggle(i.sku)" />
              <span class="flex-1">{{ i.name }} <span class="text-slate-400">· {{ i.qty }} left</span></span>
              <span class="font-semibold text-brand-700">+{{ i.suggested_qty }}</span>
            </label>
            <button class="btn btn-sm btn-primary mt-4 w-full" :disabled="!items.some((i) => picked.has(i.sku))" @click="createPo(supplier, items)">Create PO</button>
          </div>
        </div>
      </div>

      <div class="grid gap-4 lg:grid-cols-4">
        <div v-for="(col, status) in COLUMNS" :key="status" class="rounded-2xl bg-slate-100/70 p-3">
          <div class="mb-3 flex items-center gap-2 px-1">
            <span class="size-2.5 rounded-full" :class="col.tone" />
            <p class="text-sm font-bold text-slate-700">{{ humanize(status) }}</p>
            <span class="ml-auto rounded-full bg-white px-2 text-xs font-bold text-slate-500">{{ byStatus(status).length }}</span>
          </div>
          <TransitionGroup tag="div" class="space-y-3" move-class="transition duration-300">
            <div v-for="po in byStatus(status)" :key="po.id" class="card p-4">
              <div class="flex items-center justify-between"><p class="font-bold text-slate-800">{{ po.id }}</p><p class="text-sm font-bold">{{ money(po.total) }}</p></div>
              <p class="text-sm text-slate-500">{{ po.supplier }}</p>
              <ul class="mt-3 space-y-1 text-xs text-slate-600">
                <li v-for="l in po.lines" :key="l.sku" class="flex justify-between"><span class="truncate">{{ l.name }}</span><span class="font-semibold">×{{ l.qty }}</span></li>
              </ul>
              <p class="mt-3 flex items-center gap-1.5 text-xs text-slate-400"><CalendarDays class="size-3.5" /> ETA {{ date(po.expected) }}</p>
              <button v-if="col.action" class="btn btn-sm btn-secondary mt-3 w-full" @click="advance(po)">{{ col.action }} <ArrowRight class="size-3.5" /></button>
              <p v-else class="mt-3 flex items-center gap-1.5 text-xs font-semibold text-emerald-600"><PackageCheck class="size-4" /> Stock updated</p>
            </div>
          </TransitionGroup>
        </div>
      </div>
    </template>
  </div>
</template>
