export const money = (n, digits = 0) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: digits, minimumFractionDigits: digits }).format(n ?? 0)

export const number = (n) => new Intl.NumberFormat('en-US').format(n ?? 0)

export const date = (iso) =>
  iso ? new Date(iso + (iso.length === 10 ? 'T00:00:00' : '')).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '—'

export const initials = (name = '') => name.split(' ').map((p) => p[0]).slice(0, 2).join('').toUpperCase()

export const humanize = (s = '') => s.replaceAll('_', ' ').replace(/^\w/, (c) => c.toUpperCase())

const GRADIENTS = ['from-indigo-500 to-violet-500', 'from-sky-500 to-cyan-400', 'from-emerald-500 to-teal-400',
  'from-amber-500 to-orange-500', 'from-rose-500 to-pink-500', 'from-fuchsia-500 to-purple-500']
export const avatarGradient = (seed = '') => GRADIENTS[[...seed].reduce((a, c) => a + c.charCodeAt(0), 0) % GRADIENTS.length]
