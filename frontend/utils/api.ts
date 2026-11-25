export const API_BASE = 'http://localhost:8000/api/v1'

export function authHeaders() {
  const token = process.client ? localStorage.getItem('access_token') : null
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = localStorage.getItem('refresh_token')
  if (!refreshToken) return null
  try {
    const res = await $fetch<{ access_token: string }>(`${API_BASE}/auth/refresh`, {
      method: 'POST',
      body: { refresh_token: refreshToken },
    })
    localStorage.setItem('access_token', res.access_token)
    return res.access_token
  } catch {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    navigateTo('/login')
    return null
  }
}

export async function apiFetch<T>(url: string, opts: Record<string, any> = {}): Promise<T> {
  const headers: Record<string, string> = { ...authHeaders(), ...opts.headers }
  try {
    return await $fetch<T>(url, { ...opts, headers })
  } catch (err: any) {
    if (err?.response?.status === 401) {
      const newToken = await refreshAccessToken()
      if (newToken) {
        headers.Authorization = `Bearer ${newToken}`
        return await $fetch<T>(url, { ...opts, headers })
      }
    }
    throw err
  }
}
