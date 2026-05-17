// BCE Boundary: :SearchAvailableFRAPage
// Methods: displayFRA(result_list), displayFRANotFound()

import React, { useEffect, useState } from 'react'
import { useAuth } from '../App'
import Sidebar from '../components/Sidebar'
import SearchBar from '../components/SearchBar'
import { searchAvailableFRA, retrieveAvailableFRA } from '../api/fraActivityApi'
import { saveFRA } from '../api/favouriteApi'

export default function SearchAvailableFRAPage() {
  const { user } = useAuth()
  const [fraList, setFraList] = useState([])
  const [loading, setLoading] = useState(false)
  const [noResults, setNoResults] = useState(false)
  const [selectedFRA, setSelectedFRA] = useState(null)

  useEffect(() => {
    handleSearch('')
  }, [])

  async function handleSearch(keyword) {
    setLoading(true)
    try {
      const results = await searchAvailableFRA(user.userID, keyword)
      setFraList(results)
      setNoResults(results.length === 0)
    } catch {
      setFraList([])
      setNoResults(true)
    } finally {
      setLoading(false)
    }
  }

  async function openDetail(fra) {
    // BCE: nested boundary :RetrieveAvailableFRAPage — displayFRA(FRA activity)
    try {
      const fresh = await retrieveAvailableFRA(fra.fraID)
      setSelectedFRA(fresh)
    } catch {
      setSelectedFRA(fra)
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
          // displayFRANotFound
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <EnvelopeIllustration />
            <p className="text-gray-400 text-sm font-medium">No available FRAs found.</p>
          </div>
        )}

        {!loading && !noResults && (
          // displayFRA(result_list)
          <div className="flex flex-col gap-3">
            {fraList.map((fra) => (
              <FRACard key={fra.fraID} fra={fra} onClick={() => openDetail(fra)} />
            ))}
          </div>
        )}
      </main>

      {selectedFRA && (
        <FRADetailModal
          fra={selectedFRA}
          userID={user.userID}
          onClose={() => setSelectedFRA(null)}
          onSaved={(updated) => {
            setFraList((prev) =>
              prev.map((f) => (f.fraID === updated.fraID ? updated : f))
            )
          }}
        />
      )}
    </div>
  )
}

function FRACard({ fra, onClick }) {
  const desc = fra.fraDescription || ''
  const truncated = desc.length > 120 ? desc.slice(0, 120) + '...' : desc
  return (
    <button
      onClick={onClick}
      className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex flex-col gap-1 text-left hover:bg-blue-50 transition-colors w-full"
    >
      <div className="flex items-center justify-between">
        <p className="text-sm font-bold text-gray-900">{fra.fraName}</p>
        <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-green-100 text-green-700">
          {fra.fraStatus}
        </span>
      </div>
      <p className="text-xs text-gray-600 font-medium">
        Goal: ${Number(fra.fraGoalAmount || 0).toLocaleString()}
      </p>
      {truncated && <p className="text-xs text-gray-400">{truncated}</p>}
      <p className="text-xs text-gray-400 mt-1">
        {fra.fraViewCount ?? 0} views · {fra.fraShortlistCount ?? 0} saves
      </p>
    </button>
  )
}

function FRADetailModal({ fra, userID, onClose, onSaved }) {
  // BCE: nested boundary :RetrieveAvailableFRAPage — displayFRA(FRA activity)
  const [toast, setToast] = useState(null)
  const [saving, setSaving] = useState(false)

  function showToast(type, message) {
    setToast({ type, message })
    setTimeout(() => setToast(null), 2000)
  }

  async function handleSave() {
    // BCE: nested boundary :SaveFRAPage — displaySaveSuccess(), displayDuplicateFRASaved()
    setSaving(true)
    try {
      await saveFRA(fra.fraID, userID)
      showToast('success', 'Saved to favourites!')
      // displaySaveSuccess
      setTimeout(() => onClose(), 2000)
    } catch (err) {
      if (err?.detail === 'displayDuplicateFRASaved') {
        // displayDuplicateFRASaved
        showToast('warning', 'Already in your favourites')
      } else {
        showToast('error', 'Failed to save. Please try again.')
      }
    } finally {
      setSaving(false)
    }
  }

  const toastColors = {
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    error:   'bg-deletered',
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl mx-4 p-7 flex flex-col gap-5 relative">
        {toast && (
          <div className={`absolute top-4 left-1/2 -translate-x-1/2 px-5 py-2 rounded-xl text-white text-sm font-semibold shadow-lg ${toastColors[toast.type]}`}>
            {toast.message}
          </div>
        )}

        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">FRA Details</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-lg leading-none">×</button>
        </div>

        <table className="w-full text-sm">
          <tbody className="divide-y divide-gray-100">
            <DetailRow label="FRA ID"       value={fra.fraID} />
            <DetailRow label="Name"         value={fra.fraName} />
            <DetailRow label="Goal Amount"  value={`$${Number(fra.fraGoalAmount || 0).toLocaleString()}`} />
            <DetailRow label="Start Date"   value={fra.fraStartDate} />
            <DetailRow label="End Date"     value={fra.fraEndDate} />
            <DetailRow label="Status"       value={fra.fraStatus} />
            <DetailRow label="Category"     value={fra.fra_category?.categoryName || '-'} />
            <DetailRow label="Description"  value={fra.fraDescription || <span className="text-gray-400 italic">No description</span>} />
            <DetailRow label="Views"        value={fra.fraViewCount ?? 0} />
            <DetailRow label="Saves"        value={fra.fraShortlistCount ?? 0} />
          </tbody>
        </table>

        <div className="flex justify-end gap-3 pt-1">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg bg-cancelgray text-white text-sm font-semibold hover:bg-gray-600 transition-colors"
          >
            Close
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className="px-5 py-2 rounded-lg bg-primary text-white text-sm font-semibold hover:bg-blue-700 transition-colors disabled:opacity-60"
          >
            {saving ? 'Saving...' : 'Save to Favourites'}
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
