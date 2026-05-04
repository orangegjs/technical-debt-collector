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

// → CreateUserProfileController.createUserProfile()
export async function createUserProfile(profileName, profileDescription) {
  return request('POST', '/api/profiles', { profileName, profileDescription })
}

// → RetrieveUserProfileController.retrieveUserProfile()
export async function retrieveUserProfile(profileID) {
  return request('GET', `/api/profiles/${profileID}`)
}

// → SearchUserProfileController.searchUserProfile()
export async function searchUserProfile(keyword) {
  return request('GET', `/api/profiles/search?q=${encodeURIComponent(keyword)}`)
}

// → UpdateUserProfileController.updateUserProfile()
export async function updateUserProfile(profileID, data) {
  return request('PUT', `/api/profiles/${profileID}`, data)
}

// → SuspendUserProfileController.suspendUserProfile()
export async function suspendUserProfile(profileID) {
  return request('PUT', `/api/profiles/${profileID}/suspend`)
}
