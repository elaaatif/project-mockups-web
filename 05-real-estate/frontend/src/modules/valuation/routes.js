export default [
  { path: 'valuation', component: () => import('./views/ValuationView.vue'), meta: { layout: 'site', title: 'Instant valuation' } },
  { path: 'list-your-property', component: () => import('./views/ListPropertyView.vue'), meta: { layout: 'site', title: 'List your property' } },
]
