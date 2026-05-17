// BCE Boundary: :SearchCompletedFRAPage
// US#29: displayFRA(List<FRA>), displayFRANotFound()
// US#30: displayFRA(FRA activity) — nested RetrieveCompletedFRAPage modal

import React, { useEffect, useState } from 'react'
import { useAuth } from '../App'
import Sidebar from '../components/Sidebar'
import { searchCompletedFRA, retrieveCompletedFRA } from '../api/fraActivityApi'
import { listFRACategories } from '../api/fraCategoryApi'

export default function SearchCompletedFRAPage() {
  const { user } = useAuth()
  const [fraList, setFraList] = useState([])
  const [loading, setLoading] = useState(false)
  const [noResults, setNoResults] = useState(false)
  const [selectedFRA, setSelectedFRA] = useState(null)

  const [keyword, setKeyword] = useState('')
  const [serviceType, setServiceType] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [categories, setCategories] = useState([])

  useEffect(() => {
    listFRACategories().then(setCategories).catch(() => setCategories([]))
    doSearch('', '', '', '')
  }, [])

  async function doSearch(kw, svc, start, end) {
    setLoading(true)
    try {
      const results = await searchCompletedFRA(
        user.userID,
        kw,
        svc || null,
        start || null,
        end || null,
      )
      setFraList(results)
      setNoResults(results.length === 0)
    } catch {
      setFraList([])
      setNoResults(true)
    } finally {
      setLoading(false)
    }
  }

  function handleSearch(e) {
    e.preventDefault()
    doSearch(keyword, serviceType, startDate, endDate)
  }

  async function openDetail(fra) {
    // BCE: nested boundary :RetrieveCompletedFRAPage — displayFRA(FRA activity)
    try {
      const fresh = await retrieveCompletedFRA(fra.fraID)
      setSelectedFRA(fresh)
    } catch {
      setSelectedFRA(fra)
    }
  }

  return (
    <div className="flex min-h-screen bg-lightbg">
      <Sidebar />
      <main className="flex-1 p-8 flex flex-col gap-5">
        <form onSubmit={handleSearch} className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 flex flex-wrap gap-3 items-end">
          <div className="flex flex-col gap-1 flex-1 min-w-[180px]">
            <label className="text-xs font-medium text-gray-500">Keyword</label>
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="Search FRA name or ID..."
              className="border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-primary"
            />
          </div>
          <div className="flex flex-col gap-1 min-w-[160px]">
            <label className="text-xs font-medium text-gray-500">Service Type</label>
            <select
              value={serviceType}
              onChange={(e) => setServiceType(e.target.value)}
              className="border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-primary"
            >
              <option value="">All Types</option>
              {categories.map((c) => (
                <option key={c.categoryID} value={c.categoryName}>{c.categoryName}</option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-gray-500">Start Date</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-primary"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-gray-500">End Date</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-primary"
            />
          </div>
          <button
            type="submit"
            className="bg-primary text-white px-6 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition-colors"
          >
            Search
          </button>
        </form>

        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && noResults && (
          // displayFRANotFound
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <EnvelopeIllustration />
            <p className="text-gray-400 text-sm font-medium">No matching completed FRA found.</p>
          </div>
        )}

        {!loading && !noResults && (
          // displayFRA(List<FRA>)
          <div className="flex flex-col gap-3">
            {fraList.map((fra) => (
              <CompletedFRACard key={fra.fraID} fra={fra} onClick={() => openDetail(fra)} />
            ))}
          </div>
        )}
      </main>

      {selectedFRA && (
        // BCE: nested boundary :RetrieveCompletedFRAPage
        <CompletedFRADetailModal fra={selectedFRA} onClose={() => setSelectedFRA(null)} />
      )}
    </div>
  )
}

function CompletedFRACard({ fra, onClick }) {
  const desc = fra.fraDescription || ''
  const truncated = desc.length > 120 ? desc.slice(0, 120) + '...' : desc

  return (
    <button
      onClick={onClick}
      className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex flex-col gap-1 text-left hover:bg-blue-50 transition-colors w-full"
    >
      <div className="flex items-center justify-between">
        <p className="text-sm font-bold text-gray-900">{fra.fraName}</p>
        <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">
          Completed
        </span>
      </div>
      <p className="text-xs text-gray-500">
        Goal: ${Number(fra.fraGoalAmount || 0).toLocaleString()} | Ended: {fra.fraEndDate}
      </p>
      <p className="text-xs text-gray-500">{fra.fra_category?.categoryName || ''}</p>
      {truncated && <p className="text-xs text-gray-400">{truncated}</p>}
      <p className="text-xs text-gray-400 mt-1">
        {fra.fraViewCount ?? 0} views · {fra.fraShortlistCount ?? 0} saves
      </p>
    </button>
  )
}

function CompletedFRADetailModal({ fra, onClose }) {
  // BCE: :RetrieveCompletedFRAPage — displayFRA(FRA activity)
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl mx-4 p-7 flex flex-col gap-5 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">Completed FRA Details</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-lg leading-none">×</button>
        </div>

        <table className="w-full text-sm">
          <tbody className="divide-y divide-gray-100">
            <DetailRow label="FRA ID"               value={fra.fraID} />
            <DetailRow label="FRA Name"             value={fra.fraName} />
            <DetailRow label="Goal Amount"          value={`$${Number(fra.fraGoalAmount || 0).toLocaleString()}`} />
            <DetailRow label="Start Date"           value={fra.fraStartDate} />
            <DetailRow label="End Date"             value={fra.fraEndDate} />
            <DetailRow label="Status"               value={fra.fraStatus} />
            <DetailRow label="Service Type"         value={fra.fra_category?.categoryName || '-'} />
            <DetailRow label="Owner"                value={fra.fra_owner?.username || '-'} />
            <DetailRow label="Number of Views"      value={fra.fraViewCount ?? 0} />
            <DetailRow label="Number of Shortlisted" value={fra.fraShortlistCount ?? 0} />
            <DetailRow label="Description"          value={fra.fraDescription || <span className="text-gray-400 italic">No description</span>} />
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
