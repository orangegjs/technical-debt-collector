// BCE Boundary: :UpdateUserProfilePage / :SuspendUserProfilePage
// Methods: displayUserProfile(), validateEnteredData(), displayInputErrorMessage(),
//          displayUpdateSuccess(), displayConfirmationMessage(), displaySuspendSuccess(), displaySuspendFail()

import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import SuspendConfirmModal from '../components/SuspendConfirmModal'
import { retrieveUserProfile, updateUserProfile, suspendUserProfile } from '../api/userProfileApi'

export default function EditUserProfilePage() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [form, setForm] = useState({ profileName: '', profileDescription: '' })
  const [profileStatus, setProfileStatus] = useState('Active')
  const [profileID, setProfileID] = useState(null)
  const [errors, setErrors] = useState({})
  const [globalError, setGlobalError] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [showSuspend, setShowSuspend] = useState(false)
  const [suspending, setSuspending] = useState(false)

  useEffect(() => {
    async function load() {
      try {
        // displayUserProfile()
        const profile = await retrieveUserProfile(Number(id))
        setProfileID(profile.profileID)
        setProfileStatus(profile.profileStatus)
        setForm({
          profileName: profile.profileName || '',
          profileDescription: profile.profileDescription || '',
        })
      } catch {
        setGlobalError('Failed to load profile.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [id])

  function handleChange(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }))
    setErrors((prev) => ({ ...prev, [field]: '' }))
    setGlobalError('')
  }

  function validateEnteredData() {
    const errs = {}
    if (!form.profileName.trim()) errs.profileName = 'Profile name is required.'
    return errs
  }

  async function handleConfirm() {
    const errs = validateEnteredData()
    if (Object.keys(errs).length > 0) {
      // displayInputErrorMessage
      setErrors(errs)
      return
    }
    setSaving(true)
    try {
      await updateUserProfile(Number(id), {
        profileName: form.profileName.trim(),
        profileDescription: form.profileDescription.trim() || null,
      })
      // displayUpdateSuccess
      navigate('/user-profile-management')
    } catch {
      // displayInputErrorMessage
      setGlobalError('Failed to update profile. Please check your inputs.')
    } finally {
      setSaving(false)
    }
  }

  async function handleSuspend() {
    setSuspending(true)
    try {
      await suspendUserProfile(Number(id))
      // displaySuspendSuccess
      navigate('/user-profile-management')
    } catch {
      // displaySuspendFail
      setGlobalError('Failed to suspend profile.')
      setShowSuspend(false)
    } finally {
      setSuspending(false)
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-screen">
        <Sidebar />
        <main className="flex-1 bg-lightbg flex items-center justify-center">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        </main>
      </div>
    )
  }

  const isActive = profileStatus === 'Active'

  return (
    <div className="flex min-h-screen bg-lightbg">
      <Sidebar />
      <main className="flex-1 flex flex-col">
        <header className="bg-headerbg py-5 text-center">
          <h1 className="text-2xl font-bold text-navy">Edit User Profile</h1>
        </header>

        <div className="flex-1 p-8 flex flex-col gap-5">
          <div className="bg-white rounded-2xl p-8 shadow-sm flex flex-col gap-6">
            <div className="grid grid-cols-2 gap-6">
              <Field label="Profile ID">
                <input
                  readOnly
                  value={profileID ?? ''}
                  className="w-full px-4 py-2.5 rounded-xl bg-gray-100 border border-gray-200 text-sm text-gray-500 outline-none cursor-not-allowed"
                />
              </Field>

              <Field label="Profile Status">
                <div className="flex items-center h-[42px]">
                  <span
                    className={`text-xs font-semibold px-3 py-1 rounded-full ${
                      isActive ? 'bg-green-100 text-green-700' : 'bg-red-100 text-deletered'
                    }`}
                  >
                    {profileStatus}
                  </span>
                </div>
              </Field>

              <Field label="Profile Name" error={errors.profileName}>
                <input
                  value={form.profileName}
                  onChange={(e) => handleChange('profileName', e.target.value)}
                  className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors ${
                    errors.profileName ? 'border-deletered' : 'border-gray-200'
                  }`}
                />
              </Field>
            </div>

            <Field label="Profile Description">
              <textarea
                value={form.profileDescription}
                onChange={(e) => handleChange('profileDescription', e.target.value)}
                rows={4}
                placeholder="Describe this profile role (optional)"
                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 outline-none focus:border-primary transition-colors resize-none"
              />
            </Field>

            {globalError && (
              <p className="text-deletered text-sm">{globalError}</p>
            )}

            <div className="flex justify-end gap-3 mt-2">
              <button
                onClick={() => navigate('/user-profile-management')}
                className="px-5 py-2 rounded-lg bg-cancelgray text-white text-sm font-semibold hover:bg-gray-600 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => setShowSuspend(true)}
                disabled={!isActive}
                className="px-5 py-2 rounded-lg bg-deletered text-white text-sm font-semibold hover:bg-red-700 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Suspend Profile
              </button>
              <button
                onClick={handleConfirm}
                disabled={saving}
                className="px-5 py-2 rounded-lg bg-primary text-white text-sm font-semibold hover:bg-blue-700 transition-colors disabled:opacity-60"
              >
                {saving ? 'Saving...' : 'Confirm'}
              </button>
            </div>
          </div>
        </div>
      </main>

      {showSuspend && (
        <SuspendConfirmModal
          onConfirm={handleSuspend}
          onCancel={() => setShowSuspend(false)}
          loading={suspending}
        />
      )}
    </div>
  )
}

function Field({ label, children, error }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-sm font-medium text-gray-600">{label}</label>
      {children}
      {error && <p className="text-deletered text-xs">{error}</p>}
    </div>
  )
}
