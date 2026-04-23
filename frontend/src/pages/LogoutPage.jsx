// BCE Boundary: :LogoutPage

import React from 'react'
import { useNavigate } from 'react-router-dom'
import Logo from '../components/Logo'

export default function LogoutPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white gap-10">
      <Logo size="lg" />
      <h1 className="text-5xl font-bold text-navy">Logout successful !</h1>
      <button
        onClick={() => navigate('/login')}
        className="bg-primary text-white px-10 py-3.5 rounded-2xl text-base font-semibold hover:bg-blue-700 transition-colors"
      >
        Back to login page
      </button>
    </div>
  )
}
