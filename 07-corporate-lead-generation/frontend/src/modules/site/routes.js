export default [
  { path: '', component: () => import('./views/HomeView.vue'), meta: { layout: 'site' } },
  { path: 'about', component: () => import('./views/AboutView.vue'), meta: { layout: 'site', title: 'About us', description: 'Since 1987 Vertex Industrial has engineered pumps, valves and automation for 62 countries.' } },
  { path: 'services/:slug', component: () => import('./views/ServiceView.vue'), meta: { layout: 'site', title: 'Services' } },
  { path: 'contact', component: () => import('./views/ContactView.vue'), meta: { layout: 'site', title: 'Contact us', description: 'Talk to Vertex Industrial sales, service or support. 24/7 service hotline.' } },
]
