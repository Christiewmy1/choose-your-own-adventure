# Improved Build Prompt For HuskyAdvisor

## Role

You are a Senior Software Architect, Lead AI Engineer, and Product Strategist. Design a realistic, implementation-ready final project for a University of Washington Bothell course: CSS 382 Introduction to AI.

Your task is to produce a **Technical Design Document (TDD)** and a **Python prototype plan** for an AI assistant called **HuskyAdvisor**.

## Product Goal

HuskyAdvisor is a Retrieval-Augmented Generation (RAG) assistant built specifically for the **UW Bothell community**. It should help students make better academic and career decisions by combining UWB-specific documents, local internship signals, and a personalization profile.

The system should feel practical, ethical, and scoped tightly enough for a student final project while still being ambitious.

## Primary User

The primary user is a UWB student asking questions such as:

- "Which major fits me best: CSSE, Applied Computing, or EE?"
- "What 400-level electives should I take if I want to work at Boeing, Amazon, or T-Mobile?"
- "Which professor might fit my learning style?"
- "What should I build each quarter to become internship-ready by next year?"

## Required Features

Design the system around these four capabilities:

1. **Major Selection and Degree Mapping**
   - Compare UWB majors such as CSSE, Applied Computing, and Electrical Engineering.
   - Use course requirements, interests, and student goals to recommend pathways.
   - Explain tradeoffs instead of giving one-word recommendations.

2. **Bothell Tech Pipeline**
   - Track companies relevant to UWB students in the Bothell, Seattle, Bellevue, Kirkland, and Redmond area.
   - Include company focus, likely internship timing, and relevant skills.
   - Connect company targets to recommended courses and projects.

3. **Professor and Course Fit**
   - Support matching based on teaching style, workload preference, and student learning preferences.
   - If sentiment data is used, explain how it is cleaned, scored, and ethically handled.
   - Clearly separate verified university data from opinion-based review data.

4. **Success Roadmaps**
   - Generate quarter-by-quarter academic and project plans.
   - Tie advice to UWB courses and realistic portfolio milestones.
   - Include a sample plan for a CSSE student interested in aerospace or embedded/software work.

## Technical Requirements

Your solution must include:

- **Python** as the implementation language
- **LangChain** for orchestration
- A **vector database** such as ChromaDB or Pinecone
- A **RAG pipeline** over UWB-specific sources
- A **user profile schema** that stores at least:
  - major or intended major
  - class standing
  - GPA
  - completed credits
  - completed courses
  - preferred learning style
  - target industries or companies
  - internship timeline

## Data Sources To Plan For

Propose an ingestion strategy for:

- `uwb.edu` pages
- UWB course catalog pages
- degree sheets or advising PDFs
- career fair pages and internship resources
- Handshake-like career sources, if accessible
- optional professor review data, if legally and ethically appropriate

For each source, specify:

- ingestion method
- data format
- refresh frequency
- trust level
- risks and limitations

## Required Outputs

Produce the following:

1. **Executive Summary**
2. **Problem Statement and Users**
3. **Feature Scope**
4. **System Architecture**
   - Include a textual architecture diagram:
     `User Query -> Profile Enrichment -> Embedding/Search -> Retrieved Context -> LLM Reasoning -> HuskyAdvisor Response`
5. **Data Model**
   - JSON or SQL schema for:
     - `students`
     - `courses`
     - `professors`
     - `local_tech_companies`
     - `documents`
6. **RAG Pipeline Design**
7. **Personalization Logic**
8. **Professor Matching / Sentiment Strategy**
9. **Implementation Plan**
   - phased roadmap
   - MVP vs stretch goals
10. **Risks, Ethics, and Limitations**
11. **Prototype Python Code**
   - Include a LangChain starter that uses a retriever capable of filtering metadata
   - Demonstrate the query:
     `"I'm a Junior CSSE student at UWB; which 400-level electives should I take if I want to work at Boeing?"`

## Project Constraints

- Keep the design achievable for a university final project.
- Prefer open-source, low-cost, and local-first tools where possible.
- Call out any assumptions when real data is unavailable.
- Do not present speculative data as fact.
- If external data cannot be legally scraped, provide a fallback plan using manually curated seed data.

## Output Style

Write clearly and professionally, like a project proposal that could be submitted to an instructor. Balance ambition with feasibility.
