import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ProgressBar } from '../components/ProgressBar'
import { ResetModal } from '../components/ResetModal'
import { useBookProgress } from '../hooks/useBookProgress'
import { fetchBooks, type BookSummary } from '../lib/data'

export default function BookOverview() {
  const { slug } = useParams<{ slug: string }>()
  const [book, setBook] = useState<BookSummary | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [showResetModal, setShowResetModal] = useState(false)

  useEffect(() => {
    fetchBooks()
      .then((bs) => {
        const b = bs.find((x) => x.slug === slug)
        if (!b) setError('Book not found')
        else setBook(b)
      })
      .catch((e) => setError(String(e)))
  }, [slug])

  const { foundCount, reset } = useBookProgress({
    slug: slug ?? '',
    totalEndings: book?.terminals ?? 0,
    // terminalIds not provided here — reconciliation happens in the reader
    // where the graph is already loaded. Avoids an extra network fetch.
  })

  const handleConfirmReset = (): void => {
    reset()
    setShowResetModal(false)
  }

  if (error) return <div className="container error">{error}</div>
  if (!book) return <div className="container loading">Loading…</div>

  const isBranching = book.branching_pages > 0

  return (
    <div className="container">
      <BookHeader book={book} active="overview" />

      <div className="overview-grid">
        <Stat label="Pages extracted" value={book.pages} />
        <Stat label="Graph edges" value={book.edges} />
        <Stat label="Branching pages" value={book.branching_pages} />
        <Stat label="Endings" value={book.terminals} />
        <Stat
          label="Enumerated paths"
          value={book.stories}
          hint={
            book.stories > 1
              ? 'bounded by 20 decision points'
              : book.branching_pages === 0
                ? 'linear book, single path'
                : undefined
          }
        />
        <Stat
          label="Start page"
          value={book.start_page ?? '—'}
          hint={
            book.start_page != null
              ? `The story opens at page ${book.start_page}`
              : undefined
          }
        />
      </div>

      {isBranching && (
        <section className="progress-section">
          <div className="progress-section-head">
            <h3>Your progress</h3>
            {foundCount > 0 && (
              <button
                className="btn btn-ghost btn-small"
                onClick={() => setShowResetModal(true)}
              >
                Reset
              </button>
            )}
          </div>
          <ProgressBar
            found={foundCount}
            total={book.terminals}
            className="progress-overview"
          />
          <p className="progress-detail muted">
            {foundCount === 0
              ? `No endings found yet. There are ${book.terminals} to discover.`
              : foundCount === book.terminals
                ? `All ${book.terminals} endings found!`
                : `${foundCount} of ${book.terminals} endings discovered — ${book.terminals - foundCount} remaining.`}
          </p>
        </section>
      )}

      <section className="overview-actions">
        <Link
          to={`/b/${book.slug}/read${
            book.start_page != null ? `/${book.start_page}` : ''
          }`}
          className="btn btn-primary"
        >
          {foundCount > 0 ? 'Keep reading' : 'Start reading'}
        </Link>
        {book.branching_pages > 0 && (
          <>
            <Link to={`/b/${book.slug}/graph`} className="btn">
              View story graph
            </Link>
            <Link to={`/b/${book.slug}/endings`} className="btn">
              All endings ({book.stories})
            </Link>
          </>
        )}
      </section>

      <section className="overview-source">
        <h3>Source</h3>
        <p className="muted">
          Extracted from <code>samples/{book.source_pdf}</code>. Format tag:{' '}
          <code>{book.format}</code>, reference style:{' '}
          <code>{book.reference_style}</code>.
        </p>
      </section>

      {showResetModal && (
        <ResetModal
          bookTitle={book.title}
          onConfirm={handleConfirmReset}
          onCancel={() => setShowResetModal(false)}
        />
      )}
    </div>
  )
}

function Stat({
  label,
  value,
  hint,
}: {
  label: string
  value: number | string
  hint?: string
}) {
  return (
    <div className="stat">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
      {hint && <div className="stat-hint">{hint}</div>}
    </div>
  )
}

export function BookHeader({
  book,
  active,
}: {
  book: { slug: string; title: string; branching_pages: number; start_page: number | null }
  active: 'overview' | 'read' | 'graph' | 'endings'
}) {
  const branches = book.branching_pages > 0
  return (
    <div className="book-header">
      <Link to="/" className="backlink">
        ← All books
      </Link>
      <h1>{book.title}</h1>
      <nav className="book-tabs">
        <TabLink to={`/b/${book.slug}`} active={active === 'overview'}>
          Overview
        </TabLink>
        <TabLink
          to={`/b/${book.slug}/read${
            book.start_page != null ? `/${book.start_page}` : ''
          }`}
          active={active === 'read'}
        >
          Read
        </TabLink>
        {branches && (
          <>
            <TabLink
              to={`/b/${book.slug}/graph`}
              active={active === 'graph'}
            >
              Graph
            </TabLink>
            <TabLink
              to={`/b/${book.slug}/endings`}
              active={active === 'endings'}
            >
              Endings
            </TabLink>
          </>
        )}
      </nav>
    </div>
  )
}

function TabLink({
  to,
  active,
  children,
}: {
  to: string
  active: boolean
  children: React.ReactNode
}) {
  return (
    <Link to={to} className={`book-tab ${active ? 'is-active' : ''}`}>
      {children}
    </Link>
  )
}
