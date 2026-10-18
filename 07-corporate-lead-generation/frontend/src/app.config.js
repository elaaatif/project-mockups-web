// Branding for this app — the shared layouts, router and SEO helper read from here.
import { Factory } from 'lucide-vue-next'

export default {
  name: 'Vertex Industrial',
  tagline: 'Pumps, valves, drives & automation engineered in Britain',
  description: 'Vertex Industrial designs and manufactures industrial pumps, valves, motors and automation systems, with installation and maintenance across the UK and Europe.',
  logo: Factory,
  searchPlaceholder: 'Search RFQs, companies, candidates…',
  user: { name: 'Daniel Moss', role: 'Head of Sales' },
  promo: { title: '3 hot RFQs today', text: 'Respond within 4 hours to win 2× more', cta: 'Open RFQs', to: '/app/rfqs' },
}
