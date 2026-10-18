// Branding for this app — the shared layouts and router read from here.
import { House } from 'lucide-vue-next'

export default {
  name: 'Haven',
  tagline: 'London Real Estate',
  logo: House,
  searchPlaceholder: 'Search leads, properties, tenants…',
  user: { name: 'Sophie Bennett', role: 'Senior Sales Agent' },
  promo: { title: '3 viewings today', text: 'Next: 10:30 · Contemporary villa', cta: 'Open schedule', to: '/app/viewings' },
}
