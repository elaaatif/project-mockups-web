import { CalendarClock, Kanban, LayoutDashboard } from 'lucide-vue-next'

export default [
  { path: '', component: () => import('./views/AgentDashboardView.vue'), meta: { layout: 'app', title: 'Agent dashboard', nav: { label: 'Dashboard', icon: LayoutDashboard, order: 1 } } },
  { path: 'leads', component: () => import('./views/PipelineView.vue'), meta: { layout: 'app', title: 'Leads', nav: { label: 'Lead pipeline', icon: Kanban, order: 2 } } },
  { path: 'viewings', component: () => import('./views/ViewingsView.vue'), meta: { layout: 'app', title: 'Viewings', nav: { label: 'Viewings', icon: CalendarClock, order: 3 } } },
]
