<script setup>
import { computed } from 'vue'
import { Minus, Plus, ShoppingBag, Trash2, Truck, X } from 'lucide-vue-next'
import { money } from '@/core/format'
import { img } from '@/core/media'
import { cart, FREE_SHIPPING_OVER } from '../cart.store'

const remaining = computed(() => Math.max(0, FREE_SHIPPING_OVER - cart.subtotal.value))
</script>

<template>
  <Teleport to="body">
    <Transition enter-from-class="opacity-0" leave-to-class="opacity-0" enter-active-class="transition" leave-active-class="transition">
      <div v-if="cart.state.open" class="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm" @click="cart.state.open = false" />
    </Transition>
    <Transition enter-from-class="translate-x-full" leave-to-class="translate-x-full" enter-active-class="transition duration-300" leave-active-class="transition duration-200">
      <aside v-if="cart.state.open" class="fixed inset-y-0 right-0 z-50 flex w-full max-w-md flex-col bg-white shadow-2xl">
        <div class="flex items-center justify-between border-b border-slate-100 px-6 py-5">
          <h2 class="font-display text-xl font-semibold">Your bag ({{ cart.count.value }})</h2>
          <button class="rounded-full p-2 hover:bg-slate-100" @click="cart.state.open = false"><X class="size-5" /></button>
        </div>
        <div v-if="cart.state.items.length" class="border-b border-slate-100 px-6 py-3 text-sm">
          <p class="flex items-center gap-2"><Truck class="size-4 text-brand-600" />
            <span v-if="remaining">Add <strong>{{ money(remaining, 2) }}</strong> for free shipping</span><span v-else class="font-semibold text-brand-700">You've unlocked free shipping 🎉</span></p>
          <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-brand-500 transition-all" :style="{ width: Math.min(100, (cart.subtotal.value / FREE_SHIPPING_OVER) * 100) + '%' }" /></div>
        </div>
        <ul class="flex-1 divide-y divide-slate-100 overflow-y-auto px-6">
          <li v-for="i in cart.state.items" :key="i.id" class="flex gap-4 py-5">
            <img :src="img(i.image, 200)" :alt="i.name" class="size-20 rounded-xl bg-slate-100 object-cover" />
            <div class="flex flex-1 flex-col">
              <div class="flex justify-between gap-2"><RouterLink :to="`/product/${i.slug}`" class="font-semibold hover:text-brand-700" @click="cart.state.open = false">{{ i.name }}</RouterLink><p class="font-semibold">{{ money(i.price * i.qty, 2) }}</p></div>
              <p class="text-sm text-slate-500">{{ money(i.price, 2) }} each</p>
              <div class="mt-auto flex items-center justify-between">
                <div class="flex items-center rounded-full ring-1 ring-slate-200">
                  <button class="p-2 hover:text-brand-700" @click="cart.setQty(i.id, i.qty - 1)"><Minus class="size-3.5" /></button>
                  <span class="w-6 text-center text-sm font-semibold">{{ i.qty }}</span>
                  <button class="p-2 hover:text-brand-700" @click="cart.setQty(i.id, i.qty + 1)"><Plus class="size-3.5" /></button>
                </div>
                <button class="text-slate-400 hover:text-rose-600" @click="cart.remove(i.id)"><Trash2 class="size-4" /></button>
              </div>
            </div>
          </li>
        </ul>
        <div v-if="!cart.state.items.length" class="grid flex-1 place-items-center p-10 text-center">
          <div><ShoppingBag class="mx-auto size-12 text-slate-300" /><p class="mt-3 font-semibold">Your bag is empty</p>
            <RouterLink to="/shop" class="btn btn-primary mt-5" @click="cart.state.open = false">Start shopping</RouterLink></div>
        </div>
        <div v-else class="border-t border-slate-100 p-6">
          <div class="flex justify-between text-lg font-bold"><span>Subtotal</span><span>{{ money(cart.subtotal.value, 2) }}</span></div>
          <p class="mt-1 text-xs text-slate-500">Taxes included. Shipping calculated at checkout.</p>
          <RouterLink to="/checkout" class="btn btn-primary mt-4 w-full !py-3.5" @click="cart.state.open = false">Checkout</RouterLink>
        </div>
      </aside>
    </Transition>
  </Teleport>
</template>
