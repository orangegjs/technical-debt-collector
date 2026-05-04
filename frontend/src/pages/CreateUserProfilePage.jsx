// BCE Boundary: :CreateUserProfilePage
// Methods: validateRepeatProfile(), displayDuplicateProfile(),
//          displayUserProfileCreatedSuccess(), displayUserProfileCreatedFail()

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import { createUserProfile } from '../api/userProfileApi'

export default function CreateUserProfilePage() {
  const navigate = useNavigate()

  const [form, setForm] = useState({ profileName: '', profileDescription: '' })
  const [errors, setErrors] = useState({})
  const [globalError, setGlobalError] = useState('')
  const [saving, setSaving] = useState(false)

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
      setErrors(errs)
      return
    }
    setSaving(true)
    try {
      await createUserProfile(form.profileName.trim(), form.profileDescription.trim() || null)
      // displayUserProfileCreatedSuccess
      navigate('/user-profile-management')
    } catch (err) {
      if (err?.detail === 'displayDuplicateProfile') {
        // validateRepeatProfile → displayDuplicateProfile
        setErrors({ profileName: 'A profile with this name already exists.' })
      } else {
        // displayUserProfileCreatedFail
        setGlobalError('Failed to create profile. Please try again.')
      }
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-lightbg">
      <Sidebar />
      <main className="flex-1 flex flex-col">
        <header className="bg-headerbg py-5 text-center">
          <h1 className="text-2xl font-bold text-navy">Create User Profile</h1>
        </header>

        <div className="flex-1 p-8 flex flex-col gap-5">
          <div className="bg-white rounded-2xl p-8 shadow-sm flex flex-col gap-6">
            <div className="flex flex-col gap-6">
              <Field label="Profile ID">
                <input
                  readOnly
                  value="Auto-generated"
                  className="w-full px-4 py-2.5 rounded-xl bg-gray-100 border border-gray-200 text-sm text-gray-400 outline-none cursor-not-allowed"
                />
              </Field>

              <Field label="Profile Name" error={errors.profileName}>
                <input
                  value={form.profileName}
                  onChange={(e) => handleChange('profileName', e.target.value)}
                  placeholder="e.g. Donee, Fund Raiser"
                  className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors ${
                    errors.profileName ? 'border-deletered' : 'border-gray-200'
                  }`}
                />
              </Field>

              <Field label="Profile Description">
                <textarea
                  value={form.profileDescription}
                  onChange={(e) => handleChange('profileDescription', e.target.value)}
                  rows={4}
                  placeholder="Describe this profile role (optional)"
                  className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 outline-none focus:border-primary transition-colors resize-none"
                />
              </Field>
            </div>

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
                onClick={handleConfirm}
                disabled={saving}
                className="px-5 py-2 rounded-lg bg-primary text-white text-sm font-semibold hover:bg-blue-700 transition-colors disabled:opacity-60"
              >
                {saving ? 'Creating...' : 'Confirm'}
              </button>
            </div>
          </div>
        </div>
      </main>
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
