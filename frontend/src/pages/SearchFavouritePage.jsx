// BCE Boundary: :SearchFavouritePage
// Methods: displayFavourite(result_list), displayFavouriteNotFound()

import React, { useEffect, useState } from 'react'
import { useAuth } from '../App'
import Sidebar from '../components/Sidebar'
import SearchBar from '../components/SearchBar'
import { searchFavourite, retrieveFavourite } from '../api/favouriteApi'

export default function SearchFavouritePage() {
  const { user } = useAuth()
  const [favList, setFavList] = useState([])
  const [loading, setLoading] = useState(false)
  const [noResults, setNoResults] = useState(false)
  const [selectedFav, setSelectedFav] = useState(null)

  useEffect(() => {
    handleSearch('')
  }, [])

  async function handleSearch(keyword) {
    setLoading(true)
    try {
      const results = await searchFavourite(user.userID, keyword)
      setFavList(results)
      setNoResults(results.length === 0)
    } catch {
      setFavList([])
      setNoResults(true)
    } finally {
      setLoading(false)
    }
  }

  async function openDetail(fav) {
    // BCE: nested boundary :RetrieveFavouritePage — displayFavourite(Favourite fav)
    try {
      const fresh = await retrieveFavourite(user.userID, fav.fraID)
      setSelectedFav(fresh)
    } catch {
      setSelectedFav(fav)
    }
  }

  return (
    <div className="flex min-h-screen bg-lightbg">
      <Sidebar />
      <main className="flex-1 p-8 flex flex-col gap-5">
        <div className="flex items-center gap-3">
          <div className="flex-1">
            <SearchBar onSearch={handleSearch} placeholder="Search by FRA ID, FRA Name..." />
          </div>
        </div>

        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && noResults && (
          // displayFavouriteNotFound
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <EnvelopeIllustration />
            <p className="text-gray-400 text-sm font-medium">No favourites found.</p>
          </div>
        )}

        {!loading && !noResults && (
          // displayFavourite(result_list)
          <div className="flex flex-col gap-3">
            {favList.map((fav) => (
              <FavouriteCard key={fav.favouriteID} fav={fav} onClick={() => openDetail(fav)} />
            ))}
          </div>
        )}
      </main>

      {selectedFav && (
        <FavouriteDetailModal fav={selectedFav} onClose={() => setSelectedFav(null)} />
      )}
    </div>
  )
}

function FavouriteCard({ fav, onClick }) {
  const fra = fav.fra || {}
  return (
    <button
      onClick={onClick}
      className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex flex-col gap-1 text-left hover:bg-blue-50 transition-colors w-full"
    >
      <div className="flex items-center justify-between">
        <p className="text-sm font-bold text-gray-900">{fra.fraName || '-'}</p>
        <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-green-100 text-green-700">
          {fra.fraStatus || '-'}
        </span>
      </div>
      <p className="text-xs text-gray-600 font-medium">
        Goal: ${Number(fra.fraGoalAmount || 0).toLocaleString()}
      </p>
      <p className="text-xs text-gray-400">Saved on {fav.savedDate}</p>
    </button>
  )
}

function FavouriteDetailModal({ fav, onClose }) {
  // BCE: nested boundary :RetrieveFavouritePage — displayFavourite(Favourite fav)
  const fra = fav.fra || {}
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl mx-4 p-7 flex flex-col gap-5">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">Favourite Details</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-lg leading-none">×</button>
        </div>

        <table className="w-full text-sm">
          <tbody className="divide-y divide-gray-100">
            <DetailRow label="Saved On"     value={fav.savedDate} />
            <DetailRow label="FRA Name"     value={fra.fraName || '-'} />
            <DetailRow label="Goal Amount"  value={`$${Number(fra.fraGoalAmount || 0).toLocaleString()}`} />
            <DetailRow label="Start Date"   value={fra.fraStartDate || '-'} />
            <DetailRow label="End Date"     value={fra.fraEndDate || '-'} />
            <DetailRow label="Status"       value={fra.fraStatus || '-'} />
            <DetailRow label="Category"     value={fra.fra_category?.categoryName || '-'} />
            <DetailRow label="Description"  value={fra.fraDescription || <span className="text-gray-400 italic">No description</span>} />
          </tbody>
        </table>

        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg bg-cancelgray text-white text-sm font-semibold hover:bg-gray-600 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

function DetailRow({ label, value }) {
  return (
    <tr>
      <td className="py-2.5 pr-4 font-medium text-gray-600 w-2/5 align-top">{label}</td>
      <td className="py-2.5 text-gray-800 align-top">{value}</td>
    </tr>
  )
}

function EnvelopeIllustration() {
  return (
    <svg width="120" height="120" viewBox="0 0 120 120" fill="none">
      <rect x="15" y="40" width="70" height="55" rx="4" fill="#e5e7eb" />
      <path d="M15 44l35 25 35-25" stroke="#d1d5db" strokeWidth="2" fill="none" />
      <rect x="20" y="20" width="40" height="30" rx="4" fill="#d1d5db" />
      <rect x="28" y="28" width="24" height="4" rx="2" fill="#9ca3af" />
      <rect x="28" y="36" width="16" height="4" rx="2" fill="#9ca3af" />
      <ellipse cx="85" cy="35" rx="18" ry="18" fill="#e5e7eb" />
      <circle cx="85" cy="31" r="2" fill="#9ca3af" />
      <circle cx="85" cy="35" r="2" fill="#9ca3af" />
      <circle cx="85" cy="39" r="2" fill="#9ca3af" />
    </svg>
  )
}
