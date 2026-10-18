<script setup>
import { computed, ref, watch } from 'vue'
import { Line } from 'vue-chartjs'
import { CalendarCheck, ChevronLeft, ChevronRight, DollarSign, Gauge, UserX } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard from '@/components/ui/StatCard.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { money } from '@/core/format'
import { bookingsService } from '@/modules/bookings/bookings.service'
import BusinessSwitcher from '../components/BusinessSwitcher.vue'
import { ownerService } from '../owner.service'
import { currentBusiness } from '../owner.store'

const day = ref(new Date().toISOString().slice(0, 10))
const { data, error, reload } = useResource(() => ownerService.overview(currentBusiness.value, day.value))
watch([currentBusiness, day], reload)

const shift = (n) => { const d = new Date(day.value + 'T00:00'); d.setDate(d.getDate() + n); day.value = d.toLocaleDateString('en-CA') }
const label = computed(() => new Date(day.value + 'T00:00').toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }))

// Calendar geometry: 1 minute = PX pixels
const PX = 1.4
const mins = (t) => +t.slice(0, 2) * 60 + +t.slice(3, 5)
const startMin = computed(() => Math.floor(mins(data.value.business.open) / 60) * 60)
const endMin = computed(() => Math.ceil(mins(data.value.business.close) / 60) * 60)
const hours = computed(() => Array.from({ length: (endMin.value - startMin.value) / 60 }, (_, i) => startMin.value / 60 + i))
const forStaff = (id) => data.value.schedule.filter((b) => b.staff_id === id)
const TONES = ['bg-brand-50 border-brand-500 text-brand-900', 'bg-violet-50 border-violet-500 text-violet-900', 'bg-amber-50 border-amber-500 text-amber-900', 'bg-sky-50 border-sky-500 text-sky-900']
const nowTop = computed(() => {
  const n = new Date()
  if (day.value !== n.toLocaleDateString('en-CA')) return null
  const m = n.getHours() * 60 + n.getMinutes()
  return m >= startMin.value && m <= endMin.value ? (m - startMin.value) * PX : null
})

const trendData = computed(() => ({
  labels: data.value.trend.map((t) => t.date.slice(5)),
  datasets: [{ data: data.value.trend.map((t) => t.count), borderColor: '#0d9488', backgroundColor: 'rgba(13,148,136,.1)', fill: true, tension: 0.4, pointRadius: 3 }],
}))
const trendOpts = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false } }, y: { beginAtZero: true, grid: { color: '#f1f5f9' } } } }

const active = ref(null)
async function setStatus(status) {
  const res = await act(() => bookingsService.setStatus(active.value.code, status), 'Booking updated')
  if (res) { active.value = null; reload() }
}
</script>

