import { ShieldCheck } from 'lucide-vue-next'

export default [
  { path: '', component: () => import('./views/TrainingView.vue'), meta: { layout: 'app', title: 'Employee training', nav: { label: 'Employee training', icon: ShieldCheck, order: 1 } } },
]
