import { CalendarDays, ClipboardList, Layers } from 'lucide-vue-next'

export default [
  { path: '', component: () => import('./views/CalendarView.vue'), meta: { layout: 'app', title: 'Today', nav: { label: 'Calendar', icon: CalendarDays, order: 1 } } },
  { path: 'bookings', component: () => import('./views/BookingsView.vue'), meta: { layout: 'app', title: 'Bookings', nav: { label: 'Bookings', icon: ClipboardList, order: 2 } } },
  { path: 'services', component: () => import('./views/ServicesView.vue'), meta: { layout: 'app', title: 'Services & team', nav: { label: 'Services & team', icon: Layers, order: 3 } } },
]
