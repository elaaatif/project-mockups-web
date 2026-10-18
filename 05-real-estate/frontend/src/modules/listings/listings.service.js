import { http } from '@/core/http'
import { money } from '@/core/format'

export const listingsService = {
  search: (params = {}) => http.get('/listings?' + new URLSearchParams(Object.entries(params).filter(([, v]) => v !== '' && v != null && v !== 0))),
  meta: () => http.get('/listings/meta'),
  detail: (slug) => http.get(`/listings/${slug}`),
  enquire: (body) => http.post('/leads/enquiry', body),
  slots: (property_id, date) => http.get(`/leads/viewing-slots?property_id=${property_id}&date=${date}`),
  bookViewing: (body) => http.post('/leads/viewings', body),
}

/** "£2.95m" / "£785k" / "£3,400 pcm" */
export function shortPrice(p) {
  if (p.purpose === 'rent') return `${money(p.price)} pcm`
  return p.price >= 1e6 ? `£${(p.price / 1e6).toFixed(2).replace(/\.?0+$/, '')}m` : `£${Math.round(p.price / 1000)}k`
}
