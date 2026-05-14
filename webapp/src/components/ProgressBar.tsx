interface ProgressBarProps {
  found: number
  total: number
  /** Render the "X / Y endings" text label. Defaults to true. */
  showLabel?: boolean
  className?: string
}

/**
 * Accessible progress bar using the ARIA progressbar role.
 * `aria-valuenow`, `aria-valuemin`, `aria-valuemax` are set so screen readers
 * announce the value without relying on the visual fill width.
 *
 * The fill width is driven by an inline style (computed from props) so it
 * works without any JavaScript animation library — a CSS transition on the
 * `.progress-fill` class provides the smooth interpolation.
 */
export function ProgressBar({
  found,
  total,
  showLabel = true,
  className,
}: ProgressBarProps) {
  const pct = total > 0 ? Math.min((found / total) * 100, 100) : 0
  const ariaLabel = `${found} of ${total} endings found`

  return (
    <div className={`progress-wrap${className ? ` ${className}` : ''}`}>
      <div
        className="progress-track"
        role="progressbar"
        aria-valuenow={found}
        aria-valuemin={0}
        aria-valuemax={total}
        aria-label={ariaLabel}
      >
        <div
          className="progress-fill"
          style={{ width: `${pct}%` }}
        />
      </div>
      {showLabel && (
        <span className="progress-label" aria-hidden="true">
          {found}&thinsp;/&thinsp;{total}
        </span>
      )}
    </div>
  )
}
