import { http } from '@/core/http'

export const portfolioService = {
  profile: () => http.get('/profile'),
  projects: () => http.get('/projects'),
  status: () => http.get('/projects/status'),
  project: (slug) => http.get(`/projects/${slug}`),
  options: () => http.get('/contact/options'),
  estimate: (body) => http.post('/contact/estimate', body),
  send: (body) => http.post('/contact', body),
  messages: () => http.get('/contact/messages'),
  setStatus: (id, status) => http.patch(`/contact/messages/${id}`, { status }),
}
