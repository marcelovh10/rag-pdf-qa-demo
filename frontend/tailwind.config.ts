import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0a0a0a",
        panel: "#141414",
        border: "#262626",
        accent: "#10a37f",
      },
    },
  },
  plugins: [],
};
export default config;
