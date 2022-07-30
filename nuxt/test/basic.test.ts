import { describe, it, expect } from 'vitest'
import { setup, $fetch } from '@nuxt/test-utils-edge'

describe('Index.vue', async () => {
  await setup({
    server: true,
  });

  it('Index Page HTML', async () => {
    const html = await $fetch('/login');
  })
})
