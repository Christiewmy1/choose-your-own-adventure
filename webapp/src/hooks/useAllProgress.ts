import { useEffect, useMemo, useState } from 'react'
import { STORAGE_KEY, readStore, subscribe } from '../lib/progress'

/**
 * Returns a stable map of `{ slug → foundEndingCount }` covering every book
 * that has any recorded progress. Re-renders only when the underlying store
 * actually changes. Stays in sync across tabs via the `storage` event and
 * across same-tab writes via the pub/sub bus in lib/progress.ts.
 *
 * Used by Home.tsx to annotate every book card without each card needing its
 * own listener (one subscription at the list level is enough).
 */
export function useAllProgress(): Readonly<Record<string, number>> {
  const [store, setStore] = useState(readStore)

  useEffect(() => {
    const sync = (): void => setStore(readStore())

    const unsub = subscribe(sync)
    const handleStorage = (e: StorageEvent): void => {
      if (e.key === STORAGE_KEY) sync()
    }
    window.addEventListener('storage', handleStorage)
    return () => {
      unsub()
      window.removeEventListener('storage', handleStorage)
    }
  }, [])

  // Derive the slug→count map only when the store object reference changes.
  return useMemo(
    () =>
      Object.fromEntries(
        Object.entries(store.books).map(([slug, bp]) => [
          slug,
          bp.foundEndingPages.length,
        ]),
      ),
    [store],
  )
}
