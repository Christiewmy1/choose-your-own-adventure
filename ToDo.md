# ToDo.md

_Task list for forking and extending choose-your-own-adventure_
_Owner: Christie — April 2026_

---

## Phase 1 — Setup & Data ✅ / 🔲

- [ ] Fork the repo from Christiewmy1/choose-your-own-adventure on GitHub
- [ ] Clone locally and confirm existing scripts run (Python 3 required)
- [ ] Write a Python script (or extend existing ones) to export `story-data.json`
      - Parse all `output/cot-pages-ocr-v2/*.txt` files
      - Extract page text and choices ("turn to page X")
      - Identify terminal pages (no outgoing choices)
      - Output: `web/src/data/story-data.json`
- [ ] Create the `/web` folder and scaffold a React + Vite app
      ```
      cd web && npm create vite@latest . -- --template react
      ```
- [ ] Install dependencies: `cytoscape`, `react-cytoscapejs` (or just cytoscape), `tailwindcss`
- [ ] Commit initial scaffold to GitHub

---

## Phase 2 — Reader Mode 🔲

- [ ] Build `StoryPage` component
      - Displays page number + text
      - Renders choice buttons at the bottom
      - "THE END" screen for terminal pages
- [ ] Build `useStory` hook (or context)
      - Loads `story-data.json`
      - Tracks current page
      - Tracks history (path taken so far)
      - `goToPage(n)` function
      - `goBack()` function
- [ ] Build `HistoryTrail` component — shows breadcrumb path (e.g. 2 → 3 → 5 → 16)
- [ ] Build `App` layout — navigation bar + reader panel
- [ ] Test full read-through of at least 3 different story paths
- [ ] Deploy to GitHub Pages (basic working version)
      ```
      npm install gh-pages --save-dev
      npm run deploy
      ```
- [ ] Confirm live URL works: https://Christiewmy1.github.io/choose-your-own-adventure/

---

## Phase 3 — Graph Visualization 🔲

- [ ] Build `StoryGraph` component using Cytoscape.js
      - Load all nodes + edges from `story-data.json`
      - Color terminal pages red
      - Color start page green
      - Color main trunk nodes blue
      - Gray for all others
- [ ] Wire up: clicking a node in the graph navigates reader to that page
- [ ] Highlight current page in graph as reader moves through story
- [ ] Add zoom/pan controls
- [ ] Add toggle button: show/hide graph panel

---

## Phase 4 — Author Mode 🔲

- [ ] Add mode toggle: "Read" vs "Author" in the nav bar
- [ ] In Author mode, make page text editable (textarea instead of paragraph)
- [ ] Build `AddChoice` UI — input for choice text + destination page number
- [ ] Build `AddPage` UI — create a new blank page
- [ ] Save edits to localStorage so they persist between sessions
- [ ] Build `ExportJSON` button — download current story state as JSON
- [ ] Show orphan pages (no incoming edges) highlighted in yellow on graph
- [ ] Show "unfinished" pages (text exists but no choices added yet) in orange

---

## Phase 5 — Polish & Documentation 🔲

- [ ] Make the UI mobile-friendly (stack panels vertically on small screens)
- [ ] Fix any obvious OCR errors in the story text (at least pages 2–20)
- [ ] Write final `README.md` including:
      - [ ] Live site URL
      - [ ] GitHub repo URL
      - [ ] Team member names
      - [ ] How to run locally
      - [ ] How to regenerate story data from scratch
- [ ] Update `Codebase.md` to reflect the new web app architecture
- [ ] Final commit and push — verify all team members have commits on `main`

---

## Stretch Goals (only if phases 1–5 are done) 🔲

- [ ] AI story continuation button (calls Claude API to generate a new page)
- [ ] Dark mode toggle
- [ ] Animated page transitions
- [ ] Page search — find a page by keyword in its text
- [ ] "Random adventure" button — auto-plays through a random path

---

## Questions / Blockers

- [ ] Decide: Python script vs JS script to generate story-data.json?
- [ ] Decide: Cytoscape.js vs D3 for graph?
- [ ] Decide: GitHub Pages vs Vercel for deployment?
- [ ] Check: does the existing `render_story_graph_svg.py` output work in the browser or do we need to redo it in JS?

---

## Assignments (if working in a team)

| Task | Owner |
|------|-------|
| story-data.json parser | TBD |
| Reader Mode components | TBD |
| Graph visualization | TBD |
| Author Mode UI | TBD |
| Deployment + README | TBD |
