// BCE Boundary: :SearchUserAccountPage
// Methods: displayUserFound(result_list), displayUserNotFound()

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import SearchBar from '../components/SearchBar'
import UserCard from '../components/UserCard'
import AccountDetailsModal from '../components/AccountDetailsModal'
import { searchUserAcc } from '../api/userAccountApi'

export default function DashboardPage() {
  const navigate = useNavigate()
  const [users, setUsers] = useState([])
  const [searched, setSearched] = useState(false)
  const [selectedUser, setSelectedUser] = useState(null)
  const [loading, setLoading] = useState(false)
  const [noResults, setNoResults] = useState(false)

  useEffect(() => {
    loadAll()
  }, [])

  async function loadAll() {
    setLoading(true)
    try {
      const results = await searchUserAcc('')
      setUsers(results)
      setNoResults(results.length === 0)
    } catch {
      setUsers([])
    } finally {
      setLoading(false)
    }
  }

  async function handleSearch(keyword) {
    setLoading(true)
    setSearched(true)
    try {
      const results = await searchUserAcc(keyword)
      setUsers(results)
      setNoResults(results.length === 0)
    } catch {
      setUsers([])
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
            <SearchBar onSearch={handleSearch} />
          </div>
          <button
            onClick={() => navigate('/create-account')}
            className="flex items-center gap-2 bg-primary text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-blue-700 transition-colors shrink-0"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z" />
            </svg>
            Create Account
          </button>
        </div>

        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && noResults && (
          // displayUserNotFound
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <EnvelopeIllustration />
            <p className="text-gray-400 text-sm font-medium">Sorry ,search no found!</p>
          </div>
        )}

        {!loading && !noResults && (
          // displayUserFound(result_list)
          <div className="flex flex-col gap-3">
            {users.map((user) => (
              <UserCard key={user.userID} user={user} onClick={setSelectedUser} />
            ))}
          </div>
        )}
      </main>

      {selectedUser && (
        <AccountDetailsModal user={selectedUser} onClose={() => setSelectedUser(null)} />
      )}
    </div>
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
