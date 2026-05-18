// BCE API Layer — maps to backend controller methods

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function request(method, path, body) {
  const options = { method, headers: { 'Content-Type': 'application/json' } }
  if (body !== undefined) options.body = JSON.stringify(body)
  const res = await fetch(`${BASE_URL}${path}`, options)
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw { status: res.status, detail: data.detail || 'Request failed' }
  return data
}

// → GenerateReportController.generateReport()
// reportType must be "daily" | "weekly" | "monthly"
// startDate optional — if omitted, controller defaults to today; endDate is always derived server-side
export async function generateReport(reportType, startDate) {
  const params = new URLSearchParams({ reportType })
  if (startDate) params.append('startDate', startDate)
  return request('POST', `/api/reports/generate?${params.toString()}`)
}
