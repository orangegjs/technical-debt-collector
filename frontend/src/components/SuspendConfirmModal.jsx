// BCE Boundary: :SuspendUserAccountPage / :SuspendUserProfilePage
// Methods: displayConfirmationMessage(), displaySuspendSuccess(), displaySuspendFail()

import React from 'react'

export default function SuspendConfirmModal({
  onConfirm,
  onCancel,
  loading,
  title = 'Set Status to Inactive?',
  message = 'This will deactivate the record. You can reactivate it later by changing the status back to Active.',
  cancelLabel = 'Cancel',
}) {
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#e53e3e">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" />
            </svg>
          </div>
          <h2 className="text-lg font-bold text-gray-800">{title}</h2>
        </div>
        <p className="text-gray-600 text-sm mb-7">{message}</p>
        <div className="flex justify-end gap-3">
          <button
            onClick={onCancel}
            disabled={loading}
            className="px-5 py-2 rounded-lg bg-cancelgray text-white text-sm font-semibold hover:bg-gray-600 transition-colors disabled:opacity-50"
          >
            {cancelLabel}
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className="px-5 py-2 rounded-lg bg-deletered text-white text-sm font-semibold hover:bg-red-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Saving...' : 'Confirm'}
          </button>
        </div>
      </div>
    </div>
  )
}
