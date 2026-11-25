export function useSmoothScroll() {
  const scrollToSection = (id: string) => {
    const el = document.getElementById(id)
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return { scrollToSection, scrollToTop }
}

export function useIntersectionObserver() {
  const observer = ref<IntersectionObserver | null>(null)

  const createObserver = (callback: IntersectionObserverCallback, options?: IntersectionObserverInit) => {
    observer.value = new IntersectionObserver(callback, options)
    return observer.value
  }

  const observe = (el: HTMLElement) => {
    observer.value?.observe(el)
  }

  onUnmounted(() => {
    observer.value?.disconnect()
  })

  return { createObserver, observe }
}
