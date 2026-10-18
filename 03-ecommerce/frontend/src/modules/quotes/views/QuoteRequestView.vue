<script setup>
import { ref } from 'vue'
import { CheckCircle2, FileText, Trash2 } from 'lucide-vue-next'
import { act } from '@/core/resource'
import { money } from '@/core/format'
import { img } from '@/core/media'
import { quotesService } from '../quotes.service'
import { quoteList } from '../quote.store'

const form = ref({ company: '', contact: '', email: '', phone: '', needed_by: '', notes: '' })
const sent = ref(null)

async function submit() {
  const body = { ...form.value, needed_by: form.value.needed_by || null, items: quoteList.items.map((i) => ({ product_id: i.id, qty: i.qty })) }
  const res = await act(() => quotesService.request(body), 'Quote request sent')
  if (res) { sent.value = res; quoteList.clear() }
}
</script>

<template>
  <div class="mx-auto max-w-6xl px-6 py-14">
    <p class="text-sm font-semibold tracking-widest text-brand-700 uppercase">For businesses</p>
    <h1 class="mt-2 font-display text-4xl font-semibold">Request a quotation</h1>
    <p class="mt-2 max-w-2xl text-slate-600">Hotels, offices, gyms and retailers: tell us what you need and our team replies with tailored bulk pricing within one business day.</p>

    <div v-if="sent" class="card mt-10 p-10 text-center">
      <CheckCircle2 class="mx-auto size-14 text-brand-600" />
      <h2 class="mt-4 font-display text-2xl font-semibold">Thanks, {{ sent.contact.split(' ')[0] }}! Request #{{ sent.id }} received</h2>
      <p class="mt-2 text-slate-600">Indicative value at wholesale tiers: <strong>{{ money(sent.estimate, 2) }}</strong>. A formal quote will arrive at {{ sent.email }}.</p>
      <RouterLink to="/shop" class="btn btn-primary mt-6">Continue browsing</RouterLink>
    </div>

    <div v-else class="mt-10 grid gap-8 lg:grid-cols-5">
      <div class="lg:col-span-2">
        <div class="card p-6">
          <h2 class="font-semibold">Products in your request</h2>
          <ul v-if="quoteList.items.length" class="mt-4 space-y-4">
            <li v-for="i in quoteList.items" :key="i.id" class="flex items-center gap-3">
              <img :src="img(i.image, 120)" class="size-14 rounded-lg object-cover" :alt="i.name" />
              <div class="min-w-0 flex-1"><p class="truncate text-sm font-semibold">{{ i.name }}</p><p class="text-xs text-slate-500">List {{ money(i.price) }}</p></div>
              <input v-model.number="i.qty" type="number" min="1" class="input !w-20 !py-1.5" />
              <button class="text-slate-400 hover:text-rose-600" @click="quoteList.remove(i.id)"><Trash2 class="size-4" /></button>
            </li>
          </ul>
          <div v-else class="mt-4 rounded-xl bg-slate-50 p-6 text-center text-sm text-slate-500">
            <FileText class="mx-auto size-8 text-slate-300" />
            <p class="mt-2">No products yet. Use <strong>“Add to quote”</strong> on any product page.</p>
            <RouterLink to="/shop" class="btn btn-sm btn-secondary mt-4">Browse catalog</RouterLink>
          </div>
        </div>
      </div>
      <form class="card grid gap-4 p-6 sm:grid-cols-2 lg:col-span-3" @submit.prevent="submit">
        <div><label class="label">Company</label><input v-model="form.company" required class="input" /></div>
        <div><label class="label">Contact name</label><input v-model="form.contact" required class="input" /></div>
        <div><label class="label">Work email</label><input v-model="form.email" type="email" required class="input" /></div>
        <div><label class="label">Phone</label><input v-model="form.phone" class="input" /></div>
        <div class="sm:col-span-2"><label class="label">Needed by</label><input v-model="form.needed_by" type="date" class="input" /></div>
        <div class="sm:col-span-2"><label class="label">Project notes</label><textarea v-model="form.notes" rows="4" class="input" placeholder="Branding, delivery phases, installation…" /></div>
        <button class="btn btn-primary sm:col-span-2" :disabled="!quoteList.items.length">Send quote request</button>
      </form>
    </div>
  </div>
</template>
