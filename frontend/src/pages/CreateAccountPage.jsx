// BCE Boundary: :CreateAccountPage
// Methods: validateInput(username, password, name, email, accountStatus, role),
//          displayInvalidInput(), displayUserAccountCreatedSuccess(), displayUserAccountCreatedFail()

import React, { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import { createUserAccount } from '../api/userAccountApi'

const ROLES = ['User Admin', 'Donee', 'Platform Management', 'Fund Raiser']
const STATUSES = ['Active', 'Inactive']

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validatePassword(pw) {
  if (!pw) return 'Password is required.'
  if (pw.length < 12) return 'Must be at least 12 characters and include uppercase, lowercase, number, and symbol'
  if (!/[A-Z]/.test(pw)) return 'Must be at least 12 characters and include uppercase, lowercase, number, and symbol'
  if (!/[a-z]/.test(pw)) return 'Must be at least 12 characters and include uppercase, lowercase, number, and symbol'
  if (!/[0-9]/.test(pw)) return 'Must be at least 12 characters and include uppercase, lowercase, number, and symbol'
  if (!/[^A-Za-z0-9]/.test(pw)) return 'Must be at least 12 characters and include uppercase, lowercase, number, and symbol'
  return ''
}

export default function CreateAccountPage() {
  const navigate = useNavigate()
  const fileRef = useRef()

  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    status: 'Active',
    role: 'Donee',
    name: '',
    age: '',
    profile_picture_url: '',
  })
  const [errors, setErrors] = useState({})
  const [globalError, setGlobalError] = useState('')
  const [saving, setSaving] = useState(false)

  function handleChange(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }))
    setErrors((prev) => ({ ...prev, [field]: '' }))
    setGlobalError('')
  }

  function validateInput(username, password, name, email, accountStatus, role) {
    const errs = {}
    if (!username || !username.trim()) errs.username = 'Username is required.'
    if (!name || !name.trim()) errs.name = 'Name is required.'
    if (!email || !EMAIL_REGEX.test(email)) {
      errs.email = 'Please enter a valid email address in the format name@example.com.'
    }
    const pwErr = validatePassword(password)
    if (pwErr) errs.password = pwErr
    if (!['Active', 'Inactive'].includes(accountStatus)) errs.status = 'Status must be Active or Inactive.'
    if (!['User Admin', 'Donee', 'Platform Management', 'Fund Raiser'].includes(role)) {
      errs.role = 'Please select a valid role.'
    }
    return errs
  }

  async function handleConfirm() {
    const errs = validateInput(
      form.username,
      form.password,
      form.name,
      form.email,
      form.status,
      form.role,
    )
    if (Object.keys(errs).length > 0) {
      // displayInvalidInput
      setErrors(errs)
      return
    }
    setSaving(true)
    try {
      // displayUserAccountCreatedSuccess
      await createUserAccount(
        form.username,
        form.password,
        form.name || form.username,
        form.email,
        form.status,
        form.role,
      )
      navigate('/dashboard')
    } catch {
      // displayUserAccountCreatedFail
      setGlobalError('Failed to create account. Username or email may already be taken.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-lightbg">
      <Sidebar />
      <main className="flex-1 flex flex-col">
        <header className="bg-headerbg py-5 text-center">
          <h1 className="text-2xl font-bold text-navy">Create Account</h1>
        </header>

        <div className="flex-1 p-8 flex flex-col gap-5">
          {/* Avatar section */}
          <div className="bg-white rounded-2xl p-6 flex items-center gap-5 shadow-sm">
            <div className="relative">
              <div className="w-20 h-20 rounded-full bg-gray-400 flex items-center justify-center overflow-hidden border-2 border-gray-200">
                {form.profile_picture_url ? (
                  <img src={form.profile_picture_url} alt="avatar" className="w-full h-full object-cover" />
                ) : (
                  <svg viewBox="0 0 24 24" fill="white" width="44" height="44">
                    <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
                  </svg>
                )}
              </div>
              <button
                onClick={() => fileRef.current?.click()}
                className="absolute -bottom-1 -right-1 w-7 h-7 bg-primary rounded-full flex items-center justify-center border-2 border-white"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="white"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" /></svg>
              </button>
              <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={(e) => {
                const file = e.target.files[0]
                if (file) handleChange('profile_picture_url', URL.createObjectURL(file))
              }} />
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => fileRef.current?.click()}
                className="flex items-center gap-2 px-5 py-2 border border-gray-300 rounded-xl text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12" /></svg>
                Upload
              </button>
              <button
                onClick={() => handleChange('profile_picture_url', '')}
                className="flex items-center gap-2 px-5 py-2 border border-gray-300 rounded-xl text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="3 6 5 6 21 6" /><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6" /><path d="M10 11v6M14 11v6" /></svg>
                Remove
              </button>
            </div>
          </div>

          {/* Form section */}
          <div className="bg-white rounded-2xl p-8 shadow-sm flex flex-col gap-6">
            <div className="grid grid-cols-2 gap-6">
              <Field label="User ID">
                <input
                  readOnly
                  value="Auto-generated"
                  className="w-full px-4 py-2.5 rounded-xl bg-gray-100 border border-gray-200 text-sm text-gray-400 outline-none cursor-not-allowed"
                />
              </Field>
              <Field label="User Name" error={errors.username}>
                <input
                  value={form.username}
                  onChange={(e) => handleChange('username', e.target.value)}
                  className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors ${errors.username ? 'border-deletered' : 'border-gray-200'}`}
                />
              </Field>
              <Field label="Email" error={errors.email}>
                <input
                  value={form.email}
                  onChange={(e) => handleChange('email', e.target.value)}
                  className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors ${errors.email ? 'border-deletered' : 'border-gray-200'}`}
                />
              </Field>
              <Field label="Password" error={errors.password} hint={!errors.password ? 'Must be 8-12 characters long and include letters, numbers, and special characters.' : ''}>
                <input
                  type="password"
                  value={form.password}
                  onChange={(e) => handleChange('password', e.target.value)}
                  className={`w-full px-4 py-2.5 rounded-xl border text-sm text-gray-700 outline-none focus:border-primary transition-colors ${errors.password ? 'border-deletered' : 'border-gray-200'}`}
                />
              </Field>
              <Field label="User Status">
                <div className="relative">
                  <select
                    value={form.status}
                    onChange={(e) => handleChange('status', e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 outline-none focus:border-primary appearance-none bg-white transition-colors"
                  >
                    {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                  </select>
                  <ChevronDown />
                </div>
              </Field>
              <Field label="Role">
                <div className="relative">
                  <select
                    value={form.role}
                    onChange={(e) => handleChange('role', e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 outline-none focus:border-primary appearance-none bg-white transition-colors"
                  >
                    {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
                  </select>
                  <ChevronDown />
                </div>
              </Field>
            </div>

            {globalError && (
              <p className="text-deletered text-sm">{globalError}</p>
            )}

            <div className="flex justify-end gap-3 mt-2">
              <button
                onClick={() => navigate('/dashboard')}
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

function Field({ label, children, error, hint }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-sm font-medium text-gray-600">{label}</label>
      {children}
      {error && <p className="text-deletered text-xs">{error}</p>}
      {hint && !error && <p className="text-gray-400 text-xs">{hint}</p>}
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
