import { FileSpreadsheet, Inbox, LayoutDashboard, UserCheck } from 'lucide-vue-next'

export default [
  { path: '', component: () => import('./views/CrmDashboardView.vue'), meta: { layout: 'app', title: 'Lead dashboard', nav: { label: 'Dashboard', icon: LayoutDashboard, order: 1 } } },
  { path: 'rfqs', component: () => import('./views/RfqsView.vue'), meta: { layout: 'app', title: 'Quote requests', nav: { label: 'Quote requests', icon: FileSpreadsheet, order: 2 } } },
  { path: 'inbox', component: () => import('./views/InboxView.vue'), meta: { layout: 'app', title: 'Inbox', nav: { label: 'Contact inbox', icon: Inbox, order: 3 } } },
  { path: 'applications', component: () => import('./views/ApplicationsView.vue'), meta: { layout: 'app', title: 'Applications', nav: { label: 'Job applications', icon: UserCheck, order: 4 } } },
]
