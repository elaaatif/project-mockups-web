<script setup>
// Agent card with two lead-gen actions: book a viewing (real slots) or send an enquiry.
import { ref, watch } from 'vue'
import { CalendarCheck, CheckCircle2, Mail, Phone } from 'lucide-vue-next'
import { act } from '@/core/resource'
import { listingsService } from '../listings.service'

const props = defineProps({ property: Object })
const tab = ref('viewing')
const days = Array.from({ length: 10 }, (_, i) => { const d = new Date(); d.setDate(d.getDate() + i + 1); return d })
const day = ref(days[0].toLocaleDateString('en-CA'))
const slots = ref([])
const time = ref(null)
const form = ref({ name: '', email: '', phone: '', message: `I'm interested in ${props.property.title}. Is it still available?` })
const done = ref(null)

async function loadSlots() { time.value = null; slots.value = (await act(() => listingsService.slots(props.property.id, day.value))) ?? [] }
watch(day, loadSlots, { immediate: true })

async function submit() {
  const base = { name: form.value.name, email: form.value.email, phone: form.value.phone }
  const res = tab.value === 'viewing'
    ? await act(() => listingsService.bookViewing({ ...base, property_id: props.property.id, date: day.value, time: time.value }))
    : await act(() => listingsService.enquire({ ...base, property_id: props.property.id, message: form.value.message }))
  if (res) done.value = tab.value === 'viewing' ? `Viewing confirmed for ${day.value} at ${time.value}.` : 'Thanks — your message is with the agent.'
  else if (tab.value === 'viewing') loadSlots()
}
</script>

<template>
  <div class="card overflow-hidden shadow-xl">
    <div class="flex items-center gap-4 p-5">
      <img :src="property.agent.photo + '&w=160&h=160&q=70'" :alt="property.agent.name" class="size-14 rounded-full object-cover" />
      <div class="flex-1"><p class="font-semibold">{{ property.agent.name }}</p><p class="text-sm text-slate-500">{{ property.agent.title }} · {{ property.agent.deals }} deals</p></div>
      <a :href="`tel:${property.agent.phone}`" class="rounded-full bg-brand-50 p-2.5 text-brand-700"><Phone class="size-4" /></a>
    </div>
    <div v-if="done" class="border-t border-slate-100 p-8 text-center">
      <CheckCircle2 class="mx-auto size-12 text-emerald-500" /><p class="mt-3 font-semibold">{{ done }}</p><p class="mt-1 text-sm text-slate-500">{{ property.agent.name.split(' ')[0] }} will be in touch shortly.</p>
    </div>
    <template v-else>
      <div class="grid grid-cols-2 border-y border-slate-100 text-sm font-semibold">
        <button class="flex items-center justify-center gap-2 py-3" :class="tab === 'viewing' ? 'bg-slate-900 text-white' : 'text-slate-600'" @click="tab = 'viewing'"><CalendarCheck class="size-4" /> Book viewing</button>
        <button class="flex items-center justify-center gap-2 py-3" :class="tab === 'enquiry' ? 'bg-slate-900 text-white' : 'text-slate-600'" @click="tab = 'enquiry'"><Mail class="size-4" /> Enquire</button>
      </div>
      <form class="space-y-3 p-5" @submit.prevent="submit">
        <template v-if="tab === 'viewing'">
          <div class="-mx-1 flex gap-2 overflow-x-auto px-1 pb-1">
            <button v-for="d in days" :key="d.toISOString()" type="button" class="w-14 shrink-0 rounded-xl py-2 text-center ring-1" :class="day === d.toLocaleDateString('en-CA') ? 'bg-brand-600 text-white ring-brand-600' : 'ring-slate-200'" @click="day = d.toLocaleDateString('en-CA')">
              <span class="block text-[11px] uppercase opacity-70">{{ d.toLocaleDateString('en', { weekday: 'short' }) }}</span><span class="font-bold">{{ d.getDate() }}</span>
            </button>
          </div>
          <div v-if="slots.length" class="grid grid-cols-4 gap-2">
            <button v-for="s in slots" :key="s.time" type="button" :disabled="!s.available" class="rounded-lg py-1.5 text-sm font-semibold ring-1 disabled:text-slate-300 disabled:line-through" :class="time === s.time ? 'bg-slate-900 text-white ring-slate-900' : 'ring-slate-200'" @click="time = s.time">{{ s.time }}</button>
          </div>
          <p v-else class="rounded-lg bg-slate-50 p-3 text-center text-sm text-slate-500">No viewings on Sundays.</p>
        </template>
        <input v-model="form.name" required minlength="2" class="input" placeholder="Full name" />
        <input v-model="form.email" required type="email" class="input" placeholder="Email" />
        <input v-model="form.phone" class="input" placeholder="Phone" />
        <textarea v-if="tab === 'enquiry'" v-model="form.message" rows="3" class="input" />
        <button class="btn btn-primary w-full" :disabled="tab === 'viewing' && !time">{{ tab === 'viewing' ? (time ? `Confirm viewing at ${time}` : 'Pick a time') : 'Send enquiry' }}</button>
      </form>
    </template>
  </div>
</template>
