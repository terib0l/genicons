/// <reference types="vitest" />

import { defineConfig } from "vite"
import Vue from "@vitejs/plugin-vue"

export default defineConfig({
  plugins: [
    Vue()
  ],
  test: {
    deps: {
      inline: [/@nuxt\/test-utils-edge/],
    },
    global: true,
    environment: "happy-dom",
  },
});
