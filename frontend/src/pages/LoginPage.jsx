// BCE Boundary: :LoginPage
// Methods: displayUserAdminDashboard(), displayLoginFail()

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../App'
import { login as apiLogin } from '../api/userAccountApi'
import Logo from '../components/Logo'

export default function LoginPage() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!username || !password) {
      setError('Please fill in all fields.')
      return
    }
    setLoading(true)
    setError('')
    try {
      const user = await apiLogin(username, password)
      login(user)
      navigate('/dashboard')
    } catch (err) {
      // displayLoginFail
      setError('Invalid username or password. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex bg-white">
      {/* Left panel */}
      <div className="flex-1 flex items-center justify-center bg-lightbg">
        <Logo size="lg" />
      </div>

      {/* Right panel */}
      <div className="flex-1 flex flex-col items-start justify-center px-16">
        <h1 className="text-4xl font-bold text-navy mb-10">Login to account</h1>
        <form onSubmit={handleSubmit} className="w-full max-w-sm flex flex-col gap-4">
          <input
            type="text"
            placeholder="*User Name"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full px-4 py-3 rounded-xl bg-blue-50 border border-blue-100 text-sm text-gray-700 outline-none focus:border-primary transition-colors"
          />
          <input
            type="password"
            placeholder="*Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 rounded-xl bg-blue-50 border border-blue-100 text-sm text-gray-700 outline-none focus:border-primary transition-colors"
          />
          {error && (
            <p className="text-deletered text-xs">{error}</p>
          )}
          <div className="flex justify-end mt-2">
            <button
              type="submit"
              disabled={loading}
              className="bg-primary text-white px-8 py-2.5 rounded-full text-sm font-semibold hover:bg-blue-700 transition-colors disabled:opacity-60"
            >
              {loading ? 'Signing in...' : 'Next'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
