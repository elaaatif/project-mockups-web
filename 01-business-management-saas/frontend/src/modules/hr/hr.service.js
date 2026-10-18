import { http } from '@/core/http'

export const hrService = {
  employees: () => http.get('/hr/employees'),
  leaves: () => http.get('/hr/leaves'),
  requestLeave: (body) => http.post('/hr/leaves', body),
  decideLeave: (id, status) => http.patch(`/hr/leaves/${id}`, { status }),
  payrollRuns: () => http.get('/hr/payroll'),
  runPayroll: (month) => http.post('/hr/payroll/run', { month }),
}
