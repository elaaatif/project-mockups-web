import { http } from '@/core/http'

export const valuationService = {
  estimate: (body) => http.post('/leads/valuation', body),
  districts: () => http.get('/listings/meta'),
  plans: () => http.get('/plans'),
}
