/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // ✅ Ensures all React files are scanned for classes
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb', // Tailwind blue-600
          light: '#3b82f6',   // Tailwind blue-500
          dark: '#1e40af',    // Tailwind blue-800
        },
      },
    },
  },
  plugins: [],
};
