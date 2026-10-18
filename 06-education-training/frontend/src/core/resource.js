// Small controller helpers shared by all views.
import { ref } from 'vue'
import { toast } from './toast'

/** Loads data once on setup and exposes { data, loading, error, reload }. */
export function useResource(loader, initial = null) {
  const data = ref(initial)
  const loading = ref(true)
  const error = ref(null)
  async function reload() {
    loading.value = true
    error.value = null
    try {
      data.value = await loader()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }
  reload()
  return { data, loading, error, reload }
}

/** Runs a mutation, shows a toast for success or failure, returns the result (or null on error). */
export async function act(fn, successMessage) {
  try {
    const result = await fn()
    if (successMessage) toast(successMessage)
    return result
  } catch (e) {
    toast(e.message, 'error')
    return null
  }
}
