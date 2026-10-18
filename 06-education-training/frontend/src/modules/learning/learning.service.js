import { http } from '@/core/http'

export const learningService = {
  myCourses: () => http.get('/learning/my-courses'),
  enroll: (slug, name = 'Alex Morgan') => http.post(`/learning/${slug}/enroll`, { name }),
  progress: (slug) => http.get(`/learning/${slug}/progress`),
  complete: (slug, lessonId) => http.post(`/learning/${slug}/lessons/${lessonId}/complete`),
  quiz: (slug) => http.get(`/learning/${slug}/quiz`),
  submitQuiz: (slug, answers) => http.post(`/learning/${slug}/quiz`, { answers }),
  certificate: (id) => http.get(`/learning/certificates/${encodeURIComponent(id)}`),
}
