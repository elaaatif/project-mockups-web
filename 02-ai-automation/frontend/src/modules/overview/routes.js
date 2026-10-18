import { LayoutDashboard } from 'lucide-vue-next'

export default [
  {
    path: '',
    component: () => import('./views/OverviewView.vue'),
    meta: { layout: 'app', title: 'Overview', nav: { label: 'Overview', icon: LayoutDashboard, order: 1 } },
  },
]
