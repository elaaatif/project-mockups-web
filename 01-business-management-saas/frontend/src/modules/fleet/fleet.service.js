import { http } from '@/core/http'

export const fleetService = {
  list: () => http.get('/fleet'),
  logService: (id, body) => http.post(`/fleet/${id}/service`, body),
  renewInsurance: (id) => http.post(`/fleet/${id}/renew-insurance`),
}
