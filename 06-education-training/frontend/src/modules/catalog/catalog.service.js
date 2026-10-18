import { http } from '@/core/http'

export const catalogService = {
  categories: () => http.get('/courses/categories'),
  list: (params = {}) => http.get('/courses?' + new URLSearchParams(Object.entries(params).filter(([, v]) => v))),
  detail: (slug) => http.get(`/courses/${slug}`),
  plans: () => http.get('/plans'),
}
