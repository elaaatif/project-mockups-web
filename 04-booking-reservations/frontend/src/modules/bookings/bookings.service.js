import { http } from '@/core/http'

export const bookingsService = {
  book: (body) => http.post('/bookings', body),
  lookup: (email) => http.get('/bookings/lookup?' + new URLSearchParams({ email })),
  cancel: (code) => http.post(`/bookings/${code}/cancel`),
  setStatus: (code, status) => http.patch(`/bookings/${code}/status`, { status }),
}

/** Generates an .ics calendar file for a booking. */
export function downloadIcs(b) {
  const start = new Date(`${b.date}T${b.time}:00`)
  const end = new Date(start.getTime() + b.minutes * 60000)
  const fmt = (d) => d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '')
  const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Bookly//EN', 'BEGIN:VEVENT', `UID:${b.code}@bookly`, `DTSTAMP:${fmt(new Date())}`,
    `DTSTART:${fmt(start)}`, `DTEND:${fmt(end)}`, `SUMMARY:${b.service_name} · ${b.business_name}`, `DESCRIPTION:Booking ${b.code} with ${b.staff_name}`,
    'END:VEVENT', 'END:VCALENDAR'].join('\r\n')
  const a = document.createElement('a')
  a.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' }))
  a.download = `${b.code}.ics`
  a.click()
}
