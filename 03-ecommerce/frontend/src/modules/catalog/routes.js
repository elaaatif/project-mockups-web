export default [
  { path: '', component: () => import('./views/HomeView.vue'), meta: { layout: 'site' } },
  { path: 'shop', component: () => import('./views/ShopView.vue'), meta: { layout: 'site', title: 'Shop' } },
  { path: 'product/:slug', component: () => import('./views/ProductView.vue'), meta: { layout: 'site', title: 'Product' } },
]
