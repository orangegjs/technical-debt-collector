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

// → SaveFRAController.saveFRA()
// Side-effect: increments fraShortlistCount on the FRA server-side.
export async function saveFRA(fraID, userID) {
  return request('POST', '/api/favourites', { fraID, userID })
}

// → SearchFavouriteController.searchFavourite()
export async function searchFavourite(userID, keyword) {
  const q = encodeURIComponent(keyword || '')
  return request('GET', `/api/favourites/search?userID=${userID}&q=${q}`)
}

// → RetrieveFavouriteController.retrieveFavourite()
export async function retrieveFavourite(userID, fraID) {
  return request('GET', `/api/favourites/${userID}/${fraID}`)
}
