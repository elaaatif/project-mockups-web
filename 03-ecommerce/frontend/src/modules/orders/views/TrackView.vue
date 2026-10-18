<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { CheckCircle2, Circle, PackageSearch, Truck } from 'lucide-vue-next'
import { date, money } from '@/core/format'
import { img } from '@/core/media'
import { ordersService } from '../orders.service'

const route = useRoute()
const form = ref({ order: route.query.order ?? '', email: route.query.email ?? '' })
const order = ref(null)
const error = ref('')
const loading = ref(false)

async function track() {
  loading.value = true
  error.value = ''
  try { order.value = await ordersService.track(form.value.order, form.value.email) } catch (e) { error.value = e.message; order.value = null }
  loading.value = false
}
onMounted(() => form.value.order && form.value.email && track())
const demo = () => { form.value = { order: 'MC-48213', email: 'noah@example.com' }; track() }
</script>

<template>
  <div class="mx-auto max-w-4xl px-6 py-14">
    <div class="text-center">
      <PackageSearch class="mx-auto size-12 text-brand-600" />
      <h1 class="mt-3 font-display text-4xl font-semibold">Track your order</h1>
      <p class="mt-2 text-slate-600">Enter your order number and the email you used at checkout.</p>
    </div>
    <form class="card mx-auto mt-8 flex max-w-2xl flex-wrap gap-3 p-4" @submit.prevent="track">
      <input v-model="form.order" required class="input min-w-40 flex-1" placeholder="Order no. e.g. MC-48213" />
      <input v-model="form.email" required type="email" class="input min-w-52 flex-1" placeholder="Email" />
      <button class="btn btn-primary" :disabled="loading">{{ loading ? 'Searching…' : 'Track' }}</button>
    </form>
    <p class="mt-3 text-center text-sm text-slate-500">No order handy? <button class="font-semibold text-brand-700 underline" @click="demo">Try a demo order</button></p>
    <p v-if="error" class="mx-auto mt-6 max-w-2xl rounded-xl bg-rose-50 p-4 text-center text-sm text-rose-700">{{ error }}</p>

    <div v-if="order" class="card mt-10 overflow-hidden">
      <div class="flex flex-wrap items-center justify-between gap-4 bg-brand-900 p-6 text-white">
        <div><p class="text-sm text-brand-200">Order {{ order.id }}</p><p class="mt-1 text-2xl font-semibold">{{ order.timeline.findLast((t) => t.done).label }}</p></div>
        <div class="text-right text-sm"><p class="flex items-center gap-1.5"><Truck class="size-4" />{{ order.carrier }}</p><p class="font-mono text-brand-200">{{ order.tracking_no }}</p></div>
      </div>
      <div class="p-6">
        <ol class="grid gap-6 sm:grid-cols-6">
          <li v-for="(t, i) in order.timeline" :key="t.key" class="relative flex gap-3 sm:flex-col sm:items-center sm:text-center">
            <span v-if="i" class="absolute top-3 right-1/2 hidden h-0.5 w-full sm:block" :class="t.done ? 'bg-brand-500' : 'bg-slate-200'" />
            <CheckCircle2 v-if="t.done" class="relative z-10 size-6 shrink-0 bg-white text-brand-600" />
            <Circle v-else class="relative z-10 size-6 shrink-0 bg-white text-slate-300" />
            <div><p class="text-sm font-semibold" :class="t.done ? 'text-slate-900' : 'text-slate-400'">{{ t.label }}</p><p class="text-xs text-slate-500">{{ t.at ? date(t.at) : '' }}</p></div>
          </li>
        </ol>
        <div class="mt-8 divide-y divide-slate-100 border-t border-slate-100">
          <div v-for="i in order.items" :key="i.product_id" class="flex items-center gap-3 py-3"><img :src="img(i.image, 120)" class="size-12 rounded-lg object-cover" :alt="i.name" /><span class="flex-1 text-sm">{{ i.name }} × {{ i.qty }}</span><span class="font-semibold">{{ money(i.unit_price * i.qty, 2) }}</span></div>
        </div>
        <p class="mt-3 text-right font-bold">Total {{ money(order.total, 2) }}</p>
      </div>
    </div>
  </div>
</template>
