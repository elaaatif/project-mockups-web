<script setup>
import { computed, reactive, ref } from 'vue'
import { Building2, CheckCircle2, Search } from 'lucide-vue-next'
import { act, useResource } from '@/core/resource'
import { date, money } from '@/core/format'
import { img } from '@/core/media'
import { tierPrice, wholesaleService } from '../wholesale.service'

const { data } = useResource(wholesaleService.priceList)
const qty = reactive({})
const q = ref('')
const company = ref({ company: '', vat_number: '', email: '', po_reference: '' })
const placed = ref(null)

const rows = computed(() => (data.value?.products ?? []).filter((p) => p.name.toLowerCase().includes(q.value.toLowerCase())))
const lines = computed(() => (data.value?.products ?? []).filter((p) => qty[p.id] > 0).map((p) => ({ p, qty: qty[p.id], unit: tierPrice(p, qty[p.id]) })))
const total = computed(() => lines.value.reduce((s, l) => s + l.qty * l.unit, 0))
const retail = computed(() => lines.value.reduce((s, l) => s + l.qty * l.p.price, 0))
const belowMoq = computed(() => lines.value.some((l) => l.qty < l.p.moq_wholesale))

async function submit() {
  const res = await act(() => wholesaleService.order({ ...company.value, items: lines.value.map((l) => ({ product_id: l.p.id, qty: l.qty })) }), 'Wholesale order placed')
  if (res) { placed.value = res; Object.keys(qty).forEach((k) => delete qty[k]) }
}
</script>

<template>
  <div class="mx-auto max-w-7xl px-6 py-12">
    <div class="flex flex-wrap items-end justify-between gap-6">
      <div>
        <p class="flex items-center gap-2 text-sm font-semibold tracking-widest text-brand-700 uppercase"><Building2 class="size-4" /> Wholesale portal</p>
        <h1 class="mt-2 font-display text-4xl font-semibold">Trade price list</h1>
        <p class="mt-2 text-slate-600">Tiered pricing applies per line · min. 10 units per product · min. order {{ money(data?.min_order_value ?? 500) }} · {{ data?.payment_terms }} terms</p>
      </div>
      <div class="relative w-72"><Search class="absolute top-1/2 left-3.5 size-4 -translate-y-1/2 text-slate-400" /><input v-model="q" class="input pl-10" placeholder="Filter products" /></div>
    </div>

    <div v-if="placed" class="mt-8 flex items-center gap-4 rounded-2xl bg-brand-50 p-5 ring-1 ring-brand-200">
      <CheckCircle2 class="size-8 shrink-0 text-brand-600" />
      <div class="flex-1"><p class="font-semibold">Order {{ placed.id }} placed for {{ placed.customer.name }}</p><p class="text-sm text-slate-600">{{ money(placed.total, 2) }} · you saved {{ money(placed.savings, 2) }} vs retail · invoice due {{ date(placed.due_date) }}</p></div>
      <button class="btn btn-sm btn-ghost" @click="placed = null">Dismiss</button>
    </div>

    <div class="mt-8 grid gap-8 lg:grid-cols-3">
      <div class="card overflow-x-auto lg:col-span-2">
        <table class="table-base">
          <thead><tr><th>Product</th><th class="text-right">Retail</th><th class="text-right">10+</th><th class="text-right">50+</th><th class="text-right">200+</th><th class="text-right">Stock</th><th class="w-28">Qty</th></tr></thead>
          <tbody>
            <tr v-for="p in rows" :key="p.id" :class="{ 'bg-brand-50/40': qty[p.id] > 0 }">
              <td><div class="flex items-center gap-3"><img :src="img(p.image, 100)" class="size-10 rounded-lg object-cover" :alt="p.name" /><div><p class="font-semibold">{{ p.name }}</p><p class="text-xs text-slate-500">{{ p.sku }}</p></div></div></td>
              <td class="text-right text-slate-400">{{ money(p.price) }}</td>
              <td v-for="t in p.tiers" :key="t.min_qty" class="text-right tabular-nums" :class="qty[p.id] >= t.min_qty && tierPrice(p, qty[p.id]) === t.unit_price ? 'font-bold text-brand-700' : ''">{{ money(t.unit_price, 2) }}</td>
              <td class="text-right" :class="p.stock < 15 ? 'text-rose-600' : 'text-slate-600'">{{ p.stock }}</td>
              <td><input v-model.number="qty[p.id]" type="number" min="0" :max="p.stock" step="10" class="input !py-1.5" placeholder="0" :disabled="!p.stock" /></td>
            </tr>
          </tbody>
        </table>
      </div>

      <aside class="space-y-6">
        <form class="card sticky top-24 space-y-4 p-6" @submit.prevent="submit">
          <h2 class="font-semibold">Order summary</h2>
          <ul v-if="lines.length" class="space-y-2 text-sm">
            <li v-for="l in lines" :key="l.p.id" class="flex justify-between gap-2"><span class="truncate">{{ l.p.name }} × {{ l.qty }}</span><span class="font-semibold">{{ money(l.qty * l.unit, 2) }}</span></li>
          </ul>
          <p v-else class="text-sm text-slate-500">Enter quantities in the price list.</p>
          <div class="space-y-1 border-t border-slate-100 pt-3 text-sm">
            <div class="flex justify-between text-slate-500"><span>Retail value</span><span class="line-through">{{ money(retail, 2) }}</span></div>
            <div class="flex justify-between text-brand-700"><span>Trade savings</span><span>-{{ money(retail - total, 2) }}</span></div>
            <div class="flex justify-between text-lg font-bold"><span>Total (ex. VAT)</span><span>{{ money(total, 2) }}</span></div>
          </div>
          <p v-if="belowMoq" class="rounded-lg bg-amber-50 p-2 text-xs text-amber-800">Each line needs at least 10 units.</p>
          <p v-else-if="lines.length && total < (data?.min_order_value ?? 500)" class="rounded-lg bg-amber-50 p-2 text-xs text-amber-800">Add {{ money((data?.min_order_value ?? 500) - total, 2) }} more to reach the minimum order.</p>
          <input v-model="company.company" required class="input" placeholder="Company name" />
          <div class="grid grid-cols-2 gap-2"><input v-model="company.vat_number" class="input" placeholder="VAT number" /><input v-model="company.po_reference" class="input" placeholder="PO reference" /></div>
          <input v-model="company.email" required type="email" class="input" placeholder="Accounts email" />
          <button class="btn btn-primary w-full" :disabled="!lines.length || belowMoq">Place order on {{ data?.payment_terms }}</button>
        </form>
      </aside>
    </div>
  </div>
</template>
