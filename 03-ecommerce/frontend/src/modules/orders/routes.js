import { Receipt } from 'lucide-vue-next'

export default [
  { path: 'track', component: () => import('./views/TrackView.vue'), meta: { layout: 'site', title: 'Track your order' } },
  {
    path: 'orders',
    component: () => import('./views/OrdersAdminView.vue'),
    meta: { layout: 'app', title: 'Orders', nav: { label: 'Orders', icon: Receipt, order: 2 } },
  },
]
