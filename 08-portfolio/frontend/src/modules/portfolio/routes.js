import { Inbox } from 'lucide-vue-next'

export default [
  { path: '', component: () => import('./views/HomeView.vue'), meta: { layout: 'site' } },
  { path: 'work/:slug', component: () => import('./views/CaseStudyView.vue'), meta: { layout: 'site', title: 'Case study' } },
  { path: '', component: () => import('./views/InboxView.vue'), meta: { layout: 'app', title: 'Inbox', nav: { label: 'Project enquiries', icon: Inbox, order: 1 } } },
]
