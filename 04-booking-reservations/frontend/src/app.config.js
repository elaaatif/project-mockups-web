// Branding for this app — the shared layouts and router read from here.
import { CalendarCheck } from 'lucide-vue-next'

export default {
  name: 'Bookly',
  tagline: 'Book anything, instantly',
  logo: CalendarCheck,
  searchPlaceholder: 'Search bookings, customers…',
  user: { name: 'Chloe Dubois', role: 'Owner' },
  promo: { title: 'Your booking page', text: 'Share it on Instagram & Google', cta: 'Open public page', to: '/explore' },
}
