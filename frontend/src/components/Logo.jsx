import React from 'react'

export default function Logo({ size = 'md' }) {
  const textSize = size === 'sm' ? 'text-lg' : 'text-3xl'
  const iconSize = size === 'sm' ? 32 : 56

  return (
    <div className="flex items-center gap-2">
      <HandMoneyIcon size={iconSize} />
      <span className={`${textSize} font-bold leading-none`}>
        <span style={{ color: '#0d1b4b' }}>Fund</span>
        <span style={{ color: '#1a6ff4' }}>Bridger</span>
      </span>
    </div>
  )
}

function HandMoneyIcon({ size }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <ellipse cx="32" cy="48" rx="26" ry="10" fill="#1a6ff4" opacity="0.15" />
      <path
        d="M10 38c0 0 4-6 12-6h12c4 0 8-2 10-5l4-8c1-2-1-4-3-3l-8 4"
        stroke="#1a6ff4"
        strokeWidth="3"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M10 38l6 6h20c4 0 14-6 16-10"
        stroke="#1a6ff4"
        strokeWidth="3"
        strokeLinecap="round"
        fill="none"
      />
      <rect x="22" y="16" width="16" height="18" rx="4" fill="#1a6ff4" />
      <text x="30" y="29" textAnchor="middle" fontSize="10" fill="white" fontWeight="bold">$</text>
    </svg>
  )
}
