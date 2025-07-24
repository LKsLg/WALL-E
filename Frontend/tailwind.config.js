module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: '#0d0d0d',
      },
      gridTemplateColumns: {
        32: 'repeat(32, minmax(0, 1fr))'
      }
    },
  },
  plugins: [],
}