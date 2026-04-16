import { useEffect, useRef } from 'react'
import cytoscape from 'cytoscape'

export default function StoryGraph({ allPages, currentPage, onNodeClick }) {
  const containerRef = useRef(null)
  const cyRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current) return

    const nodes = Object.values(allPages).map(p => ({
      data: {
        id: String(p.id),
        label: String(p.id),
        type: p.id === 2 ? 'start' : p.isTerminal ? 'terminal' : p.isContinuation ? 'continuation' : 'normal'
      }
    }))

    const edges = []
    Object.values(allPages).forEach(p => {
      p.choices.forEach((c, i) => {
        edges.push({
          data: {
            id: `e${p.id}-${c.page}-${i}`,
            source: String(p.id),
            target: String(c.page)
          }
        })
      })
    })

    cyRef.current = cytoscape({
      container: containerRef.current,
      elements: [...nodes, ...edges],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#6b7280',
            'label': 'data(label)',
            'color': '#fff',
            'font-size': '10px',
            'text-valign': 'center',
            'text-halign': 'center',
            'text-margin-y': '-1px',
            'width': '32px',
            'height': '32px',
            'border-width': '2px',
            'border-color': 'transparent',
            'text-outline-width': 0,
            'text-outline-color': '#111827'
          }
        },
        {
          selector: 'node[type="start"]',
          style: { 'background-color': '#16a34a', 'width': '36px', 'height': '36px', 'font-size': '11px', 'font-weight': 'bold' }
        },
        {
          selector: 'node[type="terminal"]',
          style: { 'background-color': '#dc2626' }
        },
        {
          selector: 'node[type="continuation"]',
          style: { 'background-color': '#9333ea' }
        },
        {
          selector: 'node.current',
          style: {
            'border-color': '#facc15',
            'border-width': '3px',
            'background-color': '#f59e0b',
            'width': '38px',
            'height': '38px',
            'font-size': '11px'
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 1.8,
            'line-color': '#7c93b3',
            'target-arrow-color': '#7c93b3',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'arrow-scale': 0.9,
            'opacity': 0.8
          }
        }
      ],
      layout: {
        name: 'breadthfirst',
        directed: true,
        roots: ['2'],
        spacingFactor: 1.2,
        padding: 20
      },
      userZoomingEnabled: true,
      userPanningEnabled: true,
      minZoom: 0.2,
      maxZoom: 3
    })

    cyRef.current.on('tap', 'node', (e) => {
      onNodeClick(Number(e.target.id()))
    })

    return () => { if (cyRef.current) cyRef.current.destroy() }
  }, [allPages])

  // Highlight current page
  useEffect(() => {
    if (!cyRef.current) return
    cyRef.current.nodes().removeClass('current')
    cyRef.current.$(`#${currentPage}`).addClass('current')
    // Pan to current node
    const node = cyRef.current.$(`#${currentPage}`)
    if (node.length) cyRef.current.animate({ center: { eles: node }, zoom: 1.2 }, { duration: 400 })
  }, [currentPage])

  return (
    <div className="graph-container">
      <div className="graph-legend">
        <span className="legend-item"><span className="dot dot-start" />Start</span>
        <span className="legend-item"><span className="dot dot-normal" />Page</span>
        <span className="legend-item"><span className="dot dot-continuation" />Continuation</span>
        <span className="legend-item"><span className="dot dot-terminal" />Ending</span>
        <span className="legend-item"><span className="dot dot-current" />You are here</span>
      </div>
      <div ref={containerRef} className="graph-canvas" />
    </div>
  )
}