import { defineNuxtConfig } from 'nuxt'

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  app: {
    head: {
      "title": "Genicons",
      "charset": "utf-8",
      "viewport": "width=device-width, initial-scale=1",
      "meta": [],
      "link": [
        {rel: "icon", type: "image/jpg", href: "/favicon.jpg"}
      ],
      "style": [],
      "script": [],
    }
  },
  build: {
    postcss: {
      postcssOptions: {
        plugins: {
          tailwindcss: {},
          autoprefixer: {},
        },
      },
    },
  },
  css: [
    "@/assets/css/tailwind.css"
  ],
  modules: [
  ],
  ssr: true,
})
