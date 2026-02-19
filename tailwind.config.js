/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        physica: {
          DEFAULT: '#6c8ea1',
          50: '#f4f7f9',
          100: '#e8eff3',
          200: '#d1dfe7',
          300: '#a9c3d3',
          400: '#8aa9bc',
          500: '#6c8ea1',
          600: '#577486',
          700: '#475e6d',
          800: '#3d4f5b',
          900: '#36444e',
        },
      },
    },
  },
  plugins: [],
}
