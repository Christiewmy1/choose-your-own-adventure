// ─── Storage key & schema version ─────────────────────────────────────────────
//
// Bump SCHEMA_VERSION whenever the shape of ProgressStore changes in a
// backwards-incompatible way. Stale entries with an old version are discarded
// rather than migrated, which is safe because this is supplemental user data
// (worst case: progress resets, never data loss on the canonical book data).

export const STORAGE_KEY = 'cyoa-progress-v1' as const
const SCHEMA_VERSION = 1 as const

// ─── Public types ──────────────────────────────────────────────────────────────

/**
 * Progress record for a single book, stored inside ProgressStore.books.
 * All arrays are kept sorted for stable JSON serialisation.
 */
export interface BookProgress {
  /** Sorted list of terminal page IDs the user has reached at least once. */
  readonly foundEndingPages: readonly number[]
  /**
   * Snapshot of book.terminals at the time this entry was last written.
   * Compared against the live value on mount to detect stale entries so
   * reconcileBookProgress can prune pages that no longer exist.
   */
  readonly totalEndingsSnapshot: number
  /** Unix-ms timestamp of the last write — useful for debugging / future "resume". */
  readonly lastUpdatedAt: number
}

interface ProgressStore {
  readonly version: typeof SCHEMA_VERSION
  readonly books: Readonly<Record<string, BookProgress>>
}

// ─── Defaults (avoid allocating new objects on every empty read) ───────────────

const EMPTY_STORE: ProgressStore = { version: SCHEMA_VERSION, books: {} }

export const EMPTY_BOOK_PROGRESS: BookProgress = {
  foundEndingPages: [],
  totalEndingsSnapshot: 0,
  lastUpdatedAt: 0,
}

// ─── In-process pub/sub ────────────────────────────────────────────────────────
//
// The browser `storage` event only fires in *other* tabs. For same-tab sync
// (e.g. progress bar on overview updating while reader is open) we maintain
// a lightweight listener set that is notified on every write.

type Listener = () => void
const listeners = new Set<Listener>()

/** Subscribe to in-process storage writes. Returns an unsubscribe function. */
export function subscribe(fn: Listener): () => void {
  listeners.add(fn)
  return () => {
    listeners.delete(fn)
  }
}

function notify(): void {
  listeners.forEach((fn) => fn())
}

// ─── Serialisation helpers ────────────────────────────────────────────────────

function parseStore(raw: string | null): ProgressStore {
  if (!raw) return EMPTY_STORE
  try {
    const parsed: unknown = JSON.parse(raw)
    if (
      typeof parsed !== 'object' ||
      parsed === null ||
      (parsed as Record<string, unknown>).version !== SCHEMA_VERSION
    ) {
      return EMPTY_STORE
    }
    return parsed as ProgressStore
  } catch {
    return EMPTY_STORE
  }
}

// ─── Read / write primitives ──────────────────────────────────────────────────

export function readStore(): ProgressStore {
  try {
    return parseStore(localStorage.getItem(STORAGE_KEY))
  } catch {
    // localStorage may be unavailable (private-browsing strict mode, sandboxed
    // iframe, etc.). Degrade to in-memory empty state — the app still works,
    // progress just won't persist.
    return EMPTY_STORE
  }
}

function commitStore(store: ProgressStore): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(store))
    notify()
  } catch {
    // QuotaExceededError or SecurityError — degrade silently.
  }
}

export function readBookProgress(slug: string): BookProgress {
  return readStore().books[slug] ?? EMPTY_BOOK_PROGRESS
}

export function writeBookProgress(slug: string, progress: BookProgress): void {
  const store = readStore()
  commitStore({ ...store, books: { ...store.books, [slug]: progress } })
}

// ─── Domain operations ────────────────────────────────────────────────────────

/**
 * Records that `pageId` is a discovered ending for `slug`.
 *
 * - No-ops (without a write) if the page was already recorded.
 * - Returns `true` when this is a brand-new discovery so callers can show
 *   a "new ending found" notification.
 */
export function recordEndingPage(
  slug: string,
  pageId: number,
  totalEndings: number,
): boolean {
  const current = readBookProgress(slug)
  const found = new Set(current.foundEndingPages)
  if (found.has(pageId)) return false

  found.add(pageId)
  const sorted = Array.from(found).sort((a, b) => a - b)
  writeBookProgress(slug, {
    ...current,
    foundEndingPages: sorted,
    totalEndingsSnapshot: totalEndings,
    lastUpdatedAt: Date.now(),
  })
  return true
}

/** Removes all stored progress for `slug`. */
export function resetBookProgress(slug: string): void {
  const store = readStore()
  const books = Object.fromEntries(
    Object.entries(store.books).filter(([k]) => k !== slug),
  )
  commitStore({ ...store, books })
}

/**
 * Reconcile stored progress against the *current* set of terminal node IDs.
 *
 * When the pipeline is re-run (e.g. a new book version is processed), some
 * terminal pages may disappear or new ones appear. This function:
 *   - Removes `foundEndingPages` that are no longer valid terminals.
 *   - Updates `totalEndingsSnapshot` to the current total.
 *
 * Returns the same object reference when nothing changed, so React can use
 * reference equality to skip unnecessary re-renders.
 */
export function reconcileBookProgress(
  progress: BookProgress,
  currentTotalEndings: number,
  currentTerminalIds: ReadonlySet<number>,
): BookProgress {
  const validFound = progress.foundEndingPages.filter((id) =>
    currentTerminalIds.has(id),
  )

  const snapshotUnchanged = progress.totalEndingsSnapshot === currentTotalEndings
  const foundUnchanged = validFound.length === progress.foundEndingPages.length

  if (snapshotUnchanged && foundUnchanged) return progress // nothing to do

  return {
    ...progress,
    foundEndingPages: validFound,
    totalEndingsSnapshot: currentTotalEndings,
    lastUpdatedAt: Date.now(),
  }
}
