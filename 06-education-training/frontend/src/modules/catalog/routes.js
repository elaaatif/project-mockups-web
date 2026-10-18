export default [
  { path: '', component: () => import('./views/HomeView.vue'), meta: { layout: 'site' } },
  { path: 'courses', component: () => import('./views/CoursesView.vue'), meta: { layout: 'site', title: 'Courses' } },
  { path: 'course/:slug', component: () => import('./views/CourseView.vue'), meta: { layout: 'site', title: 'Course' } },
  { path: 'pricing', component: () => import('./views/PricingView.vue'), meta: { layout: 'site', title: 'Plans & licences' } },
]
