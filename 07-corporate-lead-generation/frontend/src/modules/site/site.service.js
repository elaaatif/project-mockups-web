import { Cog, Cpu, PenTool, Wrench } from 'lucide-vue-next'
import { http } from '@/core/http'

export const siteService = {
  company: () => http.get('/company'),
  service: (slug) => http.get(`/company/services/${slug}`),
  contact: (body) => http.post('/company/contact', body),
}

export const SERVICE_ICONS = { Cog, Cpu, PenTool, Wrench }
