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

// → SearchFRACategoryController.searchCategory() — returns all categories
export async function listFRACategories() {
  return request('GET', '/api/categories')
}

// → CreateFRACategoryController.createCategory()
export async function createCategory(categoryName, categoryDescription, categoryStatus = 'Active') {
  return request('POST', '/api/categories', { categoryName, categoryDescription, categoryStatus })
}

// → RetrieveFRACategoryController.retrieveCategory()
export async function retrieveCategory(categoryID) {
  return request('GET', `/api/categories/${categoryID}`)
}

// → SearchFRACategoryController.searchCategory()
export async function searchCategory(keyword) {
  return request('GET', `/api/categories/search?q=${encodeURIComponent(keyword)}`)
}

// → UpdateFRACategoryController.updateCategory()
export async function updateCategory(categoryID, data) {
  return request('PUT', `/api/categories/${categoryID}`, data)
}

// → SuspendFRACategoryController.suspendCategory()
export async function suspendCategory(categoryID) {
  return request('PUT', `/api/categories/${categoryID}/suspend`)
}
