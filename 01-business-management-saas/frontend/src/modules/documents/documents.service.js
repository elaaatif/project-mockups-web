import { http } from '@/core/http'

export const documentsService = {
  list: () => http.get('/documents'),
  create: (doc) => http.post('/documents', doc),
  decide: (id, decision, comment) => http.post(`/documents/${id}/decision`, { decision, comment }),
}
