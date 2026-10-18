import { http } from '@/core/http'

export const careersService = {
  jobs: (params = {}) => http.get('/careers/jobs?' + new URLSearchParams(Object.entries(params).filter(([, v]) => v))),
  job: (slug) => http.get(`/careers/jobs/${slug}`),
  apply: (slug, fields, cv) => {
    const form = new FormData()
    Object.entries(fields).forEach(([k, v]) => form.append(k, v))
    form.append('cv', cv)
    return http.post(`/careers/jobs/${slug}/apply`, form)
  },
}
