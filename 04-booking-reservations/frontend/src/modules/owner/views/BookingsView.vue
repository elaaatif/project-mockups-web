<script setup>
import { ref, watch } from 'vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date, humanize, money } from '@/core/format'
import { bookingsService } from '@/modules/bookings/bookings.service'
import BusinessSwitcher from '../components/BusinessSwitcher.vue'
import { ownerService } from '../owner.service'
import { currentBusiness } from '../owner.store'

const status = ref('')
const { data, error, reload } = useResource(() => ownerService.bookings(currentBusiness.value, status.value))
watch([currentBusiness, status], reload)
const NEXT = { confirmed: ['checked_in', 'cancelled'], checked_in: ['completed', 'no_show'] }

async function setStatus(b, s) {
  const res = await act(() => bookingsService.setStatus(b.code, s), `${b.code} → ${humanize(s)}`)
  if (res) Object.assign(b, res)
}
</script>

<template>
  <div>
    <PageHeader title="Bookings" subtitle="Every reservation across your team"><BusinessSwitcher /></PageHeader>
    <div class="mb-4 inline-flex flex-wrap rounded-xl bg-slate-200/60 p-1">
      <button v-for="s in ['', 'confirmed', 'checked_in', 'completed', 'no_show', 'cancelled']" :key="s" class="tab" :class="{ 'tab-active': status === s }" @click="status = s">{{ s ? humanize(s) : 'All' }}</button>
    </div>
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="card overflow-x-auto">
      <table class="table-base">
        <thead><tr><th>Code</th><th>Customer</th><th>Service</th><th>Staff / area</th><th>When</th><th class="text-right">Price</th><th>Status</th><th /></tr></thead>
        <tbody>
          <tr v-for="b in data" :key="b.code">
            <td class="font-mono text-xs font-bold">{{ b.code }}</td>
            <td><p class="font-semibold">{{ b.customer.name }}</p><p class="text-xs text-slate-500">{{ b.customer.email }}</p></td>
            <td>{{ b.service_name }}<span v-if="b.party_size > 1" class="text-slate-500"> · {{ b.party_size }}p</span></td>
            <td class="text-slate-600">{{ b.staff_name }}</td>
            <td class="whitespace-nowrap text-slate-600">{{ date(b.date) }} · {{ b.time }}</td>
            <td class="text-right font-semibold">{{ b.price ? money(b.price) : '—' }}</td>
            <td><StatusBadge :status="b.status" /></td>
            <td><div class="flex justify-end gap-1"><button v-for="s in NEXT[b.status] ?? []" :key="s" class="btn btn-sm" :class="s === 'cancelled' || s === 'no_show' ? 'btn-danger' : 'btn-success'" @click="setStatus(b, s)">{{ humanize(s) }}</button></div></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
