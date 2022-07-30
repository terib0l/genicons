import { useAuth } from '@/composables/useAuth'

export default defineNuxtRouteMiddleware(async (to, form) => {
  const { accessToken, logout } = useAuth();

  if (!accessToken.value && to.path !== '/login'){
    await logout()
    return navigateTo('/login')
  }
})
