import { School } from 'lucide-vue-next'

export default [
  { path: 'academy', component: () => import('./views/AcademyView.vue'), meta: { layout: 'app', title: 'Training centre', nav: { label: 'Training centre admin', icon: School, order: 2 } } },
]
