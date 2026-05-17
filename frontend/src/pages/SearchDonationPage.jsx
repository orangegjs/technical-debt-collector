// BCE Boundary: :SearchDonationPage
// Methods: displayDonation(result_list), displayDonationNotFound()

import React, { useEffect, useState } from 'react'
import { useAuth } from '../App'
import Sidebar from '../components/Sidebar'
import { searchDonation, retrieveDonation } from '../api/donationApi'
import { listFRACategories } from '../api/fraCategoryApi'

export default function SearchDonationPage() {
  const { user } = useAuth()
  const [donations, setDonations] = useState([])
  const [loading, setLoading] = useState(false)
  const [noResults, setNoResults] = useState(false)
  const [selectedDonation, setSelectedDonation] = useState(null)

  const [keyword, setKeyword] = useState('')
  const [category, setCategory] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [categories, setCategories] = useState([])

  useEffect(() => {
    listFRACategories().then(setCategories).catch(() => setCategories([]))
    doSearch('', '', '', '')
  }, [])

  async function doSearch(kw, cat, start, end) {
    setLoading(true)
    try {
      const results = await searchDonation(
        user.userID,
        kw,
        cat || null,
        start || null,
        end || null,
      )
      setDonations(results)
      setNoResults(results.length === 0)
    } catch {
      setDonations([])
      setNoResults(true)
    } finally {
      setLoading(false)
    }
  }

  function handleSearch(e) {
    e.preventDefault()
    doSearch(keyword, category, startDate, endDate)
  }

  async function openDetail(don) {
    // BCE: nested boundary :RetrieveDonationPage — displayDonation(Donation don)
    try {
      const fresh = await retrieveDonation(don.donationID)
      setSelectedDonation(fresh)
    } catch {
      setSelectedDonation(don)
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
            <label className="text-xs font-medium text-gray-500">Category</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-primary"
            >
              <option value="">All Categories</option>
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
          // displayDonationNotFound
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <EnvelopeIllustration />
            <p className="text-gray-400 text-sm font-medium">No donation records found.</p>
          </div>
        )}

        {!loading && !noResults && (
          // displayDonation(result_list)
          <div className="flex flex-col gap-3">
            {donations.map((don) => (
              <DonationCard key={don.donationID} don={don} onClick={() => openDetail(don)} />
            ))}
          </div>
        )}
      </main>

      {selectedDonation && (
        <DonationDetailModal don={selectedDonation} onClose={() => setSelectedDonation(null)} />
      )}
    </div>
  )
}

function statusBadge(status) {
  const map = {
    Completed: 'bg-green-100 text-green-700',
    Pending:   'bg-yellow-100 text-yellow-700',
    Failed:    'bg-red-100 text-red-700',
  }
  return map[status] || 'bg-gray-100 text-gray-600'
}

function ProgressBar({ fraProgress }) {
  const pct = Math.min((fraProgress || 0) * 100, 100).toFixed(1)
  return (
    <div className="flex flex-col gap-1">
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div className="bg-primary h-2 rounded-full transition-all" style={{ width: `${pct}%` }} />
      </div>
      <p className="text-xs text-gray-400">{pct}% funded</p>
    </div>
  )
}

function DonationCard({ don, onClick }) {
  const fra = don.fra || {}
  const raised = (fra.fraGoalAmount || 0) * (don.fraProgress || 0)
  return (
    <button
      onClick={onClick}
      className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex flex-col gap-2 text-left hover:bg-blue-50 transition-colors w-full"
    >
      <div className="flex items-center justify-between">
        <p className="text-sm font-bold text-gray-900">{fra.fraName || '-'}</p>
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${statusBadge(don.donationStatus)}`}>
          {don.donationStatus}
        </span>
      </div>
      <p className="text-sm font-semibold text-primary">
        ${Number(don.donationAmount || 0).toLocaleString()}
        <span className="text-gray-400 font-normal text-xs ml-2">{don.donationDate}</span>
      </p>
      <p className="text-xs text-gray-400">{fra.fra_category?.categoryName || ''}</p>
      <p className="text-xs text-gray-500">
        ${Number(raised).toLocaleString(undefined, { maximumFractionDigits: 0 })} raised of ${Number(fra.fraGoalAmount || 0).toLocaleString()} goal
      </p>
      <ProgressBar fraProgress={don.fraProgress} />
    </button>
  )
}

function DonationDetailModal({ don, onClose }) {
  // BCE: nested boundary :RetrieveDonationPage — displayDonation(Donation don)
  const fra = don.fra || {}
  const raised = (fra.fraGoalAmount || 0) * (don.fraProgress || 0)
  const pct = Math.min((don.fraProgress || 0) * 100, 100).toFixed(1)

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl mx-4 p-7 flex flex-col gap-5 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">Donation Details</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-lg leading-none">×</button>
        </div>

        <table className="w-full text-sm">
          <tbody className="divide-y divide-gray-100">
            <DetailRow label="Donation ID"    value={don.donationID} />
            <DetailRow label="Amount"         value={`$${Number(don.donationAmount || 0).toLocaleString()}`} />
            <DetailRow label="Date"           value={don.donationDate} />
            <DetailRow label="Status"         value={<span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusBadge(don.donationStatus)}`}>{don.donationStatus}</span>} />
            <DetailRow label="FRA Name"       value={fra.fraName || '-'} />
            <DetailRow label="Category"       value={fra.fra_category?.categoryName || '-'} />
            <DetailRow label="Goal Amount"    value={`$${Number(fra.fraGoalAmount || 0).toLocaleString()}`} />
            <DetailRow label="FRA Start"      value={fra.fraStartDate || '-'} />
            <DetailRow label="FRA End"        value={fra.fraEndDate || '-'} />
            <DetailRow label="Description"    value={fra.fraDescription || <span className="text-gray-400 italic">No description</span>} />
          </tbody>
        </table>

        <div className="flex flex-col gap-2">
          <p className="text-sm font-medium text-gray-600">FRA Funding Progress</p>
          <p className="text-xs text-gray-500">
            ${Number(raised).toLocaleString(undefined, { maximumFractionDigits: 0 })} raised of ${Number(fra.fraGoalAmount || 0).toLocaleString()} goal
          </p>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div className="bg-primary h-3 rounded-full transition-all" style={{ width: `${pct}%` }} />
          </div>
          <p className="text-xs text-gray-400">{pct}% funded</p>
        </div>

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
