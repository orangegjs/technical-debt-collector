import React, { useState } from 'react'

export default function SearchBar({ onSearch }) {
  const [value, setValue] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    onSearch(value.trim())
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-3 items-center">
      <div className="flex items-center gap-2 bg-white rounded-xl px-4 py-2.5 flex-1 border border-gray-200 shadow-sm">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2" strokeLinecap="round">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Search by User ID, User Name......"
          className="flex-1 outline-none text-sm text-gray-700 bg-transparent placeholder-gray-400"
        />
      </div>
      <button
        type="submit"
        className="bg-primary text-white px-6 py-2.5 rounded-xl text-sm font-semibold hover:bg-blue-700 transition-colors"
      >
        Search
      </button>
    </form>
  )
}
