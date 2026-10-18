import { http } from '@/core/http'

export const catalogService = {
  categories: () => http.get('/catalog/categories'),
  products: (params = {}) => http.get('/catalog/products?' + new URLSearchParams(Object.entries(params).filter(([, v]) => v !== '' && v != null && v !== false))),
  product: (slug) => http.get(`/catalog/products/${slug}`),
}
