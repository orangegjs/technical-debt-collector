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

// → SearchDonationController.searchDonation()
export async function searchDonation(userID, keyword, category, startDate, endDate) {
  const params = new URLSearchParams({ userID: String(userID), q: keyword || '' })
  if (category)  params.append('category',  category)
  if (startDate) params.append('startDate', startDate)
  if (endDate)   params.append('endDate',   endDate)
  return request('GET', `/api/donations/search?${params.toString()}`)
}

// → RetrieveDonationController.retrieveDonation()
export async function retrieveDonation(donationID) {
  return request('GET', `/api/donations/${donationID}`)
}
