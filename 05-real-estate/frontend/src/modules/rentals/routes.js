import { KeyRound } from 'lucide-vue-next'

export default [
  { path: 'rentals', component: () => import('./views/RentalsView.vue'), meta: { layout: 'app', title: 'Rental management', nav: { label: 'Rental management', icon: KeyRound, order: 4 } } },
]
