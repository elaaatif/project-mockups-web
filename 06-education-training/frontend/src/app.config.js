// Branding for this app — the shared layouts and router read from here.
import { GraduationCap } from 'lucide-vue-next'

export default {
  name: 'Brightpath',
  tagline: 'Learn skills that matter',
  logo: GraduationCap,
  searchPlaceholder: 'Search employees, courses, students…',
  user: { name: 'Nadia Hassan', role: 'L&D Manager · Northwind' },
  promo: { title: 'Compliance deadline', text: 'Cyber Security due in 14 days', cta: 'Send reminders', to: '/app' },
}
