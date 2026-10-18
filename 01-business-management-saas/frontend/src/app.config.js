// Branding for this app — the shared layout and router read from here.
import { Workflow } from 'lucide-vue-next'

export default {
  name: 'OpsFlow',
  tagline: 'Business Management Platform',
  logo: Workflow,
  searchPlaceholder: 'Search invoices, items, employees…',
  user: { name: 'Amira Haddad', role: 'Admin · Northstar Ltd' },
  promo: { title: 'Growth plan trial', text: '12 days left · unlock payroll & fleet', cta: 'Upgrade', to: '/#pricing' },
}
