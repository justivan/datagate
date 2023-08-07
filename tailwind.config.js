/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{html,js}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          "50": "#f3faf8",
          "100": "#d7f0eb",
          "200": "#b0dfd8",
          "300": "#6bbfb5",
          "400": "#55aca4",
          "500": "#3c908a",
          "600": "#2e7370",
          "700": "#285d5b",
          "800": "#244b4a",
          "900": "#21403f",
          "950": "#0e2525",
        },
      },
      fontFamily: {
        sans: ["Inter"],
      },
      spacing: {
        "13": "3.25rem",
        "15": "3.75rem",
        "128": "32rem",
        "144": "36rem",
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
};