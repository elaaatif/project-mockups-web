// Branding for the portfolio shell. Personal details live in backend/app/modules/profile/models.py.
import { Code2 } from 'lucide-vue-next'

export default {
  name: 'Portfolio',
  tagline: 'Vue.js + FastAPI developer',
  logo: Code2,
  searchPlaceholder: 'Search messages…',
  user: { name: 'Your Name', role: 'Owner' },
  promo: null,
}
