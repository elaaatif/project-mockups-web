// Branding for this app — the shared layout and router read from here.
import { Sparkles } from 'lucide-vue-next'

export default {
  name: 'Autom8',
  tagline: 'AI Automation for Business',
  logo: Sparkles,
  searchPlaceholder: 'Search workflows, conversations, documents…',
  user: { name: 'Jordan Blake', role: 'Ops Lead · Lumen Home' },
  promo: { title: '8,087 tasks automated', text: '≈ 539 hours saved this month', cta: 'See ROI', to: '/app' },
}
