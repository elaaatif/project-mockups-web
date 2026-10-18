import { http } from '@/core/http'

export const academyService = {
  overview: () => http.get('/academy'),
  addStudent: (body) => http.post('/academy/students', body),
  pay: (id) => http.post(`/academy/students/${id}/payment`),
  attendance: (student_id, status) => http.post('/academy/attendance', { student_id, status }),
}
