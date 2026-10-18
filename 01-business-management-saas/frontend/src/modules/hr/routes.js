import { Users } from 'lucide-vue-next'

export default [
  {
    path: 'hr',
    component: () => import('./views/HrView.vue'),
    meta: { layout: 'app', title: 'People & Payroll', nav: { label: 'HR & Payroll', icon: Users, order: 5 } },
  },
]
