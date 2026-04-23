/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#1a6ff4',
        navy: '#0d1b4b',
        lightbg: '#f0f4ff',
        cardbg: '#ffffff',
        headerbg: '#dbe8ff',
        deletered: '#e53e3e',
        cancelgray: '#4a5568',
      },
      fontFamily: {
        sans: ["'DM Sans'", 'sans-serif'],
      },
    },
  },
  plugins: [],
}
