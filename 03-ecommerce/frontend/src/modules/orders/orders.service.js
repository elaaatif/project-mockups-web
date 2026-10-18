import { http } from '@/core/http'

export const ordersService = {
  checkout: (body) => http.post('/orders', body),
  track: (order_id, email) => http.get('/orders/track?' + new URLSearchParams({ order_id, email })),
  list: () => http.get('/orders'),
  advance: (id) => http.patch(`/orders/${id}/advance`),
}
