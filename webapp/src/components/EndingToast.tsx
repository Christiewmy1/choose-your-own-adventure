import { useEffect } from 'react'

interface EndingToastProps {
  show: boolean
  foundCount: number
  totalEndings: number
  onDismiss: () => void
}

const AUTO_DISMISS_MS = 4_500

/**
 * Fixed-position toast that slides in from the bottom-right when `show` is
 * true and auto-dismisses after AUTO_DISMISS_MS milliseconds.
 *
 * The element is always in the DOM (never `return null`) so the CSS exit
 * transition plays out rather than cutting to invisible on dismiss. The
 * `toast-visible` class drives enter/exit via CSS transform + opacity.
 *
 * Accessibility: `role="status"` + `aria-live="polite"` lets screen readers
 * announce the discovery without interrupting the current focus.
 */
export function EndingToast({
  show,
  foundCount,
  totalEndings,
  onDismiss,
}: EndingToastProps) {
  useEffect(() => {
    if (!show) return
    const timer = setTimeout(onDismiss, AUTO_DISMISS_MS)
    return () => clearTimeout(timer)
  }, [show, onDismiss])

  return (
    <div
      className={`toast${show ? ' toast-visible' : ''}`}
      role="status"
      aria-live="polite"
      aria-atomic="true"
    >
      <span className="toast-icon" aria-hidden="true">
        ★
      </span>
      <div className="toast-body">
        <strong className="toast-title">Ending discovered!</strong>
        <span className="toast-sub">
          {foundCount} of {totalEndings} found
        </span>
      </div>
      <button
        className="toast-close"
        onClick={onDismiss}
        aria-label="Dismiss notification"
        tabIndex={show ? 0 : -1}
      >
        ×
      </button>
    </div>
  )
}
