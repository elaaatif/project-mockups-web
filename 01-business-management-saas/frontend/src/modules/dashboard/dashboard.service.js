import { http } from '@/core/http'

export const dashboardService = {
  overview: () => http.get('/dashboard'),
}
