import { http } from '@/core/http'

export const ownerService = {
  businesses: () => http.get('/businesses'),
  overview: (slug, date) => http.get(`/dashboard/${slug}` + (date ? `?date=${date}` : '')),
  bookings: (slug, status) => http.get(`/dashboard/${slug}/bookings` + (status ? `?status=${status}` : '')),
  business: (slug) => http.get(`/businesses/${slug}`),
}
