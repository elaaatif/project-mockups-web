import { http } from '@/core/http'

export const extractionService = {
  samples: () => http.get('/extraction/samples'),
  upload: (file) => {
    const form = new FormData()
    form.append('file', file)
    return http.post('/extraction/upload', form)
  },
  runSample: (name) => http.post(`/extraction/sample/${encodeURIComponent(name)}`),
}

/** Client-side CSV export of extracted fields. */
export function downloadCsv(result) {
  const rows = [['Field', 'Value', 'Confidence'], ...result.fields.map((f) => [f.label, f.value, f.confidence])]
  const csv = rows.map((r) => r.map((c) => `"${String(c).replaceAll('"', '""')}"`).join(',')).join('\n')
  const a = document.createElement('a')
  a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }))
  a.download = result.filename.replace(/\.\w+$/, '') + '-extracted.csv'
  a.click()
  URL.revokeObjectURL(a.href)
}
