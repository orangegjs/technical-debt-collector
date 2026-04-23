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

// → LoginController.login()
export async function login(username, password) {
  return request('POST', '/api/auth/login', { username, password })
}

// → LogoutController.logout()
export async function logout() {
  return request('POST', '/api/auth/logout')
}

// → CreateUserAccountController.createUserAccount()
export async function createUserAccount(username, password, name, email, accountStatus, role) {
  return request('POST', '/api/users', { username, password, name, email, accountStatus, role })
}

// → RetrieveUserAccountController.retrieveUserAccount()
export async function retrieveUserAccount(userID) {
  return request('GET', `/api/users/${userID}`)
}

// → SearchUserAccountController.searchUserAcc()
export async function searchUserAcc(keyword) {
  return request('GET', `/api/users/search?q=${encodeURIComponent(keyword)}`)
}

// → UpdateUserAccountController.updateUserAccount()
export async function updateUserAccount(userID, data) {
  return request('PUT', `/api/users/${userID}`, data)
}

// → SuspendUserAccountController.suspendUserAccount()
export async function suspendUserAccount(userID) {
  return request('PUT', `/api/users/${userID}/suspend`)
}
