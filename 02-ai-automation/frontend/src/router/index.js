// Routes are collected automatically from every src/modules/*/routes.js file.
// A route with meta.layout === 'app' renders inside the dashboard shell; meta.nav adds it to the sidebar.
import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import config from '@/app.config'

const files = import.meta.glob('../modules/*/routes.js', { eager: true })
const moduleRoutes = Object.values(files).flatMap((m) => m.default)

const appRoutes = moduleRoutes.filter((r) => r.meta?.layout === 'app')
const publicRoutes = moduleRoutes.filter((r) => r.meta?.layout !== 'app')

export const navItems = appRoutes.filter((r) => r.meta?.nav).sort((a, b) => a.meta.nav.order - b.meta.nav.order)

const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...publicRoutes,
    { path: '/app', component: AppLayout, children: appRoutes },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
  scrollBehavior: (to) => (to.hash ? { el: to.hash, behavior: 'smooth' } : { top: 0 }),
})

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} · ${config.name}` : `${config.name} · ${config.tagline}`
})

export default router
