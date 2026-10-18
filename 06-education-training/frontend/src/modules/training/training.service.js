import { http } from '@/core/http'

export const trainingService = {
  overview: () => http.get('/training'),
  assign: (body) => http.post('/training/assign', body),
  remind: (id) => http.post(`/training/assignments/${id}/remind`),
  courses: () => http.get('/courses'),
}
