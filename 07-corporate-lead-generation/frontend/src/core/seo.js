// Per-page SEO: <title>, meta description, canonical and JSON-LD structured data.
import config from '@/app.config'

function meta(name, content) {
  let el = document.head.querySelector(`meta[name="${name}"]`)
  if (!el) { el = document.createElement('meta'); el.setAttribute('name', name); document.head.appendChild(el) }
  el.setAttribute('content', content)
}

export function setSeo({ title, description, jsonLd } = {}) {
  document.title = title ? `${title} | ${config.name}` : `${config.name} — ${config.tagline}`
  meta('description', description || config.description)
  let canonical = document.head.querySelector('link[rel="canonical"]')
  if (!canonical) { canonical = document.createElement('link'); canonical.rel = 'canonical'; document.head.appendChild(canonical) }
  canonical.href = location.origin + location.pathname
  document.getElementById('jsonld')?.remove()
  if (jsonLd) {
    const s = document.createElement('script')
    s.type = 'application/ld+json'
    s.id = 'jsonld'
    s.textContent = JSON.stringify({ '@context': 'https://schema.org', ...jsonLd })
    document.head.appendChild(s)
  }
}
