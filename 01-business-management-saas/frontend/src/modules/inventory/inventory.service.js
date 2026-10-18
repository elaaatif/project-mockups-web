import { http } from '@/core/http'

export const inventoryService = {
  list: (params = {}) => http.get('/inventory?' + new URLSearchParams(Object.entries(params).filter(([, v]) => v))),
  create: (item) => http.post('/inventory', item),
  adjust: (sku, delta) => http.patch(`/inventory/${sku}/adjust`, { delta }),
}
