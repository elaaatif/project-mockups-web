import { LayoutDashboard } from 'lucide-vue-next'

export default [
  {
    path: '',
    component: () => import('./views/DashboardView.vue'),
    meta: { layout: 'app', title: 'Dashboard', nav: { label: 'Dashboard', icon: LayoutDashboard, order: 1 } },
  },
]
