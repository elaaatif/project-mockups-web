import { http } from '@/core/http'

export const reportsService = {
  templates: () => http.get('/reports/templates'),
  generate: (template_id, period) => http.post('/reports/generate', { template_id, period }),
  schedules: () => http.get('/reports/schedules'),
  schedule: (body) => http.post('/reports/schedules', body),
  unschedule: (id) => http.delete(`/reports/schedules/${id}`),
}
