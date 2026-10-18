<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { CalendarDays, CalendarPlus, Clock, UserRound, XCircle } from 'lucide-vue-next'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { act } from '@/core/resource'
import { date, money } from '@/core/format'
import { bookingsService, downloadIcs } from '../bookings.service'

const route = useRoute()
const email = ref(route.query.email ?? '')
const list = ref(null)
const today = new Date().toISOString().slice(0, 10)
const upcoming = computed(() => list.value?.filter((b) => b.date >= today && b.status !== 'cancelled').reverse() ?? [])
const past = computed(() => list.value?.filter((b) => b.date < today || b.status === 'cancelled') ?? [])

async function find() { list.value = await act(() => bookingsService.lookup(email.value)) }
async function cancel(b) {
  if (!confirm(`Cancel ${b.service_name} on ${b.date}?`)) return
  const res = await act(() => bookingsService.cancel(b.code), 'Booking cancelled — any deposit will be refunded')
  if (res) Object.assign(b, res)
}
onMounted(() => email.value && find())
</script>

<template>
  <div class="mx-auto max-w-4xl px-6 py-14">
    <h1 class="text-4xl font-extrabold tracking-tight">My bookings</h1>
    <p class="mt-2 text-slate-600">Enter the email you booked with to view, add to calendar or cancel.</p>
    <form class="mt-6 flex gap-2" @submit.prevent="find">
      <input v-model="email" type="email" required class="input" placeholder="you@example.com" />
      <button class="btn btn-primary shrink-0">Find bookings</button>
    </form>
    <p class="mt-2 text-sm text-slate-500">Demo: <button class="font-semibold text-brand-700 underline" @click="email = 'emma@example.com'; find()">emma@example.com</button></p>

    <template v-if="list">
      <h2 class="mt-12 text-lg font-extrabold">Upcoming ({{ upcoming.length }})</h2>
      <div class="mt-4 space-y-3">
        <div v-for="b in upcoming" :key="b.code" class="card flex flex-wrap items-center gap-4 p-5">
          <div class="grid w-16 place-items-center rounded-2xl bg-brand-50 py-2 text-brand-700"><span class="text-xs font-bold uppercase">{{ new Date(b.date + 'T00:00').toLocaleDateString('en', { month: 'short' }) }}</span><span class="text-2xl font-extrabold">{{ +b.date.slice(8) }}</span></div>
          <div class="min-w-48 flex-1">
            <p class="font-bold">{{ b.service_name }} · {{ b.business_name }}</p>
            <p class="mt-1 flex flex-wrap gap-3 text-sm text-slate-500"><span class="flex items-center gap-1"><Clock class="size-4" />{{ b.time }} · {{ b.minutes }} min</span><span class="flex items-center gap-1"><UserRound class="size-4" />{{ b.staff_name }}</span><span v-if="b.price">{{ money(b.price) }}</span></p>
          </div>
          <div class="flex gap-2">
            <button class="btn btn-sm btn-secondary" @click="downloadIcs(b)"><CalendarPlus class="size-3.5" /> Calendar</button>
            <button class="btn btn-sm btn-danger" @click="cancel(b)"><XCircle class="size-3.5" /> Cancel</button>
          </div>
        </div>
        <p v-if="!upcoming.length" class="rounded-2xl bg-slate-50 p-8 text-center text-slate-500"><CalendarDays class="mx-auto mb-2 size-8 text-slate-300" />No upcoming bookings. <RouterLink to="/explore" class="font-semibold text-brand-700">Book something →</RouterLink></p>
      </div>
      <h2 v-if="past.length" class="mt-12 text-lg font-extrabold">History</h2>
      <div class="card mt-4 divide-y divide-slate-100">
        <div v-for="b in past" :key="b.code" class="flex items-center justify-between gap-4 p-4 text-sm">
          <div><p class="font-semibold">{{ b.service_name }} · {{ b.business_name }}</p><p class="text-slate-500">{{ date(b.date) }} · {{ b.time }}</p></div>
          <StatusBadge :status="b.status" />
        </div>
      </div>
    </template>
  </div>
</template>
