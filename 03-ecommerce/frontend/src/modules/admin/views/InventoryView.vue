<script setup>
import { PackagePlus } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { money } from '@/core/format'
import { img } from '@/core/media'
import { adminService } from '../admin.service'

const { data, error, reload } = useResource(adminService.inventory)
const status = (p) => (p.stock === 0 ? 'out_of_stock' : p.stock < 15 ? 'low_stock' : 'in_stock')
async function restock(p, qty) {
  const res = await act(() => adminService.restock(p.slug, qty), `+${qty} ${p.name}`)
  if (res) Object.assign(p, res)
}
</script>

<template>
  <div>
    <PageHeader title="Inventory" subtitle="Live stock shared by the shop, wholesale portal and quotes — sorted by urgency" />
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="card overflow-x-auto">
      <table class="table-base">
        <thead><tr><th>Product</th><th>SKU</th><th class="text-right">Price</th><th class="text-right">Stock</th><th>Status</th><th class="text-right">Restock</th></tr></thead>
        <tbody>
          <tr v-for="p in data" :key="p.id">
            <td><div class="flex items-center gap-3"><img :src="img(p.image, 100)" class="size-10 rounded-lg object-cover" :alt="p.name" /><span class="font-semibold">{{ p.name }}</span></div></td>
            <td class="font-mono text-xs">{{ p.sku }}</td>
            <td class="text-right">{{ money(p.price) }}</td>
            <td class="text-right font-bold tabular-nums">{{ p.stock }}</td>
            <td><StatusBadge :status="status(p)" /></td>
            <td><div class="flex justify-end gap-1"><button v-for="n in [25, 100]" :key="n" class="btn btn-sm btn-secondary" @click="restock(p, n)"><PackagePlus class="size-3.5" />+{{ n }}</button></div></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
