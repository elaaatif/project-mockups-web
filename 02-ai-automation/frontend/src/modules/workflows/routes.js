import { Workflow } from 'lucide-vue-next'

export default [
  {
    path: 'workflows',
    component: () => import('./views/WorkflowsView.vue'),
    meta: { layout: 'app', title: 'Workflows', nav: { label: 'Email & WhatsApp Flows', icon: Workflow, order: 5 } },
  },
]
