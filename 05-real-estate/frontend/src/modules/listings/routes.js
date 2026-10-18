export default [
  { path: '', component: () => import('./views/HomeView.vue'), meta: { layout: 'site' } },
  { path: 'properties', component: () => import('./views/PropertiesView.vue'), meta: { layout: 'site', title: 'Properties' } },
  { path: 'property/:slug', component: () => import('./views/PropertyView.vue'), meta: { layout: 'site', title: 'Property' } },
]
