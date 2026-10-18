<script setup>
import { computed, ref, watch } from 'vue'
import { CalendarPlus, CheckCircle2, ChevronLeft, Clock, Loader2, Minus, Plus, UserRound, Users } from 'lucide-vue-next'
import { act } from '@/core/resource'
import { money } from '@/core/format'
import { bookingsService, downloadIcs } from '@/modules/bookings/bookings.service'
import { marketplaceService } from '../marketplace.service'

const props = defineProps({ business: Object })
const isTable = computed(() => props.business.kind === 'table')

const step = ref(1)
const serviceId = ref(null)
const staffId = ref(null) // null = any
const party = ref(2)
const day = ref(props.business.days[0].date)
const time = ref(null)
const slots = ref([])
const loadingSlots = ref(false)
const customer = ref({ name: '', email: '', phone: '' })
const notes = ref('')
const confirmed = ref(null)

const svc = computed(() => props.business.services.find((s) => s.id === serviceId.value))
const staff = computed(() => props.business.staff.find((s) => s.id === staffId.value))
const price = computed(() => (svc.value ? svc.value.price * (svc.value.per_person ? party.value : 1) : 0))
const groups = computed(() => {
  const g = { Morning: [], Afternoon: [], Evening: [] }
  for (const s of slots.value) g[+s.time.slice(0, 2) < 12 ? 'Morning' : +s.time.slice(0, 2) < 17 ? 'Afternoon' : 'Evening'].push(s)
  return Object.entries(g).filter(([, v]) => v.length)
})

async function loadSlots() {
  if (!serviceId.value) return
  loadingSlots.value = true
  time.value = null
  const res = await act(() => marketplaceService.availability(props.business.slug, { service_id: serviceId.value, date: day.value, staff_id: staffId.value, party_size: party.value }))
  slots.value = res?.slots ?? []
  loadingSlots.value = false
}
watch([day, staffId, party, serviceId], loadSlots)

function pickService(id) { serviceId.value = id; step.value = isTable.value ? 3 : 2 }
function pickStaff(id) { staffId.value = id; step.value = 3 }

async function confirm() {
  const res = await act(() => bookingsService.book({
    business_slug: props.business.slug, service_id: serviceId.value, staff_id: staffId.value, date: day.value, time: time.value,
    party_size: isTable.value ? party.value : 1, customer: customer.value, notes: notes.value,
  }))
  if (res) { confirmed.value = res; step.value = 5 } else loadSlots()
}
const back = () => { step.value = step.value === 3 && isTable.value ? 1 : step.value - 1 }
const STEPS = computed(() => (isTable.value ? ['Experience', 'Date & time', 'Details'] : ['Service', 'Staff', 'Date & time', 'Details']))
const stepIndex = computed(() => (isTable.value ? { 1: 0, 3: 1, 4: 2 }[step.value] : step.value - 1))
</script>

