import { GraduationCap, Scissors, Stethoscope, Utensils, Wrench } from 'lucide-vue-next'
import { http } from '@/core/http'

export const marketplaceService = {
  categories: () => http.get('/businesses/categories'),
  list: (params = {}) => http.get('/businesses?' + new URLSearchParams(Object.entries(params).filter(([, v]) => v))),
  business: (slug) => http.get(`/businesses/${slug}`),
  availability: (slug, params) => http.get(`/businesses/${slug}/availability?` + new URLSearchParams(Object.entries(params).filter(([, v]) => v != null))),
}

export const CATEGORY_ICONS = { Stethoscope, Utensils, Scissors, Wrench, GraduationCap }
export const CATEGORY_ICON_BY_SLUG = { clinics: Stethoscope, restaurants: Utensils, salons: Scissors, repair: Wrench, training: GraduationCap }
