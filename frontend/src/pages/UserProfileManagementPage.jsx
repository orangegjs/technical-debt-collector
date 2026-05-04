// BCE Boundary: :SearchUserProfilePage
// Methods: displayProfileFound(result_list), displayProfileNotFound()

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import SearchBar from '../components/SearchBar'
import { searchUserProfile } from '../api/userProfileApi'

export default function UserProfileManagementPage() {
  const navigate = useNavigate()
  const [profiles, setProfiles] = useState([])
  const [loading, setLoading] = useState(false)
  const [noResults, setNoResults] = useState(false)

  useEffect(() => {
    loadAll()
  }, [])

  async function loadAll() {
    setLoading(true)
    try {
      const results = await searchUserProfile('')
      setProfiles(results)
      setNoResults(results.length === 0)
    } catch {
      setProfiles([])
    } finally {
      setLoading(false)
    }
  }

  async function handleSearch(keyword) {
    setLoading(true)
    try {
      const results = await searchUserProfile(keyword)
      setProfiles(results)
      setNoResults(results.length === 0)
    } catch {
      setProfiles([])
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
            onClick={() => navigate('/create-user-profile')}
            className="flex items-center gap-2 bg-primary text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-blue-700 transition-colors shrink-0"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z" />
            </svg>
            Create Profile
          </button>
        </div>

        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && noResults && (
          // displayProfileNotFound
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <EnvelopeIllustration />
            <p className="text-gray-400 text-sm font-medium">No profiles found.</p>
          </div>
        )}

        {!loading && !noResults && (
          // displayProfileFound(result_list)
          <div className="flex flex-col gap-3">
            {profiles.map((profile) => (
              <ProfileCard
                key={profile.profileID}
                profile={profile}
                onClick={() => navigate(`/edit-user-profile/${profile.profileID}`)}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  )
}

function ProfileCard({ profile, onClick }) {
  const isActive = profile.profileStatus === 'Active'
  const desc = profile.profileDescription || ''
  const truncated = desc.length > 80 ? desc.slice(0, 80) + '…' : desc

  return (
    <button
      onClick={onClick}
      className="bg-white rounded-2xl shadow-sm px-6 py-4 flex items-center gap-4 text-left hover:shadow-md transition-shadow w-full"
    >
      <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center shrink-0">
        <BadgeIcon />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold text-gray-800 truncate">{profile.profileName}</p>
        {truncated && (
          <p className="text-xs text-gray-400 mt-0.5 truncate">{truncated}</p>
        )}
      </div>
      <span
        className={`shrink-0 text-xs font-semibold px-3 py-1 rounded-full ${
          isActive ? 'bg-green-100 text-green-700' : 'bg-red-100 text-deletered'
        }`}
      >
        {profile.profileStatus}
      </span>
    </button>
  )
}

function BadgeIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
    </svg>
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
