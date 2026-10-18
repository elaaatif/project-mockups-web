import { ShoppingCart } from 'lucide-vue-next'

export default [
  {
    path: 'purchasing',
    component: () => import('./views/PurchasingView.vue'),
    meta: { layout: 'app', title: 'Purchasing', nav: { label: 'Purchasing', icon: ShoppingCart, order: 4 } },
  },
]
