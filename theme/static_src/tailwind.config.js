/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Tell Tailwind to scan Django templates
    '../../**/templates/**/*.html',
    '../../templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          light: '#ff7f7f',
          DEFAULT: '#ff4949',
          dark: '#cc0000',
        },
      },
      borderRadius: {
        xl: '1.5rem',
      },
    },
  },
  plugins: [],
}
