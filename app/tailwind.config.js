/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./app/**/*.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        brand: "#0E7490",
        alert: {
          low: "#22C55E",
          medium: "#EAB308",
          high: "#F97316",
          extreme: "#DC2626",
        },
      },
    },
  },
  plugins: [],
};
