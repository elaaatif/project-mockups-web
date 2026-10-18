// Cart state (persisted in localStorage). Shared by the header, product page, drawer and checkout.
import { computed, reactive, watch } from 'vue'

const KEY = 'mercato-cart'
const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) ?? [] } catch { return [] } }

const state = reactive({ items: load(), open: false })
watch(() => state.items, (v) => localStorage.setItem(KEY, JSON.stringify(v)), { deep: true })

export const FREE_SHIPPING_OVER = 75

export const cart = {
  state,
  count: computed(() => state.items.reduce((s, i) => s + i.qty, 0)),
  subtotal: computed(() => state.items.reduce((s, i) => s + i.qty * i.price, 0)),
  add(p, qty = 1) {
    const found = state.items.find((i) => i.id === p.id)
    if (found) found.qty = Math.min(found.qty + qty, p.stock)
    else state.items.push({ id: p.id, slug: p.slug, name: p.name, price: p.price, image: p.image, stock: p.stock, qty })
    state.open = true
  },
  setQty(id, qty) {
    const item = state.items.find((i) => i.id === id)
    if (item) item.qty = Math.max(1, Math.min(qty, item.stock))
  },
  remove(id) { state.items = state.items.filter((i) => i.id !== id) },
  clear() { state.items = [] },
}
