import { http } from '@/core/http'

export const adminService = {
  overview: () => http.get('/admin/overview'),
  inventory: () => http.get('/admin/inventory'),
  restock: (slug, qty) => http.post(`/admin/inventory/${slug}/restock`, { qty }),
}
