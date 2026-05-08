// BCE Boundary: :SearchFRACategoryPage
// Methods: displayCategoryFound(result_list), displayCategoryNotFound()

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import SearchBar from '../components/SearchBar'
import { searchCategory } from '../api/fraCategoryApi'

export default function FRACategoryManagementPage() {
  const navigate = useNavigate()
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(false)
  const [noResults, setNoResults] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState(null)

  useEffect(() => {
    loadAll()
  }, [])

  async function loadAll() {
    setLoading(true)
    try {
      const results = await searchCategory('')
      setCategories(results)
      setNoResults(results.length === 0)
    } catch {
      setCategories([])
    } finally {
      setLoading(false)
    }
  }

  async function handleSearch(keyword) {
    setLoading(true)
    try {
      const results = await searchCategory(keyword)
      setCategories(results)
      setNoResults(results.length === 0)
    } catch {
      setCategories([])
      setNoResults(true)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-lightbg">
      <Sidebar />
      <main className="flex-1 p-8 flex flex-col gap-5">
        <div className="flex items-center gap-3">
          <div className="flex-1">
            <SearchBar onSearch={handleSearch} />
          </div>
          <button
            onClick={() => navigate('/create-fra-category')}
            className="flex items-center gap-2 bg-primary text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-blue-700 transition-colors shrink-0"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z" />
            </svg>
            Create Category
          </button>
        </div>

        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && noResults && (
          // displayCategoryNotFound
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <EnvelopeIllustration />
            <p className="text-gray-400 text-sm font-medium">No categories found.</p>
          </div>
        )}

        {!loading && !noResults && (
          // displayCategoryFound(result_list)
          <div className="flex flex-col gap-3">
            {categories.map((category) => (
              <CategoryCard
                key={category.categoryID}
                category={category}
                onClick={() => setSelectedCategory(category)}
              />
            ))}
          </div>
        )}
      </main>

      {selectedCategory && (
        <CategoryDetailModal
          category={selectedCategory}
          onClose={() => setSelectedCategory(null)}
          onUpdate={() => {
            setSelectedCategory(null)
            navigate(`/edit-fra-category/${selectedCategory.categoryID}`)
          }}
        />
      )}
    </div>
  )
}

function CategoryCard({ category, onClick }) {
  const desc = category.categoryDescription || ''
  const truncated = desc.length > 120 ? desc.slice(0, 120) + '…' : desc

  return (
    <button
      onClick={onClick}
      className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex flex-col gap-1 text-left hover:bg-blue-50 transition-colors w-full"
    >
      <p className="text-sm font-bold text-gray-900">{category.categoryName}</p>
      {truncated && (
        <p className="text-xs text-gray-500">{truncated}</p>
      )}
    </button>
  )
}

function CategoryDetailModal({ category, onClose, onUpdate }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md mx-4 p-7 flex flex-col gap-5">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">Category Details</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors text-lg leading-none"
          >
            ×
          </button>
        </div>

        <div className="flex flex-col gap-4">
          <p className="text-sm font-semibold text-gray-700">Category Information</p>
          <table className="w-full text-sm">
            <tbody className="divide-y divide-gray-100">
              <DetailRow label="Category ID" value={category.categoryID} />
              <DetailRow label="Category Name" value={category.categoryName} />
              <DetailRow
                label="Category Description"
                value={category.categoryDescription || <span className="text-gray-400 italic">No description</span>}
              />
              <DetailRow label="Category Status" value={category.categoryStatus} />
            </tbody>
          </table>
        </div>

        <div className="flex justify-end gap-3 pt-1">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg bg-cancelgray text-white text-sm font-semibold hover:bg-gray-600 transition-colors"
          >
            Close
          </button>
          <button
            onClick={onUpdate}
            className="px-5 py-2 rounded-lg bg-primary text-white text-sm font-semibold hover:bg-blue-700 transition-colors"
          >
            Update
          </button>
        </div>
      </div>
    </div>
  )
}

function DetailRow({ label, value }) {
  return (
    <tr>
      <td className="py-2.5 pr-4 font-medium text-gray-600 w-2/5 align-top">{label}</td>
      <td className="py-2.5 text-gray-800 align-top">{value}</td>
    </tr>
  )
}

function EnvelopeIllustration() {
  return (
    <svg width="120" height="120" viewBox="0 0 120 120" fill="none">
      <rect x="15" y="40" width="70" height="55" rx="4" fill="#e5e7eb" />
      <path d="M15 44l35 25 35-25" stroke="#d1d5db" strokeWidth="2" fill="none" />
      <rect x="20" y="20" width="40" height="30" rx="4" fill="#d1d5db" />
      <rect x="28" y="28" width="24" height="4" rx="2" fill="#9ca3af" />
      <rect x="28" y="36" width="16" height="4" rx="2" fill="#9ca3af" />
      <ellipse cx="85" cy="35" rx="18" ry="18" fill="#e5e7eb" />
      <circle cx="85" cy="31" r="2" fill="#9ca3af" />
      <circle cx="85" cy="35" r="2" fill="#9ca3af" />
      <circle cx="85" cy="39" r="2" fill="#9ca3af" />
    </svg>
  )
}
