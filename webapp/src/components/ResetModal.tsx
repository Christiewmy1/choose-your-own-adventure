import { useEffect, useRef } from 'react'

interface ResetModalProps {
  bookTitle: string
  onConfirm: () => void
  onCancel: () => void
}

/**
 * Confirmation dialog for resetting a book's progress.
 *
 * Accessibility notes:
 * - `role="alertdialog"` is used (vs `dialog`) because the action is
 *   destructive and requires an immediate decision.
 * - The Cancel button receives focus on mount — the safe action is the
 *   default so a casual Enter-press can't accidentally destroy progress.
 * - Escape key is bound via a document-level listener that calls `onCancel`,
 *   matching native dialog behaviour.
 * - Clicking the backdrop also dismisses (calls `onCancel`). The inner modal
 *   card stops propagation so clicks inside don't bubble to the backdrop.
 */
export function ResetModal({ bookTitle, onConfirm, onCancel }: ResetModalProps) {
  const cancelRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    cancelRef.current?.focus()
  }, [])

  useEffect(() => {
    const handle = (e: KeyboardEvent): void => {
      if (e.key === 'Escape') onCancel()
    }
    document.addEventListener('keydown', handle)
    return () => document.removeEventListener('keydown', handle)
  }, [onCancel])

  return (
    <div
      className="modal-backdrop"
      onClick={onCancel}
      role="presentation"
    >
      <div
        className="modal"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        aria-describedby="modal-desc"
        onClick={(e) => e.stopPropagation()}
      >
        <h3 id="modal-title" className="modal-title">
          Reset Progress
        </h3>
        <p id="modal-desc" className="modal-desc">
          Clear all tracked endings for <strong>{bookTitle}</strong>?
        </p>
        <p className="modal-warn">This cannot be undone.</p>
        <div className="modal-actions">
          <button ref={cancelRef} className="btn" onClick={onCancel}>
            Cancel
          </button>
          <button className="btn btn-danger" onClick={onConfirm}>
            Reset
          </button>
        </div>
      </div>
    </div>
  )
}
