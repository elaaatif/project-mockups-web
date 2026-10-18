import { FileText } from 'lucide-vue-next'

export default [
  { path: 'quote', component: () => import('./views/QuoteRequestView.vue'), meta: { layout: 'site', title: 'Request a quote' } },
  {
    path: 'quotes',
    component: () => import('./views/QuotesAdminView.vue'),
    meta: { layout: 'app', title: 'Quotes', nav: { label: 'Quote requests', icon: FileText, order: 4 } },
  },
]
