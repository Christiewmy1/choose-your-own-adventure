import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ProgressBar } from '../components/ProgressBar'
import { useAllProgress } from '../hooks/useAllProgress'
import { fetchBooks, type BookSummary } from '../lib/data'

export default function Home() {
  const [books, setBooks] = useState<BookSummary[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  // One subscription at the list level — each card reads from the same map.
  const allProgress = useAllProgress()

  useEffect(() => {
    fetchBooks().then(setBooks).catch((e) => setError(String(e)))
  }, [])

  if (error) return <div className="error">Could not load books: {error}</div>
  if (!books) return <div className="loading">Loading…</div>

  const branching = books.filter((b) => b.branching_pages > 0)
  const linear = books.filter((b) => b.branching_pages === 0)

  return (
    <div className="container">
      <section className="intro">
        <h1>Choose Your Own Adventure — Reader</h1>
        <p>
          Every book here was extracted from a PDF in the{' '}
          <code>samples/</code> folder, parsed into a page-by-page graph of
          choices, and enumerated into all reachable paths. Click a book to
          start reading interactively, inspect its story graph, or browse
          every possible ending.
        </p>
      </section>

      {branching.length > 0 && (
        <section className="book-section">
          <h2>Branching adventures</h2>
          <div className="book-grid">
            {branching.map((b) => (
              <BookCard
                key={b.slug}
                book={b}
                foundEndings={allProgress[b.slug] ?? 0}
              />
            ))}
          </div>
        </section>
      )}

      {linear.length > 0 && (
        <section className="book-section">
          <h2>Linear books</h2>
          <p className="muted">
            These turned out to be computer type-in programming books or
            single-path novels — included here for completeness but have no
            branching graph.
          </p>
          <div className="book-grid">
            {linear.map((b) => (
              <BookCard key={b.slug} book={b} foundEndings={0} />
            ))}
          </div>
        </section>
      )}
    </div>
  )
}

function BookCard({
  book,
  foundEndings,
}: {
  book: BookSummary
  foundEndings: number
}) {
  const hasBranching = book.branching_pages > 0

  return (
    <Link to={`/b/${book.slug}`} className="book-card">
      <h3>{book.title}</h3>
      <div className="book-meta">
        <span className={`badge badge-${book.format}`}>{book.format}</span>
        <span className="muted">{book.pages} pages</span>
        {book.branching_pages > 0 && (
          <span className="muted">· {book.branching_pages} branches</span>
        )}
        {book.stories > 1 && (
          <span className="muted">· {book.stories} endings</span>
        )}
      </div>

      {hasBranching && (
        <div className="book-progress">
          <ProgressBar
            found={foundEndings}
            total={book.terminals}
            showLabel={foundEndings > 0}
          />
          {foundEndings === 0 && (
            <span className="progress-unstarted">Not started</span>
          )}
        </div>
      )}

      <div className="book-source">{book.source_pdf}</div>
    </Link>
  )
}
