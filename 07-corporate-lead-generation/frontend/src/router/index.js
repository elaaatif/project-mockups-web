// Routes are collected automatically from every src/modules/*/routes.js file.
//   meta.layout === 'site' → public website shell (SiteLayout)
//   meta.layout === 'app'  → admin/dashboard shell (AppLayout); meta.nav adds it to the sidebar
//   no layout              → bare page
import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import SiteLayout from '@/layouts/SiteLayout.vue'
import { setSeo } from '@/core/seo'

const files = import.meta.glob('../modules/*/routes.js', { eager: true })
const moduleRoutes = Object.values(files).flatMap((m) => m.default)
const byLayout = (layout) => moduleRoutes.filter((r) => (r.meta?.layout ?? 'none') === layout)

export const navItems = byLayout('app').filter((r) => r.meta?.nav).sort((a, b) => a.meta.nav.order - b.meta.nav.order)

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: SiteLayout, children: byLayout('site') },
    { path: '/app', component: AppLayout, children: byLayout('app') },
    ...byLayout('none'),
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
  scrollBehavior: (to, from, saved) => saved ?? (to.hash ? { el: to.hash, behavior: 'smooth' } : { top: 0 }),
})

router.afterEach((to) => {
  setSeo({ title: to.meta.title, description: to.meta.description })
})

export default router
