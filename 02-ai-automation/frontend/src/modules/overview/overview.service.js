import { http } from '@/core/http'

export const overviewService = {
  get: () => http.get('/overview'),
}
