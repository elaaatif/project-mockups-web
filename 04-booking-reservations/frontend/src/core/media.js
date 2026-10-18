/** Sized image URL for Unsplash-hosted photos (backend stores the base URL). */
export const img = (url, width = 600) => (url ? `${url}&w=${width}&q=75` : '')
