import { BarChart3 } from 'lucide-vue-next'

export default [
  {
    path: 'reports',
    component: () => import('./views/ReportsView.vue'),
    meta: { layout: 'app', title: 'Automated reports', nav: { label: 'Automated Reports', icon: BarChart3, order: 4 } },
  },
]
