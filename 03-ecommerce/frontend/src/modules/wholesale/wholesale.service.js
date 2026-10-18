import { http } from '@/core/http'

export const wholesaleService = {
  priceList: () => http.get('/wholesale/price-list'),
  order: (body) => http.post('/wholesale/orders', body),
}

/** Same tier rule as the backend — used for the live preview. */
export function tierPrice(product, qty) {
  const tier = [...product.tiers].reverse().find((t) => qty >= t.min_qty)
  return tier ? tier.unit_price : product.price
}
