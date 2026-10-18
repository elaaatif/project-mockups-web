import { Receipt } from 'lucide-vue-next'

export default [
  {
    path: 'invoices',
    component: () => import('./views/InvoicesView.vue'),
    meta: { layout: 'app', title: 'Invoices', nav: { label: 'Invoicing', icon: Receipt, order: 3 } },
  },
]
