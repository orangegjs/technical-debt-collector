// BCE Boundary: :CreateUserProfilePage
// Methods: validateRepeatProfile(), displayDuplicateProfile(),
//          displayUserProfileCreatedSuccess(), displayUserProfileCreatedFail()

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import { createUserProfile, searchUserProfile } from '../api/userProfileApi'

const STATUSES = ['Active', 'Inactive']

export default function CreateUserProfilePage() {
  const navigate = useNavigate()

  const [form, setForm] = useState({ profileName: '', profileDescription: '', profileStatus: 'Active' })
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
    if (!form.profileDescription.trim()) errs.profileDescription = 'Profile description is required.'
    return errs
  }

  async function validateRepeatProfile(profileName) {
    try {
      const results = await searchUserProfile(profileName.trim())
      return results.some((p) => p.profileName.toLowerCase() === profileName.trim().toLowerCase())
    } catch {
      return false
    }
  }

  async function handleConfirm() {
    const errs = validateEnteredData()
    if (Object.keys(errs).length > 0) {
      setErrors(errs)
      return
    }
    // validateRepeatProfile
    const isDuplicate = await validateRepeatProfile(form.profileName)
    if (isDuplicate) {
      // displayDuplicateProfile
      setErrors({ profileName: 'A profile with this name already exists.' })
      return
    }
    setSaving(true)
    try {
      await createUserProfile(
        form.profileName.trim(),
        form.profileDescription.trim(),
        form.profileStatus,
      )
      // displayUserProfileCreatedSuccess
      navigate('/user-profile-management')
    } catch {
      // displayUserProfileCreatedFail
      setGlobalError('Failed to create profile. Please try again.')
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
            <div className="grid grid-cols-2 gap-6">
              <Field label="Profile ID">
                <input
                  readOnly
                  value="Auto-generated"
                  className="w-full px-4 py-2.5 rounded-xl bg-gray-100 border border-gray-200 text-sm text-gray-400 outline-none cursor-not-allowed"
                />
              </Field>

              <Field label="Profile Status">
                <div className="relative">
                  <select
                    value={form.profileStatus}
                    onChange={(e) => handleChange('profileStatus', e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 outline-none focus:border-primary appearance-none bg-white transition-colors"
                  >
                    {STATUSES.map((s) => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                  <ChevronDown />
                </div>
              </Field>

              <Field label="Profile Name" error={errors.profileName} className="col-span-2">
                <input
                  value={form.profileName}
                  onChange={(e) => handleChange('profileName', e.target.value)}
                  placeholder="e.g. Donee, Fund Raiser"
                  className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors ${
                    errors.profileName ? 'border-deletered' : 'border-gray-200'
                  }`}
                />
              </Field>
            </div>

            <Field label="Profile Description" error={errors.profileDescription}>
              <textarea
                value={form.profileDescription}
                onChange={(e) => handleChange('profileDescription', e.target.value)}
                rows={4}
                placeholder="Describe this profile role"
                className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors resize-none ${
                  errors.profileDescription ? 'border-deletered' : 'border-gray-200'
                }`}
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

function Field({ label, children, error, className }) {
  return (
    <div className={`flex flex-col gap-1.5 ${className || ''}`}>
      <label className="text-sm font-medium text-gray-600">{label}</label>
      {children}
      {error && <p className="text-deletered text-xs">{error}</p>}
    </div>
  )
}

function ChevronDown() {
  return (
    <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6b7280" strokeWidth="2" strokeLinecap="round">
        <polyline points="6 9 12 15 18 9" />
      </svg>
    </div>
  )
}
