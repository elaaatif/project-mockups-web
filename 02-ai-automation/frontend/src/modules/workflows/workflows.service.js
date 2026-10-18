import {
  Brain, Clock, ClipboardList, GitBranch, Hash, Mail, MessageCircle, Send, Server, ShoppingBag, Sparkles, Table2, Users,
} from 'lucide-vue-next'
import { http } from '@/core/http'

export const workflowsService = {
  list: () => http.get('/workflows'),
  create: (wf) => http.post('/workflows', wf),
  toggle: (id) => http.patch(`/workflows/${id}/toggle`),
  test: (id) => http.post(`/workflows/${id}/test`),
}

// Presentation metadata for each step type (icon + colour)
export const STEP_META = {
  email_received: { icon: Mail, tone: 'bg-sky-100 text-sky-700' },
  whatsapp_message: { icon: MessageCircle, tone: 'bg-emerald-100 text-emerald-700' },
  form_submitted: { icon: ClipboardList, tone: 'bg-slate-100 text-slate-700' },
  schedule: { icon: Clock, tone: 'bg-amber-100 text-amber-700' },
  new_order: { icon: ShoppingBag, tone: 'bg-pink-100 text-pink-700' },
  ai_classify: { icon: Brain, tone: 'bg-brand-100 text-brand-700' },
  ai_extract: { icon: Sparkles, tone: 'bg-brand-100 text-brand-700' },
  ai_reply: { icon: Sparkles, tone: 'bg-brand-100 text-brand-700' },
  ai_summarize: { icon: Brain, tone: 'bg-brand-100 text-brand-700' },
  send_whatsapp: { icon: MessageCircle, tone: 'bg-emerald-100 text-emerald-700' },
  send_email: { icon: Send, tone: 'bg-sky-100 text-sky-700' },
  crm_update: { icon: Users, tone: 'bg-orange-100 text-orange-700' },
  sheet_append: { icon: Table2, tone: 'bg-green-100 text-green-700' },
  erp_post: { icon: Server, tone: 'bg-slate-200 text-slate-700' },
  condition: { icon: GitBranch, tone: 'bg-yellow-100 text-yellow-700' },
  notify_slack: { icon: Hash, tone: 'bg-fuchsia-100 text-fuchsia-700' },
}
export const metaFor = (type) => STEP_META[type] ?? { icon: Sparkles, tone: 'bg-slate-100 text-slate-600' }
