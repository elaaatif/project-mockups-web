import { FileScan } from 'lucide-vue-next'

export default [
  {
    path: 'extraction',
    component: () => import('./views/ExtractionView.vue'),
    meta: { layout: 'app', title: 'Document extraction', nav: { label: 'Document Extraction', icon: FileScan, order: 3 } },
  },
]
