// Which business the owner is managing (persisted). Demo accounts can switch between all businesses.
import { ref, watch } from 'vue'

const KEY = 'bookly-business'
let initial = 'studio-rouge'
try { initial = localStorage.getItem(KEY) || initial } catch { /* storage unavailable */ }

export const currentBusiness = ref(initial)
watch(currentBusiness, (v) => { try { localStorage.setItem(KEY, v) } catch { /* ignore */ } })
