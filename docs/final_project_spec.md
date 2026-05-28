# HuskyAdvisor Final Project Specification

## Project purpose

HuskyAdvisor helps University of Washington Bothell students make better academic and career-planning decisions by connecting:

- major selection
- course planning
- company alignment
- internship preparation
- quarter-by-quarter roadmap guidance

The project benefits the UW community by reducing the friction of piecing together advice from scattered catalog pages, degree information, employer research, and informal recommendations.

## Problem being solved

Students often have to answer questions like:

- Which major fits my interests best?
- Which upper-division classes actually move me toward my career goals?
- Which local employers align with those classes?
- What should I do next to become internship-ready?

HuskyAdvisor centralizes those decisions into one web-based system grounded in UW Bothell-specific data.

## Main user groups

- current UWB computing and engineering students
- transfer students comparing related pathways
- students preparing for internships
- students who want clearer connections between classes and employer goals

## Current MVP features

- major guidance across 6 supported pathways
- course recommendation engine
- company-aware recommendation matching
- internship-prep recommendation flow
- quarter-plan / roadmap guidance
- public website plus deployed API architecture

## Supported major pathways

- CSSE
- Applied Computing
- EE
- Computer Engineering
- Data Visualization
- technology-facing Business Administration

## Current technical architecture

Frontend:

- React
- TypeScript
- Vite
- GitHub Pages deployment

Backend:

- FastAPI
- Pydantic
- Vercel deployment target

Recommendation/data layer:

- Python
- JSON datasets
- profile-aware recommendation scoring
- optional LangChain + Chroma + OpenAI retrieval modules

## AI integration summary

HuskyAdvisor uses AI meaningfully through recommendation logic, optional LLM summarization, Crawl4AI ingestion, and optional retrieval:

1. Student profile features shape ranking and filtering.
2. The engine suppresses redundant recommendations and scores pathways by goal alignment.
3. Company intent mappings connect employer domains to class and roadmap suggestions.
4. Groq/Llama 3.3 can rewrite structured results into personalized summaries when `GROQ_API_KEY` is configured.
5. Crawl4AI gathers public UWB/employer source pages into raw and normalized data areas before human validation.
6. Optional retrieval modules support a RAG-style extension beyond the rules/scoring path.

## Public-facing deliverables

- website: `https://christiewmy1.github.io/choose-your-own-adventure/`
- API target: `https://choose-your-own-adventure-bay.vercel.app`
- repository: current project repository with instructor access

## Known current limitations

- not an official advisor-approved planning system
- strongest in UWB computing/engineering pathways
- retrieval/LLM path is present but not the primary deployed flow
- some newer pathways still have thinner metadata than CSSE
- scraped data must still be validated before it becomes trusted advising data
