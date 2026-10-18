import { http } from '@/core/http'

export const agentService = {
  overview: () => http.get('/agent/overview'),
  pipeline: () => http.get('/agent/pipeline'),
  move: (id, stage) => http.patch(`/agent/leads/${id}`, { stage }),
  appointments: () => http.get('/agent/appointments'),
}
