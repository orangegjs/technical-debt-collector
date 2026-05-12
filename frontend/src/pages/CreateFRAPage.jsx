// BCE Boundary: :CreateFRAPage
// Methods: validateRepeatFRA(), displayDuplicateFRA(), displayFRACreatedSuccess(), displayFRACreatedFail()

import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import { createFRA, searchFRA } from '../api/fraActivityApi'
import { listFRACategories } from '../api/fraCategoryApi'
import { searchUserAcc } from '../api/userAccountApi'

const STATUSES = ['Active', 'Inactive']

export default function CreateFRAPage() {
  const navigate = useNavigate()
  const [categories, setCategories] = useState([])
  const [owners, setOwners] = useState([])
  const [loadingOptions, setLoadingOptions] = useState(true)
  const [saving, setSaving] = useState(false)
  const [globalError, setGlobalError] = useState('')
  const [errors, setErrors] = useState({})

  const [form, setForm] = useState({
    fraName: '',
    fraDescription: '',
    fraGoalAmount: '',
    fraStartDate: '',
    fraEndDate: '',
    fraStatus: 'Active',
    fraCategoryID: '',
    fraOwnerID: '',
  })

  useEffect(() => {
    async function loadOptions() {
      try {
        const [cats, users] = await Promise.all([listFRACategories(), searchUserAcc('')])
        setCategories(cats.filter((c) => c.categoryStatus === 'Active'))
        setOwners(users.filter((u) => u.accountStatus === 'Active'))
      } catch {
        setCategories([])
        setOwners([])
      } finally {
        setLoadingOptions(false)
      }
    }
    loadOptions()
  }, [])

  function handleChange(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }))
    setErrors((prev) => ({ ...prev, [field]: '' }))
    setGlobalError('')
  }

  function validateEnteredData() {
    const nextErrors = {}
    if (!form.fraName.trim()) nextErrors.fraName = 'FRA name is required.'
    if (!form.fraGoalAmount || Number(form.fraGoalAmount) <= 0) nextErrors.fraGoalAmount = 'Goal amount must be greater than 0.'
    if (!form.fraStartDate) nextErrors.fraStartDate = 'Start date is required.'
    if (!form.fraEndDate) nextErrors.fraEndDate = 'End date is required.'
    if (form.fraStartDate && form.fraEndDate && form.fraEndDate < form.fraStartDate) {
      nextErrors.fraEndDate = 'End date must be on or after start date.'
    }
    if (!form.fraCategoryID) nextErrors.fraCategoryID = 'Category is required.'
    if (!form.fraOwnerID) nextErrors.fraOwnerID = 'Owner is required.'
    return nextErrors
  }

  async function validateRepeatFRA(name) {
    try {
      const records = await searchFRA(name.trim())
      return records.some((r) => r.fraName.toLowerCase() === name.trim().toLowerCase())
    } catch {
      return false
    }
  }

  async function handleConfirm() {
    const nextErrors = validateEnteredData()
    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors)
      return
    }

    const duplicate = await validateRepeatFRA(form.fraName)
    if (duplicate) {
      setErrors({ fraName: 'FRA name already exists.' })
      return
    }

    setSaving(true)
    try {
      await createFRA({
        fraName: form.fraName.trim(),
        fraDescription: form.fraDescription.trim() || null,
        fraGoalAmount: Number(form.fraGoalAmount),
        fraStartDate: form.fraStartDate,
        fraEndDate: form.fraEndDate,
        fraStatus: form.fraStatus,
        fraCategoryID: Number(form.fraCategoryID),
        fraOwnerID: Number(form.fraOwnerID),
      })
      // displayFRACreatedSuccess
      navigate('/fra-management')
    } catch (err) {
      if (err?.detail === 'displayDuplicateFRA') {
        // displayDuplicateFRA
        setErrors({ fraName: 'FRA name already exists.' })
      } else {
        // displayFRACreatedFail
        setGlobalError('Failed to create FRA. Please try again.')
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
          <h1 className="text-2xl font-bold text-navy">Create FRA</h1>
        </header>

        <div className="flex-1 p-8 flex flex-col gap-5">
          <div className="bg-white rounded-2xl p-8 shadow-sm flex flex-col gap-6">
            <div className="grid grid-cols-2 gap-6">
              <Field label="FRA ID">
                <input
                  readOnly
                  value="Auto-generated"
                  className="w-full px-4 py-2.5 rounded-xl bg-gray-100 border border-gray-200 text-sm text-gray-400 outline-none cursor-not-allowed"
                />
              </Field>

              <Field label="FRA Status">
                <div className="relative">
                  <select
                    value={form.fraStatus}
                    onChange={(e) => handleChange('fraStatus', e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 outline-none focus:border-primary appearance-none bg-white transition-colors"
                  >
                    {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                  </select>
                  <ChevronDown />
                </div>
              </Field>

              <Field label="FRA Name" error={errors.fraName} className="col-span-2">
                <input
                  value={form.fraName}
                  onChange={(e) => handleChange('fraName', e.target.value)}
                  placeholder="e.g. Community Food Drive"
                  className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors ${errors.fraName ? 'border-deletered' : 'border-gray-200'}`}
                />
              </Field>

              <Field label="Goal Amount" error={errors.fraGoalAmount}>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={form.fraGoalAmount}
                  onChange={(e) => handleChange('fraGoalAmount', e.target.value)}
                  placeholder="e.g. 10000"
                  className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors ${errors.fraGoalAmount ? 'border-deletered' : 'border-gray-200'}`}
                />
              </Field>

              <Field label="Category" error={errors.fraCategoryID}>
                <div className="relative">
                  <select
                    value={form.fraCategoryID}
                    onChange={(e) => handleChange('fraCategoryID', e.target.value)}
                    disabled={loadingOptions}
                    className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary appearance-none bg-white transition-colors ${errors.fraCategoryID ? 'border-deletered' : 'border-gray-200'}`}
                  >
                    <option value="">Select category</option>
                    {categories.map((c) => <option key={c.categoryID} value={c.categoryID}>{c.categoryName}</option>)}
                  </select>
                  <ChevronDown />
                </div>
              </Field>

              <Field label="Start Date" error={errors.fraStartDate}>
                <input
                  type="date"
                  value={form.fraStartDate}
                  onChange={(e) => handleChange('fraStartDate', e.target.value)}
                  className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors ${errors.fraStartDate ? 'border-deletered' : 'border-gray-200'}`}
                />
              </Field>

              <Field label="End Date" error={errors.fraEndDate}>
                <input
                  type="date"
                  value={form.fraEndDate}
                  onChange={(e) => handleChange('fraEndDate', e.target.value)}
                  className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors ${errors.fraEndDate ? 'border-deletered' : 'border-gray-200'}`}
                />
              </Field>

              <Field label="Owner" error={errors.fraOwnerID} className="col-span-2">
                <div className="relative">
                  <select
                    value={form.fraOwnerID}
                    onChange={(e) => handleChange('fraOwnerID', e.target.value)}
                    disabled={loadingOptions}
                    className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary appearance-none bg-white transition-colors ${errors.fraOwnerID ? 'border-deletered' : 'border-gray-200'}`}
                  >
                    <option value="">Select owner</option>
                    {owners.map((u) => <option key={u.userID} value={u.userID}>{u.username}</option>)}
                  </select>
                  <ChevronDown />
                </div>
              </Field>
            </div>

            <Field label="FRA Description">
              <textarea
                value={form.fraDescription}
                onChange={(e) => handleChange('fraDescription', e.target.value)}
                rows={4}
                placeholder="Describe this fundraising activity"
                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 outline-none focus:border-primary transition-colors resize-none"
              />
            </Field>

            {globalError && <p className="text-deletered text-sm">{globalError}</p>}

            <div className="flex justify-end gap-3 mt-2">
              <button
                onClick={() => navigate('/fra-management')}
                className="px-5 py-2 rounded-lg bg-cancelgray text-white text-sm font-semibold hover:bg-gray-600 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirm}
                disabled={saving || loadingOptions}
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
