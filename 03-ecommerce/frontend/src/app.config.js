// Branding for this app — the shared layouts and router read from here.
import { ShoppingBag } from 'lucide-vue-next'

export default {
  name: 'Mercato',
  tagline: 'Design-led goods',
  logo: ShoppingBag,
  searchPlaceholder: 'Search orders, products, quotes…',
  user: { name: 'Priya Shah', role: 'Store manager' },
  promo: { title: 'View storefront', text: 'See the shop as customers do', cta: 'Open shop', to: '/' },
}
