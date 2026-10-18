import { Boxes } from 'lucide-vue-next'

export default [
  {
    path: 'inventory',
    component: () => import('./views/InventoryView.vue'),
    meta: { layout: 'app', title: 'Inventory', nav: { label: 'Inventory', icon: Boxes, order: 2 } },
  },
]
