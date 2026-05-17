// BCE API Layer — maps to backend controller methods
// Each function corresponds to a controller in controls/

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function request(method, path, body) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  }
  if (body !== undefined) options.body = JSON.stringify(body)
  const res = await fetch(`${BASE_URL}${path}`, options)
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw { status: res.status, detail: data.detail || 'Request failed' }
  return data
}

// -> SearchFRAActivityController.searchFRA() — returns all FRA records
export async function listFRAs() {
  return request('GET', '/api/fras')
}

// -> CreateFRAActivityController.createFRA()
export async function createFRA(payload) {
  return request('POST', '/api/fras', payload)
}

// -> RetrieveFRAActivityController.retrieveFRA()
export async function retrieveFRA(fraID) {
  return request('GET', `/api/fras/${fraID}`)
}

// -> SearchFRAActivityController.searchFRA()
export async function searchFRA(keyword, ownerID = null) {
  const q = encodeURIComponent(keyword || '')
  const owner = ownerID != null ? `&ownerID=${ownerID}` : ''
  return request('GET', `/api/fras/search?q=${q}${owner}`)
}

// -> UpdateFRAActivityController.updateFRA()
export async function updateFRA(fraID, data) {
  return request('PUT', `/api/fras/${fraID}`, data)
}

// -> SuspendFRAActivityController.suspendFRA()
export async function suspendFRA(fraID) {
  return request('PUT', `/api/fras/${fraID}/suspend`)
}

// → SearchAvailableFRAController.searchAvailableFRA()
export async function searchAvailableFRA(userID, keyword) {
  const q = encodeURIComponent(keyword || '')
  return request('GET', `/api/fras/available/search?userID=${userID}&q=${q}`)
}

// → RetrieveAvailableFRAController.retrieveAvailableFRA()
// Side-effect: increments fraViewCount server-side.
export async function retrieveAvailableFRA(fraID) {
  return request('GET', `/api/fras/available/${fraID}`)
}
