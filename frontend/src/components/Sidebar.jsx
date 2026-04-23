import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../App'
import { logout as apiLogout } from '../api/userAccountApi'
import Logo from './Logo'

export default function Sidebar() {
  const navigate = useNavigate()
  const { logout } = useAuth()

  async function handleLogout() {
    try {
      await apiLogout()
    } catch {
      // proceed regardless
    }
    logout()
    navigate('/logout-success')
  }

  return (
    <aside className="w-[220px] h-screen sticky top-0 bg-white flex flex-col shadow-sm shrink-0 overflow-y-auto">
      <div className="p-5 border-b border-gray-100">
        <Logo size="sm" />
      </div>
      <nav className="flex flex-col gap-1 p-3 mt-2">
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-3 px-4 py-2.5 rounded-lg bg-blue-50 text-primary font-medium text-sm text-left"
        >
          <PersonIcon />
          User Account
        </button>
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

function PowerIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18.36 6.64A9 9 0 1 1 5.64 6.64" />
      <line x1="12" y1="2" x2="12" y2="12" />
    </svg>
  )
}
