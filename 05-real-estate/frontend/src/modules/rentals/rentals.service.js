import { http } from '@/core/http'

export const rentalsService = {
  overview: () => http.get('/rentals'),
  markPaid: (id) => http.post(`/rentals/payments/${id}/paid`),
  openTicket: (body) => http.post('/rentals/tickets', body),
  setTicket: (id, status) => http.patch(`/rentals/tickets/${id}`, { status }),
}
