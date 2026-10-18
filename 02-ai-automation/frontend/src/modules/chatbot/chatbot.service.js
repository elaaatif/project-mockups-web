import { http } from '@/core/http'

export const chatbotService = {
  send: (message) => http.post('/chatbot/message', { message }),
  conversations: () => http.get('/chatbot/conversations'),
}
