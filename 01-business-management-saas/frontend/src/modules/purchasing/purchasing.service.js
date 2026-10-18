import { http } from '@/core/http'

export const purchasingService = {
  list: () => http.get('/purchasing'),
  create: (order) => http.post('/purchasing', order),
  advance: (id) => http.patch(`/purchasing/${id}/advance`),
}
