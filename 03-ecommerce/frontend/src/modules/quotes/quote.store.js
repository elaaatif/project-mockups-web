// Quote request list (RFQ) — like a cart, but for bulk pricing requests. Persisted in localStorage.
import { reactive, watch } from 'vue'

const KEY = 'mercato-quote'
const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) ?? [] } catch { return [] } }

export const quoteList = reactive({
  items: load(),
  add(p, qty = 25) {
    const found = this.items.find((i) => i.id === p.id)
    if (found) found.qty += qty
    else this.items.push({ id: p.id, slug: p.slug, name: p.name, image: p.image, price: p.price, qty })
  },
  remove(id) { this.items = this.items.filter((i) => i.id !== id) },
  clear() { this.items = [] },
})
watch(() => quoteList.items, (v) => localStorage.setItem(KEY, JSON.stringify(v)), { deep: true })
