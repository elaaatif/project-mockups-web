export default [
  { path: '', component: () => import('./views/HomeView.vue'), meta: { layout: 'site' } },
  { path: 'explore', component: () => import('./views/ExploreView.vue'), meta: { layout: 'site', title: 'Explore' } },
  { path: 'b/:slug', component: () => import('./views/BusinessView.vue'), meta: { layout: 'site', title: 'Book' } },
]
