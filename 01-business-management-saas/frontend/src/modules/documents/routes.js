import { FileCheck } from 'lucide-vue-next'

export default [
  {
    path: 'documents',
    component: () => import('./views/DocumentsView.vue'),
    meta: { layout: 'app', title: 'Documents', nav: { label: 'Documents & Approvals', icon: FileCheck, order: 7 } },
  },
]
