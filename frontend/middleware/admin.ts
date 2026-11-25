export default defineNuxtRouteMiddleware((to, from) => {
  if (process.client) {
    const token = localStorage.getItem('access_token')
    if (!token) {
      return navigateTo('/login')
    }
    const user = localStorage.getItem('user')
    if (user) {
      const role = JSON.parse(user).role
      if (role !== 'admin' && role !== 'super_admin') {
        return navigateTo('/profile')
      }
    }
  }
})
