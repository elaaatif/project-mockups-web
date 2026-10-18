import { http } from '@/core/http'

export const crmService = {
  overview: () => http.get('/crm/overview'),
  seoAudit: () => http.get('/seo/audit'),
  rfqs: () => http.get('/crm/rfqs'),
  updateRfq: (id, body) => http.patch(`/crm/rfqs/${id}`, body),
  messages: () => http.get('/crm/messages'),
  updateMessage: (id, status) => http.patch(`/crm/messages/${id}`, { status }),
  applications: () => http.get('/crm/applications'),
  updateApplication: (id, status) => http.patch(`/crm/applications/${id}`, { status }),
}
