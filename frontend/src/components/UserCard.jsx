import React from 'react'

export default function UserCard({ user, onClick }) {
  return (
    <button
      onClick={() => onClick(user)}
      className="w-full flex items-center gap-4 bg-white rounded-xl px-5 py-4 shadow-sm hover:shadow-md hover:border-primary border border-transparent transition-all text-left"
    >
      <Avatar url={user.profile_picture_url} />
      <div className="flex gap-8 text-sm font-medium text-gray-700">
        <span>
          <span className="text-gray-400 mr-1">User ID:</span>
          {user.user_id}
        </span>
        <span>
          <span className="text-gray-400 mr-1">User Name:</span>
          {user.username}
        </span>
      </div>
    </button>
  )
}

function Avatar({ url }) {
  if (url) {
    return (
      <img
        src={url}
        alt="avatar"
        className="w-12 h-12 rounded-full object-cover border border-gray-200"
      />
    )
  }
  return (
    <div className="w-12 h-12 rounded-full bg-gray-300 flex items-center justify-center shrink-0">
      <svg viewBox="0 0 24 24" fill="white" width="28" height="28">
        <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
      </svg>
    </div>
  )
}
