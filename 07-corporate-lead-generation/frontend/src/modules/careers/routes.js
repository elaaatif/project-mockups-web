export default [
  { path: 'careers', component: () => import('./views/CareersView.vue'), meta: { layout: 'site', title: 'Careers', description: 'Engineering, manufacturing, service and sales jobs at Vertex Industrial. Graduate programme and apprenticeships.' } },
  { path: 'careers/:slug', component: () => import('./views/JobView.vue'), meta: { layout: 'site', title: 'Job' } },
]
