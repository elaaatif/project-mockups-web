<script setup>
import { computed, ref } from 'vue'
import { ArrowRight } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date, humanize, money } from '@/core/format'
import { ordersService } from '../orders.service'

const { data, error, reload } = useResource(ordersService.list)
const channel = ref('all')
const rows = computed(() => data.value.filter((o) => channel.value === 'all' || o.channel === channel.value))
const STATUS_TONE = { placed: 'pending', paid: 'confirmed', packed: 'processing', shipped: 'shipped', out_for_delivery: 'shipped', delivered: 'delivered' }

async function advance(o) {
  const res = await act(() => ordersService.advance(o.id), `${o.id} moved to the next stage`)
  if (res) Object.assign(o, res)
}
</script>

<template>
  <div>
    <PageHeader title="Orders" subtitle="Retail and wholesale orders — advance them through fulfilment" />
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="card overflow-hidden">
      <div class="border-b border-slate-100 p-4"><div class="inline-flex rounded-xl bg-slate-100 p-1">
        <button v-for="c in ['all', 'retail', 'wholesale']" :key="c" class="tab capitalize" :class="{ 'tab-active': channel === c }" @click="channel = c">{{ c }}</button>
      </div></div>
      <div class="overflow-x-auto">
        <table class="table-base">
          <thead><tr><th>Order</th><th>Customer</th><th>Date</th><th>Items</th><th>Channel</th><th class="text-right">Total</th><th>Status</th><th /></tr></thead>
          <tbody>
            <tr v-for="o in rows" :key="o.id">
              <td class="font-semibold text-brand-700">{{ o.id }}</td>
              <td><p class="font-medium">{{ o.customer.name }}</p><p class="text-xs text-slate-500">{{ o.customer.email }}</p></td>
              <td class="text-slate-500">{{ date(o.created) }}</td>
              <td>{{ o.items.reduce((s, i) => s + i.qty, 0) }}</td>
              <td class="capitalize">{{ o.channel }}</td>
              <td class="text-right font-semibold">{{ money(o.total, 2) }}</td>
              <td><StatusBadge :status="STATUS_TONE[o.status]" :label="humanize(o.status)" /></td>
              <td class="text-right"><button v-if="o.status !== 'delivered'" class="btn btn-sm btn-secondary" @click="advance(o)">Next stage <ArrowRight class="size-3.5" /></button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
