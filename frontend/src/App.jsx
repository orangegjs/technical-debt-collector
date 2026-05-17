import React, { createContext, useContext, useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import LogoutPage from './pages/LogoutPage'
import DashboardPage from './pages/DashboardPage'
import UserProfilePage from './pages/UserProfilePage'
import CreateAccountPage from './pages/CreateAccountPage'
import UserProfileManagementPage from './pages/UserProfileManagementPage'
import CreateUserProfilePage from './pages/CreateUserProfilePage'
import EditUserProfilePage from './pages/EditUserProfilePage'
import FRACategoryManagementPage from './pages/FRACategoryManagementPage'
import CreateFRACategoryPage from './pages/CreateFRACategoryPage'
import EditFRACategoryPage from './pages/EditFRACategoryPage'
import FRAManagementPage from './pages/FRAManagementPage'
import CreateFRAPage from './pages/CreateFRAPage'
import EditFRAPage from './pages/EditFRAPage'
import SearchAvailableFRAPage from './pages/SearchAvailableFRAPage'
import SearchFavouritePage    from './pages/SearchFavouritePage'
import SearchDonationPage     from './pages/SearchDonationPage'
import SearchCompletedFRAPage from './pages/SearchCompletedFRAPage'
import GenerateReportPage     from './pages/GenerateReportPage'

export const AuthContext = createContext(null)

export function useAuth() {
  return useContext(AuthContext)
}

function ProtectedRoute({ children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem('fundbridger_user')
      return stored ? JSON.parse(stored) : null
    } catch {
      return null
    }
  })

  const login = (userData) => {
    setUser(userData)
    localStorage.setItem('fundbridger_user', JSON.stringify(userData))
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('fundbridger_user')
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/logout-success" element={<LogoutPage />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/user-profile/:id"
            element={
              <ProtectedRoute>
                <UserProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/create-account"
            element={
              <ProtectedRoute>
                <CreateAccountPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/user-profile-management"
            element={
              <ProtectedRoute>
                <UserProfileManagementPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/create-user-profile"
            element={
              <ProtectedRoute>
                <CreateUserProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/edit-user-profile/:id"
            element={
              <ProtectedRoute>
                <EditUserProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/fra-category-management"
            element={
              <ProtectedRoute>
                <FRACategoryManagementPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/create-fra-category"
            element={
              <ProtectedRoute>
                <CreateFRACategoryPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/edit-fra-category/:id"
            element={
              <ProtectedRoute>
                <EditFRACategoryPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/fra-management"
            element={
              <ProtectedRoute>
                <FRAManagementPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/create-fra"
            element={
              <ProtectedRoute>
                <CreateFRAPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/edit-fra/:id"
            element={
              <ProtectedRoute>
                <EditFRAPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/available-fras"
            element={
              <ProtectedRoute>
                <SearchAvailableFRAPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/favourites"
            element={
              <ProtectedRoute>
                <SearchFavouritePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/donation-history"
            element={
              <ProtectedRoute>
                <SearchDonationPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/completed-fra-history"
            element={
              <ProtectedRoute>
                <SearchCompletedFRAPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/generate-report"
            element={
              <ProtectedRoute>
                <GenerateReportPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthContext.Provider>
  )
}
