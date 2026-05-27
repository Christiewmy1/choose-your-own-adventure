# AI Integration Strategy

## Why HuskyAdvisor is not “just a chat on the side”

HuskyAdvisor does not attach a chatbot to an otherwise normal website. The recommendation behavior itself is the AI-like core of the project.

The system uses:

- profile-based ranking
- recommendation filtering
- company-intent inference
- major-pathway comparison
- internship-playbook matching
- roadmap-track selection
- Crawl4AI-backed source ingestion for future retrieval and dataset refresh

Those are embedded into the main application logic and directly control the user-facing outputs.

## Current primary AI technique

The current deployed MVP uses a recommendation-engine approach.

### Inputs

- major
- class standing
- completed courses
- career goals
- target companies or target field

### Intelligent behavior

- suppresses courses already completed
- weights recommendations by major fit
- weights recommendations by career-tag overlap
- uses company-course mappings for employer alignment
- uses company-intent profiles to infer employer domain needs
- selects internship-prep tracks by goal, company, and major fit
- selects roadmap templates by pathway relevance

### Why this qualifies as meaningful AI

It is not a static lookup table. The system combines multiple student and dataset features to generate different outputs for different students. That makes the “intelligence” part central to the actual product behavior rather than a side feature.

## Secondary AI / RAG path

The repository also includes a stronger retrieval-oriented extension:

- `src/huskyadvisor/vector_store.py`
- `src/huskyadvisor/retrieval.py`

That path supports:

- document embeddings
- metadata-aware retrieval
- LangChain orchestration
- OpenAI-assisted synthesis

This path is included to show how HuskyAdvisor can evolve from a structured recommendation engine into a richer RAG advising assistant.

The project now also includes a Crawl4AI ingestion layer:

- `scripts/crawl_with_crawl4ai.py`
- `scripts/normalize_crawl4ai_exports.py`
- `src/huskyadvisor/crawl4ai_pipeline.py`

That layer helps HuskyAdvisor gather public UWB and employer content as markdown, normalize it, and prepare it for retrieval or manual dataset refresh. It strengthens the AI/data story by making the retrieval side more realistic and less dependent on one-time hand-written seed data.

## Honest implementation note

The current deployed MVP relies primarily on the structured recommendation engine because it is more stable and easier to demo reliably. The retrieval path is part of the technical direction and repository, but not the default production flow.

## Bottom-line defense

If asked how AI is embedded, the best answer is:

“AI is embedded through the recommendation engine itself. Student profile features, company-intent inference, roadmap selection, and recommendation ranking are part of the core application logic, and the repo also includes a retrieval-based extension for a stronger RAG path.” 
