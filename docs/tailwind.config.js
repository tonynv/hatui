/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './app/templates/**/*.njk',
    './dist/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        'ha-blue': '#41BDF5',
        'ha-dark': '#1c1c1c',
        'terminal-green': '#00ff00',
        'terminal-bg': '#0d1117'
      }
    }
  },
  plugins: []
};
