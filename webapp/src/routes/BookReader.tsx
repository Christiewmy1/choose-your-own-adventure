import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { EndingToast } from '../components/EndingToast'
import { KeyboardShortcuts } from '../components/KeyboardShortcuts'
import { useBookProgress } from '../hooks/useBookProgress'
import { useKeyboardNav } from '../hooks/useKeyboardNav'
import {
  fetchBooks,
  fetchGraph,
  fetchPage,
  nodeById,
  stripPageHeader,
  type BookSummary,
  type Choice,
  type Graph,
  type Node,
} from '../lib/data'
import { BookHeader } from './BookOverview'

export default function BookReader() {
  const { slug, page: pageParam } = useParams<{ slug: string; page?: string }>()
  const navigate = useNavigate()

  const [book, setBook] = useState<BookSummary | null>(null)
  const [graph, setGraph] = useState<Graph | null>(null)
  const [pageText, setPageText] = useState<string>('')
  const [loadingPage, setLoadingPage] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [history, setHistory] = useState<number[]>([])

  // ── Data loading ───────────────────────────────────────────────────────────

  useEffect(() => {
    if (!slug) return
    let cancelled = false
    Promise.all([fetchBooks(), fetchGraph(slug)])
      .then(([books, g]) => {
        if (cancelled) return
        const b = books.find((x) => x.slug === slug)
        if (!b) {
          setError('Book not found')
          return
        }
        setBook(b)
        setGraph(g)
      })
      .catch((e) => !cancelled && setError(String(e)))
    return () => {
      cancelled = true
    }
  }, [slug])

  const currentPage = useMemo(() => {
    if (pageParam) return parseInt(pageParam, 10)
    return graph?.start_page ?? null
  }, [pageParam, graph])

  const currentNode: Node | undefined = useMemo(
    () => (graph && currentPage != null ? nodeById(graph, currentPage) : undefined),
    [graph, currentPage],
  )

  useEffect(() => {
    if (!slug || currentPage == null) return
    let cancelled = false
    setLoadingPage(true)
    fetchPage(slug, currentPage)
      .then((t) => {
        if (!cancelled) setPageText(stripPageHeader(t))
      })
      .catch((e) => !cancelled && setError(String(e)))
      .finally(() => !cancelled && setLoadingPage(false))
    return () => {
      cancelled = true
    }
  }, [slug, currentPage])

  useEffect(() => {
    if (currentPage == null) return
    setHistory((h) => {
      if (h.length && h[h.length - 1] === currentPage) return h
      return [...h, currentPage]
    })
  }, [currentPage])

  // ── Derived values ─────────────────────────────────────────────────────────

  const hasGraph = (book?.branching_pages ?? 0) > 0

  // Build the terminal ID set once the graph is loaded — used for
  // reconciliation in useBookProgress and for ending detection below.
  const terminalIds = useMemo((): ReadonlySet<number> | undefined => {
    if (!graph) return undefined
    const ids = new Set<number>()
    for (const n of graph.nodes) {
      if (n.is_terminal || n.choices.length === 0) ids.add(n.id)
    }
    return ids
  }, [graph])

  // ── Progress tracking ──────────────────────────────────────────────────────

  const { foundCount, isNewEnding, recordEnding, clearNewEnding } =
    useBookProgress({
      slug: slug ?? '',
      totalEndings: book?.terminals ?? 0,
      terminalIds,
    })

  // Record an ending the moment the user lands on a terminal node.
  // The effect re-runs when currentNode changes (i.e. page navigation).
  // recordEnding is a no-op for already-discovered endings, so there's no
  // redundant write on revisits.
  useEffect(() => {
    if (!currentNode) return
    if (currentNode.is_terminal || currentNode.choices.length === 0) {
      recordEnding(currentNode.id)
    }
  }, [currentNode, recordEnding])

  // ── Navigation callbacks ───────────────────────────────────────────────────

  const goto = useCallback(
    (target: number) => {
      if (!slug) return
      navigate(`/b/${slug}/read/${target}`)
    },
    [slug, navigate],
  )

  const restart = useCallback(() => {
    if (!graph || !slug) return
    setHistory([])
    if (graph.start_page != null) navigate(`/b/${slug}/read/${graph.start_page}`)
  }, [graph, slug, navigate])

  const back = useCallback(() => {
    if (history.length < 2 || !slug) return
    const prev = history[history.length - 2]
    setHistory((h) => h.slice(0, -2))
    navigate(`/b/${slug}/read/${prev}`)
  }, [history, slug, navigate])

  const goToGraph = useCallback(() => {
    if (slug) navigate(`/b/${slug}/graph`)
  }, [slug, navigate])

  // ── Keyboard navigation ────────────────────────────────────────────────────

  useKeyboardNav({
    choices: currentNode?.choices ?? [],
    canGoBack: history.length >= 2,
    hasGraph,
    onChoose: goto,
    onBack: back,
    onRestart: restart,
    onGraph: goToGraph,
  })

  // ── Render ─────────────────────────────────────────────────────────────────

  if (error) return <div className="container error">{error}</div>
  if (!book || !graph) return <div className="container loading">Loading…</div>

  return (
    <div className="container reader">
      <BookHeader book={book} active="read" />

      <div className="reader-layout">
        <article className="reader-main">
          <header className="reader-page-head">
            <span className="muted">Page</span>
            <h2>{currentPage ?? '—'}</h2>
            {currentNode?.is_terminal && (
              <span className="badge badge-end">THE END</span>
            )}
          </header>

          <div className="reader-body">
            {loadingPage ? (
              <p className="muted">Loading page…</p>
            ) : !currentNode ? (
              <p className="muted">
                This page wasn't extracted. It may have been a blank or
                illustration-only page.
              </p>
            ) : (
              <pre className="page-text">{pageText}</pre>
            )}
          </div>

          {currentNode && currentNode.choices.length > 0 ? (
            <ChoiceList node={currentNode} onChoose={goto} />
          ) : currentNode ? (
            <div className="reader-end">
              <p>This path ends here.</p>
              <button className="btn" onClick={restart}>
                Start over
              </button>
            </div>
          ) : null}

          <div className="reader-controls">
            <button
              className="btn btn-ghost"
              onClick={back}
              disabled={history.length < 2}
            >
              ← Back
            </button>
            <button className="btn btn-ghost" onClick={restart}>
              Restart
            </button>
            {hasGraph && (
              <Link to={`/b/${slug}/graph`} className="btn btn-ghost">
                See graph
              </Link>
            )}
            <KeyboardShortcuts hasGraph={hasGraph} />
          </div>
        </article>

        <aside className="reader-side">
          <h3>Path so far</h3>
          {history.length === 0 ? (
            <p className="muted">No pages visited yet.</p>
          ) : (
            <ol className="path-list">
              {history.map((p, i) => (
                <li key={`${p}-${i}`}>
                  <Link to={`/b/${slug}/read/${p}`}>Page {p}</Link>
                </li>
              ))}
            </ol>
          )}

          {book.terminals > 0 && (
            <div className="reader-side-progress">
              <span className="reader-side-progress-label muted">
                Endings found
              </span>
              <span className="reader-side-progress-count">
                {foundCount} / {book.terminals}
              </span>
            </div>
          )}
        </aside>
      </div>

      <EndingToast
        show={isNewEnding}
        foundCount={foundCount}
        totalEndings={book.terminals}
        onDismiss={clearNewEnding}
      />
    </div>
  )
}

function ChoiceList({
  node,
  onChoose,
}: {
  node: Node
  onChoose: (target: number) => void
}) {
  return (
    <div className="choice-list">
      {node.choices.map((c, i) => (
        <ChoiceButton
          key={`${c.target}-${i}`}
          choice={c}
          index={i}
          onChoose={onChoose}
        />
      ))}
    </div>
  )
}

function ChoiceButton({
  choice,
  index,
  onChoose,
}: {
  choice: Choice
  index: number
  onChoose: (target: number) => void
}) {
  const shortcutKey = index < 9 ? index + 1 : null

  return (
    <button
      className="choice"
      onClick={() => onChoose(choice.target)}
    >
      {shortcutKey != null && (
        <span className="choice-num" aria-hidden="true">
          {shortcutKey}
        </span>
      )}
      <div className="choice-prompt">
        {choice.prompt && choice.prompt !== '(continues)' ? (
          <>{choice.prompt}…</>
        ) : (
          <em className="muted">Continue</em>
        )}
      </div>
      <div className="choice-arrow">→ Page {choice.target}</div>
    </button>
  )
}
