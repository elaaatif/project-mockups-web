import { Truck } from 'lucide-vue-next'

export default [
  {
    path: 'fleet',
    component: () => import('./views/FleetView.vue'),
    meta: { layout: 'app', title: 'Fleet', nav: { label: 'Fleet & Insurance', icon: Truck, order: 6 } },
  },
]
