import { Boxes, LayoutDashboard } from 'lucide-vue-next'

export default [
  { path: '', component: () => import('./views/DashboardView.vue'), meta: { layout: 'app', title: 'Store dashboard', nav: { label: 'Dashboard', icon: LayoutDashboard, order: 1 } } },
  { path: 'inventory', component: () => import('./views/InventoryView.vue'), meta: { layout: 'app', title: 'Inventory', nav: { label: 'Inventory', icon: Boxes, order: 3 } } },
]
