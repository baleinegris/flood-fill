/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors:{
        dangerGradient: 'linear-gradient(90deg, #f6c6ea 0%, #f6c6ea 50%, #f6c6ea 100%)',
      }
    },
  },
  plugins: [],
}

