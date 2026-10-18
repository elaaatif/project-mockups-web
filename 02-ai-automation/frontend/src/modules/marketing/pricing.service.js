import { http } from '@/core/http'

export const pricingService = {
  plans: () => http.get('/pricing'),
}
