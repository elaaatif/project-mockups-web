export default [
  { path: 'my-learning', component: () => import('./views/MyLearningView.vue'), meta: { layout: 'site', title: 'My learning' } },
  { path: 'verify', component: () => import('./views/VerifyView.vue'), meta: { layout: 'site', title: 'Verify a certificate' } },
  { path: '/learn/:slug', component: () => import('./views/PlayerView.vue'), meta: { title: 'Learning' } },
  { path: '/certificate/:id', component: () => import('./views/CertificateView.vue'), meta: { title: 'Certificate' } },
]
