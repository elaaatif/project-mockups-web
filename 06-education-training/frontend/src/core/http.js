// Thin fetch wrapper used by every module service. Vite proxies /api to the FastAPI backend.
const BASE = '/api'

async function request(method, path, body) {
  const isForm = body instanceof FormData
  const res = await fetch(BASE + path, {
    method,
    headers: body && !isForm ? { 'Content-Type': 'application/json' } : undefined,
    body: isForm ? body : body ? JSON.stringify(body) : undefined,
  })
  const data = await res.json().catch(() => null)
  if (!res.ok) {
    const detail = data?.detail
    throw new Error(typeof detail === 'string' ? detail : Array.isArray(detail) ? detail.map((d) => d.msg).join(', ') : res.statusText)
  }
  return data
}

export const http = {
  get: (path) => request('GET', path),
  post: (path, body) => request('POST', path, body),
  patch: (path, body) => request('PATCH', path, body),
  delete: (path) => request('DELETE', path),
}
