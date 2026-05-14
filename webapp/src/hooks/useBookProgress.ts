import { useCallback, useEffect, useRef, useState } from 'react'
import {
  EMPTY_BOOK_PROGRESS,
  STORAGE_KEY,
  readBookProgress,
  recordEndingPage as persistEndingPage,
  reconcileBookProgress,
  resetBookProgress as clearBookProgress,
  subscribe,
  writeBookProgress,
  type BookProgress,
} from '../lib/progress'

export interface UseBookProgressOptions {
  slug: string
  /** Total terminal-node count from book manifest (book.terminals). */
  totalEndings: number
  /**
   * Full set of valid terminal node IDs from the loaded graph.
   * When provided, triggers a one-time reconciliation to prune any stale
   * entries caused by pipeline re-runs changing the terminal set.
   */
  terminalIds?: ReadonlySet<number>
}

export interface UseBookProgressResult {
  readonly progress: BookProgress
  /** Convenience alias: progress.foundEndingPages.length */
  readonly foundCount: number
  /**
   * True for exactly one render cycle after a brand-new ending is recorded.
   * Callers should reset this via `clearNewEnding` once the toast is shown.
   */
  readonly isNewEnding: boolean
  /** Record that the user reached this terminal page. */
  readonly recordEnding: (pageId: number) => void
  /** Reset `isNewEnding` to false (call from toast dismiss / auto-dismiss). */
  readonly clearNewEnding: () => void
  /** Wipe all progress for this book (confirmation handled by the caller). */
  readonly reset: () => void
}

export function useBookProgress({
  slug,
  totalEndings,
  terminalIds,
}: UseBookProgressOptions): UseBookProgressResult {
  const [progress, setProgress] = useState<BookProgress>(
    () => readBookProgress(slug),
  )
  const [isNewEnding, setIsNewEnding] = useState(false)

  // Stable ref so effect callbacks always read the latest slug without
  // being listed as effect dependencies (avoids re-registering listeners).
  const slugRef = useRef(slug)
  slugRef.current = slug

  // Re-hydrate local state whenever slug changes (navigating between books).
  useEffect(() => {
    setProgress(readBookProgress(slug))
    setIsNewEnding(false)
  }, [slug])

  // ── Cross-tab + same-tab sync ──────────────────────────────────────────────
  //
  // `subscribe` catches writes from the same JavaScript process (same tab).
  // The `storage` event catches writes from other tabs/windows for the same
  // origin. Together they keep all consumers of this hook in sync.
  useEffect(() => {
    const sync = (): void => setProgress(readBookProgress(slugRef.current))

    const unsub = subscribe(sync)
    const handleStorage = (e: StorageEvent): void => {
      if (e.key === STORAGE_KEY) sync()
    }
    window.addEventListener('storage', handleStorage)
    return () => {
      unsub()
      window.removeEventListener('storage', handleStorage)
    }
  }, []) // intentionally empty — uses slugRef for currency

  // ── One-time reconciliation ────────────────────────────────────────────────
  //
  // Runs once per slug as soon as terminalIds becomes available (after the
  // graph finishes loading). Uses a ref to ensure it fires at most once per
  // slug even under React StrictMode's double-invoke pattern.
  const reconciledSlugRef = useRef<string | null>(null)
  useEffect(() => {
    if (!terminalIds || reconciledSlugRef.current === slug) return
    reconciledSlugRef.current = slug

    const current = readBookProgress(slug)
    const reconciled = reconcileBookProgress(current, totalEndings, terminalIds)
    if (reconciled !== current) {
      // writeBookProgress triggers notify() → the subscribe listener above
      // calls setProgress() automatically, so no manual setState needed.
      writeBookProgress(slug, reconciled)
    }
  }, [slug, totalEndings, terminalIds])

  // ── Actions ────────────────────────────────────────────────────────────────

  const recordEnding = useCallback(
    (pageId: number): void => {
      const isNew = persistEndingPage(slugRef.current, pageId, totalEndings)
      if (isNew) setIsNewEnding(true)
      // If not new, persistEndingPage skips the write — no unnecessary render.
    },
    [totalEndings],
  )

  const clearNewEnding = useCallback((): void => setIsNewEnding(false), [])

  const reset = useCallback((): void => {
    clearBookProgress(slugRef.current)
    setProgress(EMPTY_BOOK_PROGRESS)
  }, [])

  return {
    progress,
    foundCount: progress.foundEndingPages.length,
    isNewEnding,
    recordEnding,
    clearNewEnding,
    reset,
  }
}
