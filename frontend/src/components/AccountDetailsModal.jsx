// BCE Boundary: :RetrieveUserAccountPage
// Methods: displayAccountDetails(), displayUserAdminDashboard()

import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function AccountDetailsModal({ user, onClose }) {
  const navigate = useNavigate()

  if (!user) return null

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
        <div className="bg-gray-50 px-8 pt-8 pb-6 flex flex-col items-start gap-3">
          <h2 className="text-xl font-bold text-navy">Account Details</h2>
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-gray-400 flex items-center justify-center shrink-0 overflow-hidden">
              {user.profile_picture_url ? (
                <img src={user.profile_picture_url} alt="avatar" className="w-full h-full object-cover" />
              ) : (
                <svg viewBox="0 0 24 24" fill="white" width="36" height="36">
                  <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
                </svg>
              )}
            </div>
            <div>
              <p className="font-bold text-gray-800 text-lg">{user.username}</p>
              <p className="text-gray-500 text-sm">{user.role}</p>
            </div>
          </div>
        </div>

        <div className="px-8 py-5 space-y-3">
          <DetailRow label="User ID" value={user.userID} />
          <DetailRow label="Email" value={user.email} />
          <DetailRow label="Role" value={user.role} />
          <DetailRow label="Status" value={user.accountStatus} />
        </div>

        <div className="px-8 pb-7 flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg bg-cancelgray text-white text-sm font-semibold hover:bg-gray-600 transition-colors"
          >
            Close
          </button>
          <button
            onClick={() => navigate(`/user-profile/${user.userID}`)}
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
    <div className="flex items-start gap-8">
      <span className="w-24 text-gray-400 text-sm shrink-0">{label}</span>
      <span className="text-gray-800 text-sm font-medium">{value ?? '—'}</span>
    </div>
  )
}
