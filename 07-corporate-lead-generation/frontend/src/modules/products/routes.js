export default [
  { path: 'products', component: () => import('./views/CatalogView.vue'), meta: { layout: 'site', title: 'Product catalogue', description: 'Industrial pumps, valves, IE4 motors, VSDs, PLCs and compressors with full technical specifications and datasheets.' } },
  { path: 'products/:slug', component: () => import('./views/ProductView.vue'), meta: { layout: 'site', title: 'Product' } },
]
