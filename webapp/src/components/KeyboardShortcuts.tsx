import { useState } from 'react'

interface Shortcut {
  keys: readonly string[]
  label: string
}

const ALL_SHORTCUTS: readonly Shortcut[] = [
  { keys: ['←', 'Backspace'], label: 'Go back' },
  { keys: ['1 – 9'], label: 'Pick choice' },
  { keys: ['R'], label: 'Restart' },
  { keys: ['G'], label: 'View graph' },
]

interface KeyboardShortcutsProps {
  hasGraph: boolean
}

/**
 * Toggleable shortcut legend rendered inline in the reader controls row.
 * The `G` shortcut is omitted for linear books (hasGraph = false).
 */
export function KeyboardShortcuts({ hasGraph }: KeyboardShortcutsProps) {
  const [open, setOpen] = useState(false)

  const shortcuts = hasGraph
    ? ALL_SHORTCUTS
    : ALL_SHORTCUTS.filter((s) => !s.keys.includes('G'))

  return (
    <div className="kb-shortcuts">
      <button
        className="btn btn-ghost btn-small"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        aria-controls="kb-panel"
      >
        ⌨ Shortcuts
      </button>
      {open && (
        <div id="kb-panel" className="kb-panel" role="tooltip">
          {shortcuts.map((s) => (
            <div key={s.label} className="kb-row">
              <span className="kb-keys">
                {s.keys.map((k) => (
                  <kbd key={k}>{k}</kbd>
                ))}
              </span>
              <span className="kb-desc">{s.label}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
