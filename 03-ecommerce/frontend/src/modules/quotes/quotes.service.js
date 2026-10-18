import { http } from '@/core/http'

export const quotesService = {
  request: (body) => http.post('/quotes', body),
  list: () => http.get('/quotes'),
  respond: (id, body) => http.patch(`/quotes/${id}`, body),
}
