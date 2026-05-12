// BCE Boundary: :SearchFRAPage
// Methods: displayFRAFound(result_list), displayFRANotFound()

import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import SearchBar from '../components/SearchBar'
import { searchFRA } from '../api/fraActivityApi'

export default function FRAManagementPage() {
  const navigate = useNavigate()
  const [fraList, setFraList] = useState([])
  const [loading, setLoading] = useState(false)
  const [noResults, setNoResults] = useState(false)
  const [selectedFRA, setSelectedFRA] = useState(null)

  useEffect(() => {
    loadAll()
  }, [])

  async function loadAll() {
    setLoading(true)
    try {
      const results = await searchFRA('')
      setFraList(results)
      setNoResults(results.length === 0)
    } catch {
      setFraList([])
      setNoResults(true)
    } finally {
      setLoading(false)
    }
  }

  async function handleSearch(keyword) {
    setLoading(true)
    try {
      const results = await searchFRA(keyword)
      setFraList(results)
      setNoResults(results.length === 0)
    } catch {
      setFraList([])
      setNoResults(true)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-lightbg">
      <Sidebar />
      <main className="flex-1 p-8 flex flex-col gap-5">
        <div className="flex items-center gap-3">
          <div className="flex-1">
            <SearchBar onSearch={handleSearch} placeholder="Search by FRA ID, FRA Name......" />
          </div>
          <button
            onClick={() => navigate('/create-fra')}
            className="flex items-center gap-2 bg-primary text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-blue-700 transition-colors shrink-0"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z" />
            </svg>
            Create FRA
          </button>
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
            <p className="text-gray-400 text-sm font-medium">No FRA activities found.</p>
          </div>
        )}

        {!loading && !noResults && (
          // displayFRAFound(result_list)
          <div className="flex flex-col gap-3">
            {fraList.map((fra) => (
              <FRACard key={fra.fraID} fra={fra} onClick={() => setSelectedFRA(fra)} />
            ))}
          </div>
        )}
      </main>

      {selectedFRA && (
        <FRADetailModal
          fra={selectedFRA}
          onClose={() => setSelectedFRA(null)}
          onUpdate={() => {
            setSelectedFRA(null)
            navigate(`/edit-fra/${selectedFRA.fraID}`)
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
      <p className="text-sm font-bold text-gray-900">{fra.fraName}</p>
      <p className="text-xs text-gray-500">
        Goal: ${Number(fra.fraGoalAmount || 0).toLocaleString()} | Status: {fra.fraStatus}
      </p>
      {truncated && <p className="text-xs text-gray-500">{truncated}</p>}
    </button>
  )
}

function FRADetailModal({ fra, onClose, onUpdate }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl mx-4 p-7 flex flex-col gap-5">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">FRA Details</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors text-lg leading-none"
          >
            ×
          </button>
        </div>

        <div className="flex flex-col gap-4">
          <p className="text-sm font-semibold text-gray-700">Fundraising Activity Information</p>
          <table className="w-full text-sm">
            <tbody className="divide-y divide-gray-100">
              <DetailRow label="FRA ID" value={fra.fraID} />
              <DetailRow label="FRA Name" value={fra.fraName} />
              <DetailRow label="Goal Amount" value={`$${Number(fra.fraGoalAmount || 0).toLocaleString()}`} />
              <DetailRow label="Start Date" value={fra.fraStartDate} />
              <DetailRow label="End Date" value={fra.fraEndDate} />
              <DetailRow label="Status" value={fra.fraStatus} />
              <DetailRow label="Category" value={fra.fra_category?.categoryName || '-'} />
              <DetailRow label="Owner" value={fra.fra_owner?.username || '-'} />
              <DetailRow label="Description" value={fra.fraDescription || <span className="text-gray-400 italic">No description</span>} />
            </tbody>
          </table>
        </div>

        <div className="flex justify-end gap-3 pt-1">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg bg-cancelgray text-white text-sm font-semibold hover:bg-gray-600 transition-colors"
          >
            Close
          </button>
          <button
            onClick={onUpdate}
            className="px-5 py-2 rounded-lg bg-primary text-white text-sm font-semibold hover:bg-blue-700 transition-colors"
          >
            Update
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
