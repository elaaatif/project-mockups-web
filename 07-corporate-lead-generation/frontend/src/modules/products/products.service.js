import { http } from '@/core/http'

export const productsService = {
  categories: () => http.get('/products/categories'),
  list: (params = {}) => http.get('/products?' + new URLSearchParams(Object.entries(params).filter(([, v]) => v))),
  detail: (slug) => http.get(`/products/${slug}`),
}