<template>
  <div class="card overflow-hidden shadow-xl">
    <div v-if="step < 5" class="border-b border-slate-100 p-5">
      <div class="flex items-center gap-2">
        <button v-if="step > 1" class="rounded-lg p-1 hover:bg-slate-100" @click="back"><ChevronLeft class="size-5" /></button>
        <p class="font-bold">{{ isTable ? 'Reserve a table' : 'Book an appointment' }}</p>
      </div>
      <div class="mt-3 flex gap-1.5">
        <div v-for="(s, i) in STEPS" :key="s" class="h-1.5 flex-1 rounded-full transition" :class="i <= stepIndex ? 'bg-brand-500' : 'bg-slate-100'" />
      </div>
      <p class="mt-2 text-xs font-semibold text-slate-500">Step {{ stepIndex + 1 }} of {{ STEPS.length }} · {{ STEPS[stepIndex] }}</p>
    </div>

    <div class="p-5">
      <!-- 1 Service -->
      <div v-if="step === 1" class="space-y-2">
        <div v-if="isTable" class="mb-4 flex items-center justify-between rounded-2xl bg-slate-50 p-3">
          <span class="flex items-center gap-2 text-sm font-semibold"><Users class="size-4 text-brand-600" /> Guests</span>
          <div class="flex items-center gap-3"><button class="rounded-full p-1.5 ring-1 ring-slate-200" @click="party = Math.max(1, party - 1)"><Minus class="size-4" /></button><span class="w-5 text-center font-bold">{{ party }}</span><button class="rounded-full p-1.5 ring-1 ring-slate-200" @click="party = Math.min(12, party + 1)"><Plus class="size-4" /></button></div>
        </div>
        <button v-for="s in business.services" :key="s.id" class="flex w-full items-center gap-3 rounded-2xl p-4 text-left ring-1 ring-slate-200 transition hover:bg-brand-50/50 hover:ring-brand-400" @click="pickService(s.id)">
          <div class="flex-1"><p class="font-semibold">{{ s.name }}</p><p class="mt-0.5 flex items-center gap-1 text-xs text-slate-500"><Clock class="size-3.5" />{{ s.minutes }} min{{ s.deposit ? ` · ${money(s.deposit)} deposit` : '' }}</p></div>
          <p class="font-bold">{{ s.price ? money(s.price) + (s.per_person ? ' pp' : '') : 'Free' }}</p>
        </button>
      </div>

      <!-- 2 Staff -->
      <div v-else-if="step === 2" class="space-y-2">
        <button class="flex w-full items-center gap-3 rounded-2xl p-4 text-left ring-1 ring-slate-200 hover:bg-brand-50/50 hover:ring-brand-400" @click="pickStaff(null)">
          <span class="grid size-11 place-items-center rounded-full bg-brand-100 text-brand-700"><Users class="size-5" /></span>
          <div><p class="font-semibold">Any available</p><p class="text-xs text-slate-500">Most availability</p></div>
        </button>
        <button v-for="s in business.staff" :key="s.id" class="flex w-full items-center gap-3 rounded-2xl p-4 text-left ring-1 ring-slate-200 hover:bg-brand-50/50 hover:ring-brand-400" @click="pickStaff(s.id)">
          <span class="grid size-11 place-items-center rounded-full bg-slate-100 text-slate-600"><UserRound class="size-5" /></span>
          <div><p class="font-semibold">{{ s.name }}</p><p class="text-xs text-slate-500">{{ s.role }}</p></div>
        </button>
      </div>

      <!-- 3 Date & time -->
      <div v-else-if="step === 3">
        <div class="-mx-1 flex gap-2 overflow-x-auto px-1 pb-2">
          <button v-for="d in business.days" :key="d.date" class="flex w-14 shrink-0 flex-col items-center rounded-2xl py-2.5 ring-1 transition" :class="day === d.date ? 'bg-brand-600 text-white ring-brand-600' : 'ring-slate-200 hover:ring-brand-400'" @click="day = d.date">
            <span class="text-[11px] font-semibold uppercase opacity-70">{{ d.weekday }}</span><span class="text-lg font-bold">{{ d.day }}</span>
          </button>
        </div>
        <div v-if="loadingSlots" class="grid h-40 place-items-center"><Loader2 class="size-6 animate-spin text-brand-600" /></div>
        <template v-else>
          <div v-for="[label, list] in groups" :key="label" class="mt-4">
            <p class="text-xs font-bold text-slate-500 uppercase">{{ label }}</p>
            <div class="mt-2 grid grid-cols-4 gap-2">
              <button v-for="s in list" :key="s.time" :disabled="!s.available" class="rounded-xl py-2 text-sm font-semibold ring-1 transition disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-300 disabled:line-through disabled:ring-slate-100"
                      :class="time === s.time ? 'bg-brand-600 text-white ring-brand-600' : 'ring-slate-200 hover:ring-brand-400'" @click="time = s.time">{{ s.time }}</button>
            </div>
          </div>
          <p v-if="!slots.some((s) => s.available)" class="mt-6 rounded-xl bg-amber-50 p-4 text-center text-sm text-amber-800">Fully booked — try another day.</p>
        </template>
        <button class="btn btn-primary mt-5 w-full" :disabled="!time" @click="step = 4">Continue</button>
      </div>

      <!-- 4 Details -->
      <form v-else-if="step === 4" class="space-y-3" @submit.prevent="confirm">
        <div class="rounded-2xl bg-brand-50 p-4 text-sm">
          <p class="font-bold">{{ svc.name }}</p>
          <p class="text-slate-600">{{ new Date(day + 'T00:00').toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }) }} at {{ time }} · {{ svc.minutes }} min</p>
          <p class="text-slate-600">{{ isTable ? `${party} guests` : staff?.name ?? 'Any available staff' }}</p>
          <p class="mt-2 font-bold">{{ price ? money(price) : 'Free' }}<span v-if="svc.deposit" class="font-normal text-slate-500"> · {{ money(svc.deposit * (svc.per_person ? party : 1)) }} deposit today</span></p>
        </div>
        <input v-model="customer.name" required minlength="2" class="input" placeholder="Full name" />
        <input v-model="customer.email" required type="email" class="input" placeholder="Email" />
        <input v-model="customer.phone" class="input" placeholder="Mobile (for WhatsApp reminder)" />
        <textarea v-model="notes" rows="2" class="input" :placeholder="isTable ? 'Allergies, occasion…' : 'Anything we should know?'" />
        <button class="btn btn-primary w-full !py-3">Confirm booking</button>
      </form>

      <!-- 5 Confirmed -->
      <div v-else class="py-4 text-center">
        <CheckCircle2 class="mx-auto size-14 text-brand-600" />
        <p class="mt-3 text-xl font-extrabold">You're booked!</p>
        <p class="mt-1 text-sm text-slate-500">Confirmation <span class="font-mono font-bold text-slate-800">{{ confirmed.code }}</span> sent to {{ confirmed.customer.email }}</p>
        <div class="mt-5 rounded-2xl bg-slate-50 p-4 text-left text-sm">
          <p class="font-bold">{{ confirmed.service_name }}</p>
          <p class="text-slate-600">{{ confirmed.date }} · {{ confirmed.time }} · {{ confirmed.staff_name }}</p>
        </div>
        <div class="mt-5 grid gap-2">
          <button class="btn btn-secondary" @click="downloadIcs(confirmed)"><CalendarPlus class="size-4" /> Add to calendar</button>
          <RouterLink :to="{ path: '/my-bookings', query: { email: confirmed.customer.email } }" class="btn btn-ghost">Manage my bookings</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>