<template>
  <div>
    <PageHeader title="Calendar" :subtitle="label"><BusinessSwitcher /></PageHeader>
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Bookings this day" :value="data.kpis.today" :icon="CalendarCheck" />
        <StatCard label="Revenue · last 7 days" :value="money(data.kpis.revenue_week)" :icon="DollarSign" tone="emerald" />
        <StatCard label="Occupancy" :value="data.kpis.occupancy + '%'" :icon="Gauge" tone="sky" hint="of staff hours booked" />
        <StatCard label="No-show rate" :value="data.kpis.no_show_rate + '%'" :icon="UserX" tone="rose" hint="reminders keep this low" />
      </div>

      <div class="card mt-6 overflow-hidden">
        <div class="flex items-center gap-2 border-b border-slate-100 px-5 py-3">
          <button class="rounded-lg p-1.5 hover:bg-slate-100" @click="shift(-1)"><ChevronLeft class="size-5" /></button>
          <button class="btn btn-sm btn-secondary" @click="day = new Date().toLocaleDateString('en-CA')">Today</button>
          <button class="rounded-lg p-1.5 hover:bg-slate-100" @click="shift(1)"><ChevronRight class="size-5" /></button>
          <p class="ml-2 font-bold">{{ label }}</p>
          <span class="ml-auto text-sm text-slate-500">{{ data.business.open }}–{{ data.business.close }}</span>
        </div>
        <div class="overflow-x-auto">
          <div class="grid min-w-[720px]" :style="{ gridTemplateColumns: `64px repeat(${data.business.staff.length}, minmax(180px, 1fr))` }">
            <div class="sticky top-0 border-b border-slate-100 bg-white" />
            <div v-for="s in data.business.staff" :key="s.id" class="border-b border-l border-slate-100 bg-white px-3 py-3 text-center">
              <p class="text-sm font-bold">{{ s.name }}</p><p class="text-xs text-slate-500">{{ s.role }}</p>
            </div>
            <div class="relative" :style="{ height: (endMin - startMin) * PX + 'px' }">
              <div v-for="h in hours" :key="h" class="absolute right-2 -translate-y-2 text-xs text-slate-400" :style="{ top: (h * 60 - startMin) * PX + 'px' }">{{ String(h).padStart(2, '0') }}:00</div>
            </div>
            <div v-for="(s, si) in data.business.staff" :key="s.id" class="relative border-l border-slate-100" :style="{ height: (endMin - startMin) * PX + 'px' }">
              <div v-for="h in hours" :key="h" class="absolute inset-x-0 border-t border-slate-100" :style="{ top: (h * 60 - startMin) * PX + 'px' }" />
              <div v-if="nowTop !== null" class="absolute inset-x-0 z-10 h-0.5 bg-rose-500" :style="{ top: nowTop + 'px' }" />
              <button v-for="b in forStaff(s.id)" :key="b.code" class="absolute inset-x-1.5 overflow-hidden rounded-lg border-l-4 px-2 py-1 text-left text-xs shadow-sm transition hover:z-20 hover:shadow-md"
                      :class="[TONES[si % TONES.length], { 'opacity-50': b.status === 'no_show' }]"
                      :style="{ top: (mins(b.time) - startMin) * PX + 'px', height: Math.max(b.minutes * PX - 3, 22) + 'px' }" @click="active = b">
                <p class="truncate font-bold">{{ b.time }} · {{ b.customer.name }}</p>
                <p class="truncate opacity-80">{{ b.service_name }}{{ b.party_size > 1 ? ` · ${b.party_size} guests` : '' }}</p>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="card mt-6 p-6"><h3 class="font-bold">Bookings per day · ±7 days</h3><div class="mt-4 h-56"><Line :data="trendData" :options="trendOpts" /></div></div>
    </template>

    <Modal :open="!!active" :title="active?.customer.name" :subtitle="`${active?.code} · ${active?.service_name}`" @close="active = null">
      <div v-if="active" class="space-y-4 text-sm">
        <div class="grid grid-cols-2 gap-3 rounded-2xl bg-slate-50 p-4">
          <div><p class="label">When</p><p class="font-semibold">{{ active.date }} · {{ active.time }} ({{ active.minutes }} min)</p></div>
          <div><p class="label">With</p><p class="font-semibold">{{ active.staff_name }}</p></div>
          <div><p class="label">Price</p><p class="font-semibold">{{ active.price ? money(active.price) : 'Free' }}</p></div>
          <div><p class="label">Status</p><StatusBadge :status="active.status" /></div>
        </div>
        <p class="text-slate-500">{{ active.customer.email }}</p>
        <div class="flex flex-wrap justify-end gap-2">
          <button class="btn btn-danger" @click="setStatus('no_show')">No-show</button>
          <button class="btn btn-secondary" @click="setStatus('cancelled')">Cancel</button>
          <button class="btn btn-success" @click="setStatus('checked_in')">Check in</button>
          <button class="btn btn-primary" @click="setStatus('completed')">Complete</button>
        </div>
      </div>
    </Modal>
  </div>
</template>
