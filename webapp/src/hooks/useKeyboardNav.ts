import { useEffect, useRef } from 'react'
import type { Choice } from '../lib/data'

export interface KeyboardNavOptions {
  /** Current page's outgoing choices (determines which number keys are live). */
  choices: Choice[]
  /** Whether the back action is currently possible. */
  canGoBack: boolean
  /** Whether the graph shortcut should be active (false for linear books). */
  hasGraph: boolean
  onChoose: (target: number) => void
  onBack: () => void
  onRestart: () => void
  onGraph: () => void
}

/**
 * Binds keyboard shortcuts for the reader. Bound keys:
 *
 *   ←  /  Backspace  → back one page (when canGoBack)
 *   1 – 9            → pick the Nth choice (when N ≤ choices.length)
 *   R                → restart from the first page
 *   G                → jump to the story graph (when hasGraph)
 *
 * Design decisions:
 * - The listener is registered exactly once (empty dep array). All current
 *   values are read from `optRef` — a ref that is updated on every render —
 *   so the closure is never stale without triggering re-registration.
 * - Focus guard: listeners are ignored when the active element is an INPUT,
 *   TEXTAREA, SELECT, or any contenteditable node to prevent eating keystrokes
 *   while the user is typing.
 * - Cleanup: the `removeEventListener` in the effect cleanup is guaranteed to
 *   run on unmount, preventing memory leaks.
 */
export function useKeyboardNav(options: KeyboardNavOptions): void {
  const optRef = useRef(options)
  optRef.current = options

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent): void {
      // Do not intercept when focus is inside an interactive text element.
      const target = e.target as HTMLElement
      if (
        target.tagName === 'INPUT' ||
        target.tagName === 'TEXTAREA' ||
        target.tagName === 'SELECT' ||
        target.isContentEditable
      ) {
        return
      }

      const { choices, canGoBack, hasGraph, onChoose, onBack, onRestart, onGraph } =
        optRef.current

      switch (e.key) {
        case 'ArrowLeft':
        case 'Backspace':
          if (canGoBack) {
            e.preventDefault()
            onBack()
          }
          break

        case 'r':
        case 'R':
          e.preventDefault()
          onRestart()
          break

        case 'g':
        case 'G':
          if (hasGraph) {
            e.preventDefault()
            onGraph()
          }
          break

        default: {
          const n = parseInt(e.key, 10)
          if (!Number.isNaN(n) && n >= 1 && n <= 9 && n <= choices.length) {
            e.preventDefault()
            onChoose(choices[n - 1].target)
          }
        }
      }
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, []) // empty — optRef provides currency without re-registration
}
