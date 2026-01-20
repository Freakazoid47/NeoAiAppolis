/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        'game-dark': '#0D0221',
        'game-purple': '#1A0E2E',
        'game-accent': '#FF00FF',
        'game-gold': '#FFD700',
        'game-cyan': '#00FFFF',
        'game-danger': '#FF0055',
        'game-green': '#00FF88',
      },
      animation: {
        'card-flip': 'cardFlip 0.6s ease-out',
        'glow-pulse': 'glowPulse 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
        'slide-up': 'slideUp 0.4s ease-out',
      },
      keyframes: {
        cardFlip: {
          '0%': { transform: 'translateY(0) rotateZ(0)' },
          '50%': { transform: 'translateY(-30px) rotateZ(-5deg) scale(1.05)' },
          '100%': { transform: 'translateY(0) rotateZ(0)' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(255, 215, 0, 0.5)' },
          '50%': { boxShadow: '0 0 40px rgba(255, 215, 0, 1)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        slideUp: {
          '0%': { transform: 'translateY(50px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
