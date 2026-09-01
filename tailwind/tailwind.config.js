/** Extracted verbatim from the inline Play-CDN config in index.html. */
module.exports = {
  content: [require("path").join(__dirname, "..", "index.html")],

    darkMode: "class",
    theme: {
      extend: {
        colors: {
          "on-tertiary-container": "#fffdff",
          "error": "#ffb4ab",
          "on-primary": "#003910",
          "tertiary": "#e1c1a4",
          "on-secondary-container": "#9cbecc",
          "primary-fixed": "#99f89d",
          "surface-container-high": "#282b29",
          "on-tertiary-fixed-variant": "#59422d",
          "on-secondary": "#113540",
          "on-background": "#e1e3df",
          "on-primary-fixed-variant": "#00531a",
          "secondary-fixed": "#c5e8f7",
          "secondary-fixed-dim": "#aaccda",
          "background": "#111412",
          "inverse-primary": "#006e26",
          "inverse-surface": "#e1e3df",
          "surface-container-low": "#191c1a",
          "surface-tint": "#7ddb84",
          "on-primary-container": "#fbfff5",
          "on-error": "#690005",
          "on-surface": "#e1e3df",
          "surface-container": "#1d201e",
          "primary": "#7ddb84",
          "surface": "#111412",
          "surface-bright": "#373a38",
          "primary-container": "#27863a",
          "on-secondary-fixed-variant": "#2a4b57",
          "on-secondary-fixed": "#001f28",
          "on-error-container": "#ffdad6",
          "on-tertiary": "#402c18",
          "secondary": "#aaccda",
          "tertiary-fixed-dim": "#e1c1a4",
          "outline-variant": "#3f493e",
          "on-primary-fixed": "#002106",
          "secondary-container": "#2c4e5a",
          "on-tertiary-fixed": "#291806",
          "surface-dim": "#111412",
          "tertiary-container": "#8b7058",
          "error-container": "#93000a",
          "surface-container-lowest": "#0c0f0d",
          "primary-fixed-dim": "#7ddb84",
          "tertiary-fixed": "#ffdcbf",
          "surface-container-highest": "#323533",
          "inverse-on-surface": "#2e312f",
          "surface-variant": "#323533",
          "on-surface-variant": "#becaba",
          "outline": "#899486"
        },
        borderRadius: {
          DEFAULT: "0.25rem",
          lg: "0.5rem",
          xl: "0.75rem",
          full: "9999px"
        },
        fontFamily: {
          headline: ["Epilogue"],
          body: ["Plus Jakarta Sans"],
          label: ["Work Sans"]
        }
      }
    },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/container-queries")],
};
