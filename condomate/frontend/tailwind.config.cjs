/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'brand-white-hueso': '#F8F8F8', // Fondo principal
        'brand-gray-light': '#E6E6E6',  // Separadores, bordes
        'brand-gray-dark': '#4A4A4A',   // Texto principal
        'brand-blue-pastel': '#A4C8F0', // Botones acción, resaltados
        'brand-green-soft': '#B2D7AC',  // Éxito
        'brand-red-light': '#F5C6C6',   // Alertas
      },
      fontFamily: {
        // Using sans as a base, assuming Helvetica Neue or Inter might need web font setup
        sans: ['Inter', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'], 
      }
    },
  },
  plugins: [],
} 