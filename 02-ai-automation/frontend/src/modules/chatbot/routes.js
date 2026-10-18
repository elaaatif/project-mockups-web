import { Bot } from 'lucide-vue-next'

export default [
  {
    path: 'chatbot',
    component: () => import('./views/ChatbotView.vue'),
    meta: { layout: 'app', title: 'AI Chatbot', nav: { label: 'AI Support Chatbot', icon: Bot, order: 2 } },
  },
]
