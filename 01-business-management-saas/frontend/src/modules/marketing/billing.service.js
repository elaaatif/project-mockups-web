import { http } from '@/core/http'

export const billingService = {
  plans: () => http.get('/billing/plans'),
}
