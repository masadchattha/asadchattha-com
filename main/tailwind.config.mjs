/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,ts,tsx,md,mdx}'],
  theme: {
    extend: {
      colors: {
        bg: 'rgb(15 23 42)',              // slate-900
        surface: 'rgb(30 41 59)',         // slate-800
        border: 'rgb(51 65 85)',          // slate-700
        body: 'rgb(148 163 184)',         // slate-400
        heading: 'rgb(226 232 240)',      // slate-200
        strong: 'rgb(241 245 249)',       // slate-100
        accent: {
          DEFAULT: 'rgb(94 234 212)',     // teal-300
          strong: 'rgb(20 184 166)',      // teal-500
          dim: 'rgb(153 246 228)',        // teal-200
          deep: 'rgb(19 78 74)',          // teal-900 (selection fg)
        },
      },
      fontFamily: {
        sans: ['"Inter Variable"', 'Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['"JetBrains Mono Variable"', 'JetBrains Mono', 'monospace'],
      },
      letterSpacing: {
        h1: '-0.9px',
        h2: '-0.45px',
      },
      maxWidth: {
        container: '1280px',
      },
      transitionDuration: {
        300: '300ms',
      },
    },
  },
  plugins: [],
};
