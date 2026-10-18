<script setup>
import { computed, ref } from 'vue'
import { Banknote, CheckCircle2, CreditCard, Lock, Wallet } from 'lucide-vue-next'
import { act } from '@/core/resource'
import { money } from '@/core/format'
import { img } from '@/core/media'
import { ordersService } from '@/modules/orders/orders.service'
import { cart, FREE_SHIPPING_OVER } from '../cart.store'

const step = ref(1)
const customer = ref({ name: '', email: '', address: '', city: '', country: 'United Kingdom' })
const shipping = ref('standard')
const payment = ref('card')
const placing = ref(false)
const order = ref(null)

const shippingCost = computed(() => (shipping.value === 'express' ? 12.9 : cart.subtotal.value >= FREE_SHIPPING_OVER ? 0 : 4.9))
const total = computed(() => cart.subtotal.value + shippingCost.value)

async function place() {
  placing.value = true
  const body = { customer: customer.value, shipping: shipping.value, payment: payment.value, items: cart.state.items.map((i) => ({ product_id: i.id, qty: i.qty })) }
  const res = await act(() => ordersService.checkout(body))
  placing.value = false
  if (res) { order.value = res; cart.clear() }
}
</script>

<template>
  <div class="mx-auto max-w-6xl px-6 py-12">
    <!-- Confirmation -->
    <div v-if="order" class="mx-auto max-w-2xl text-center">
      <CheckCircle2 class="mx-auto size-16 text-brand-600" />
      <h1 class="mt-4 font-display text-4xl font-semibold">Thank you, {{ order.customer.name.split(' ')[0] }}!</h1>
      <p class="mt-2 text-slate-600">Order <strong>{{ order.id }}</strong> is confirmed. A receipt is on its way to {{ order.customer.email }}.</p>
      <div class="card mt-8 p-6 text-left">
        <div v-for="i in order.items" :key="i.product_id" class="flex items-center gap-3 py-2"><img :src="img(i.image, 120)" class="size-12 rounded-lg object-cover" :alt="i.name" /><span class="flex-1 text-sm">{{ i.name }} × {{ i.qty }}</span><span class="font-semibold">{{ money(i.unit_price * i.qty, 2) }}</span></div>
        <div class="mt-3 flex justify-between border-t border-slate-100 pt-3 font-bold"><span>Total paid</span><span>{{ money(order.total, 2) }}</span></div>
      </div>
      <RouterLink :to="{ path: '/track', query: { order: order.id, email: order.customer.email } }" class="btn btn-primary mt-8">Track this order</RouterLink>
    </div>

    <div v-else-if="!cart.state.items.length" class="py-24 text-center"><p class="font-display text-3xl">Your bag is empty</p><RouterLink to="/shop" class="btn btn-primary mt-6">Go shopping</RouterLink></div>

    <div v-else class="grid gap-10 lg:grid-cols-5">
      <div class="lg:col-span-3">
        <div class="mb-8 flex gap-2">
          <div v-for="(s, i) in ['Details', 'Delivery', 'Payment']" :key="s" class="flex flex-1 items-center gap-2 text-sm font-semibold" :class="step > i ? 'text-brand-700' : 'text-slate-400'">
            <span class="grid size-7 place-items-center rounded-full text-xs" :class="step > i ? 'bg-brand-600 text-white' : 'bg-slate-200'">{{ i + 1 }}</span>{{ s }}
            <span v-if="i < 2" class="h-px flex-1" :class="step > i + 1 ? 'bg-brand-500' : 'bg-slate-200'" />
          </div>
        </div>

        <form v-if="step === 1" class="card grid gap-4 p-6 sm:grid-cols-2" @submit.prevent="step = 2">
          <div class="sm:col-span-2"><label class="label">Full name</label><input v-model="customer.name" required minlength="2" class="input" /></div>
          <div class="sm:col-span-2"><label class="label">Email</label><input v-model="customer.email" type="email" required class="input" /></div>
          <div class="sm:col-span-2"><label class="label">Address</label><input v-model="customer.address" required minlength="3" class="input" /></div>
          <div><label class="label">City</label><input v-model="customer.city" required class="input" /></div>
          <div><label class="label">Country</label><select v-model="customer.country" class="input"><option>United Kingdom</option><option>Ireland</option><option>France</option><option>Germany</option><option>Netherlands</option></select></div>
          <button class="btn btn-primary sm:col-span-2">Continue to delivery</button>
        </form>

        <div v-else-if="step === 2" class="card space-y-3 p-6">
          <label v-for="o in [['standard', 'Standard · 2–4 business days', cart.subtotal.value >= FREE_SHIPPING_OVER ? 0 : 4.9], ['express', 'Express · next business day', 12.9]]" :key="o[0]"
                 class="flex cursor-pointer items-center gap-3 rounded-xl p-4 ring-1" :class="shipping === o[0] ? 'bg-brand-50 ring-brand-500' : 'ring-slate-200'">
            <input v-model="shipping" type="radio" :value="o[0]" class="accent-brand-600" /><span class="flex-1 font-medium">{{ o[1] }}</span><span class="font-semibold">{{ o[2] ? money(o[2], 2) : 'Free' }}</span>
          </label>
          <div class="flex gap-2 pt-2"><button class="btn btn-ghost" @click="step = 1">Back</button><button class="btn btn-primary flex-1" @click="step = 3">Continue to payment</button></div>
        </div>

        <div v-else class="card space-y-3 p-6">
          <label v-for="o in [['card', 'Credit / debit card', CreditCard], ['paypal', 'PayPal', Wallet], ['cod', 'Cash on delivery', Banknote]]" :key="o[0]"
                 class="flex cursor-pointer items-center gap-3 rounded-xl p-4 ring-1" :class="payment === o[0] ? 'bg-brand-50 ring-brand-500' : 'ring-slate-200'">
            <input v-model="payment" type="radio" :value="o[0]" class="accent-brand-600" /><component :is="o[2]" class="size-5 text-slate-500" /><span class="font-medium">{{ o[1] }}</span>
          </label>
          <div v-if="payment === 'card'" class="grid grid-cols-3 gap-3 rounded-xl bg-slate-50 p-4">
            <input class="input col-span-3" placeholder="4242 4242 4242 4242" /><input class="input col-span-2" placeholder="MM / YY" /><input class="input" placeholder="CVC" />
          </div>
          <div class="flex gap-2 pt-2"><button class="btn btn-ghost" @click="step = 2">Back</button>
            <button class="btn btn-primary flex-1 !py-3.5" :disabled="placing" @click="place"><Lock class="size-4" />{{ placing ? 'Placing order…' : `Pay ${money(total, 2)}` }}</button></div>
          <p class="text-center text-xs text-slate-400">Demo checkout — no real payment is taken.</p>
        </div>
      </div>

      <aside class="lg:col-span-2">
        <div class="card sticky top-24 p-6">
          <h2 class="font-semibold">Order summary</h2>
          <ul class="mt-4 space-y-3">
            <li v-for="i in cart.state.items" :key="i.id" class="flex items-center gap-3">
              <span class="relative"><img :src="img(i.image, 120)" class="size-14 rounded-lg object-cover" :alt="i.name" /><span class="absolute -top-2 -right-2 grid size-5 place-items-center rounded-full bg-slate-700 text-[10px] font-bold text-white">{{ i.qty }}</span></span>
              <span class="flex-1 text-sm">{{ i.name }}</span><span class="text-sm font-semibold">{{ money(i.price * i.qty, 2) }}</span>
            </li>
          </ul>
          <div class="mt-5 space-y-2 border-t border-slate-100 pt-4 text-sm">
            <div class="flex justify-between"><span class="text-slate-500">Subtotal</span><span>{{ money(cart.subtotal.value, 2) }}</span></div>
            <div class="flex justify-between"><span class="text-slate-500">Shipping</span><span>{{ shippingCost ? money(shippingCost, 2) : 'Free' }}</span></div>
            <div class="flex justify-between text-xs text-slate-400"><span>Incl. 20% VAT</span><span>{{ money(cart.subtotal.value / 6, 2) }}</span></div>
            <div class="flex justify-between border-t border-slate-100 pt-3 text-lg font-bold"><span>Total</span><span>{{ money(total, 2) }}</span></div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>
