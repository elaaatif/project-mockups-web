import { http } from '@/core/http'

export const invoicesService = {
  list: () => http.get('/invoices'),
  create: (invoice) => http.post('/invoices', invoice),
  markPaid: (id) => http.patch(`/invoices/${id}/pay`),
}
