<script setup>
import { ref } from 'vue'
import { CheckCircle2, Clock, Mail, MapPin, Phone } from 'lucide-vue-next'
import { act } from '@/core/resource'
import { siteService } from '../site.service'

const form = ref({ name: '', email: '', company: '', phone: '', topic: 'Sales enquiry', message: '' })
const sent = ref(false)
async function submit() { if (await act(() => siteService.contact(form.value))) sent.value = true }
</script>

<template>
  <div class="mx-auto grid max-w-7xl gap-12 px-6 py-20 lg:grid-cols-5">
    <div class="lg:col-span-2">
      <p class="text-sm font-bold tracking-[.2em] text-brand-600 uppercase">Contact</p>
      <h1 class="mt-3 text-5xl font-black uppercase">Let's talk</h1>
      <div class="mt-10 space-y-6">
        <p v-for="c in [[Phone, 'Sales', '+44 121 496 0000'], [Clock, '24/7 service hotline', '+44 121 496 0999'], [Mail, 'Email', 'sales@vertex-industrial.example'], [MapPin, 'Head office', 'Unit 7, Aston Science Park, Birmingham B7 4BJ']]" :key="c[1]" class="flex gap-4">
          <span class="grid size-12 shrink-0 place-items-center bg-slate-950 text-brand-500"><component :is="c[0]" class="size-5" /></span><span><span class="block text-sm text-slate-500">{{ c[1] }}</span><span class="font-bold">{{ c[2] }}</span></span>
        </p>
      </div>
    </div>
    <div class="lg:col-span-3">
      <div v-if="sent" class="grid h-full place-items-center bg-slate-50 p-12 text-center"><div><CheckCircle2 class="mx-auto size-14 text-brand-600" /><p class="mt-4 text-2xl font-black uppercase">Message received</p><p class="mt-2 text-slate-600">A specialist will reply within one business day.</p></div></div>
      <form v-else class="grid gap-4 bg-slate-50 p-8 sm:grid-cols-2" @submit.prevent="submit">
        <div><label class="label">Name</label><input v-model="form.name" required minlength="2" class="input !rounded-none" /></div>
        <div><label class="label">Work email</label><input v-model="form.email" required type="email" class="input !rounded-none" /></div>
        <div><label class="label">Company</label><input v-model="form.company" class="input !rounded-none" /></div>
        <div><label class="label">Phone</label><input v-model="form.phone" class="input !rounded-none" /></div>
        <div class="sm:col-span-2"><label class="label">Topic</label><select v-model="form.topic" class="input !rounded-none"><option>Sales enquiry</option><option>Service & maintenance</option><option>Spare parts</option><option>Become a distributor</option><option>Other</option></select></div>
        <div class="sm:col-span-2"><label class="label">Message</label><textarea v-model="form.message" required minlength="5" rows="5" class="input !rounded-none" /></div>
        <button class="btn btn-primary !rounded-none sm:col-span-2">Send message</button>
      </form>
    </div>
  </div>
</template>
