import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../App'
import { logout as apiLogout } from '../api/userAccountApi'
import Logo from './Logo'

export default function Sidebar() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuth()

  const profileName = user?.user_profile?.profileName

  async function handleLogout() {
    try {
      await apiLogout()
    } catch {
      // proceed regardless
    }
    logout()
    navigate('/logout-success')
  }

  const isUserAccount = ['/dashboard', '/create-account'].some((p) =>
    location.pathname.startsWith(p)
  ) || location.pathname.startsWith('/user-profile/')

  const isUserProfile = [
    '/user-profile-management',
    '/create-user-profile',
    '/edit-user-profile',
  ].some((p) => location.pathname.startsWith(p))

  const isFRACategory = [
    '/fra-category-management',
    '/create-fra-category',
    '/edit-fra-category',
  ].some((p) => location.pathname.startsWith(p))

  const isFRA = [
    '/fra-management',
    '/create-fra',
    '/edit-fra',
  ].some((p) => location.pathname.startsWith(p))

  return (
    <aside className="w-[220px] h-screen sticky top-0 bg-white flex flex-col shadow-sm shrink-0 overflow-y-auto">
      <div className="p-5 border-b border-gray-100">
        <Logo size="sm" />
      </div>
      <nav className="flex flex-col gap-1 p-3 mt-2">
        {profileName === 'User Admin' && (
          <>
            <button
              onClick={() => navigate('/dashboard')}
              className={`flex items-center gap-3 px-4 py-2.5 rounded-lg font-medium text-sm text-left transition-colors ${
                isUserAccount
                  ? 'bg-blue-50 text-primary'
                  : 'text-gray-500 hover:bg-gray-50'
              }`}
            >
              <PersonIcon />
              User Account
            </button>
            <button
              onClick={() => navigate('/user-profile-management')}
              className={`flex items-center gap-3 px-4 py-2.5 rounded-lg font-medium text-sm text-left transition-colors ${
                isUserProfile
                  ? 'bg-blue-50 text-primary'
                  : 'text-gray-500 hover:bg-gray-50'
              }`}
            >
              <BadgeIcon />
              User Profile
            </button>
          </>
        )}

        {(profileName === 'Platform Management' || profileName === 'Fund Raiser') && (
          <>
            <button
              onClick={() => navigate('/fra-management')}
              className={`flex items-center gap-3 px-4 py-2.5 rounded-lg font-medium text-sm text-left transition-colors ${
                isFRA
                  ? 'bg-blue-50 text-primary'
                  : 'text-gray-500 hover:bg-gray-50'
              }`}
            >
              <MegaphoneIcon />
              FRA Activity
            </button>
          </>
        )}

        {profileName === 'Platform Management' && (
          <>
            <button
              onClick={() => navigate('/fra-category-management')}
              className={`flex items-center gap-3 px-4 py-2.5 rounded-lg font-medium text-sm text-left transition-colors ${
                isFRACategory
                  ? 'bg-blue-50 text-primary'
                  : 'text-gray-500 hover:bg-gray-50'
              }`}
            >
              <FolderIcon />
              FRA Category
            </button>
          </>
        )}

        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-cancelgray font-medium text-sm text-left hover:bg-gray-50 transition-colors"
        >
          <PowerIcon />
          Logout
        </button>
      </nav>
    </aside>
  )
}

function PersonIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
    </svg>
  )
}

function BadgeIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
    </svg>
  )
}

function FolderIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
    </svg>
  )
}

function MegaphoneIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 11v2a1 1 0 0 0 1 1h2l3 6h2l-1-6h4l5 3V7l-5 3H4a1 1 0 0 0-1 1z" />
    </svg>
  )
}

function PowerIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18.36 6.64A9 9 0 1 1 5.64 6.64" />
      <line x1="12" y1="2" x2="12" y2="12" />
    </svg>
  )
}
