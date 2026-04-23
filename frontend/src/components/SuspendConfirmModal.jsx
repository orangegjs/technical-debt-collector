// BCE Boundary: :SuspendUserAccountPage
// Methods: displayConfirmationMessage(), displaySuspendSuccess(), displaySuspendFail()

import React from 'react'

export default function SuspendConfirmModal({ onConfirm, onCancel, loading }) {
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#e53e3e">
              <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
            </svg>
          </div>
          <h2 className="text-lg font-bold text-gray-800">Suspend Account ?</h2>
        </div>
        <p className="text-gray-600 text-sm mb-7">
          Suspending this account will deactivate the user. This can be reversed by updating the account status.
        </p>
        <div className="flex justify-end gap-3">
          <button
            onClick={onCancel}
            disabled={loading}
            className="px-5 py-2 rounded-lg bg-cancelgray text-white text-sm font-semibold hover:bg-gray-600 transition-colors disabled:opacity-50"
          >
            Keep Account
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className="px-5 py-2 rounded-lg bg-deletered text-white text-sm font-semibold hover:bg-red-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Suspending...' : 'Confirm'}
          </button>
        </div>
      </div>
    </div>
  )
}
