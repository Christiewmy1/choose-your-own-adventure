# HuskyAdvisor Technical Design Document

## 1. Executive Summary

HuskyAdvisor is a domain-specific academic and career advising assistant for University of Washington Bothell students. Its core value comes from combining UWB-focused academic data, local career signals, and student personalization into a single Retrieval-Augmented Generation workflow. Instead of acting like a generic chatbot, HuskyAdvisor narrows its responses to the realities of UWB programs, regional employers, and the student's current academic position.

This project is intentionally scoped as a strong final-project MVP. The initial version focuses on major guidance, elective recommendations, local company alignment, and quarter-by-quarter planning. A later version can expand to richer sentiment analysis, automated data refresh, and campus-specific advising dashboards.

## 2. Problem Statement and Users

UWB students often piece together advice from scattered sources:

- university web pages
- PDF degree sheets
- course descriptions
- job postings
- career fairs
- informal professor reviews

That makes planning slow and inconsistent. HuskyAdvisor centralizes these sources into a personalized advisor that answers questions with traceable, local context.

Primary users:

- current UWB STEM students
- transfer students choosing between majors
- juniors and seniors planning internships
- students seeking professor or course fit guidance

## 3. Scope

### MVP Features

- Major recommendation between CSSE, Applied Computing, and EE
- 400-level elective suggestions based on target careers
- Local tech company matching for Bothell-area opportunities
- Quarter-by-quarter roadmap generation
- Metadata-aware retrieval over curated UWB documents

### Stretch Features

- Professor style matching using review-derived sentiment tags
- Automated web/PDF ingestion pipelines
- Career timeline alerts for internship windows
- Dashboard UI with saved profiles

## 4. System Architecture

### Textual Architecture Diagram

`User Query -> User Profile Enrichment -> Query Embedding -> Vector Search + Metadata Filtering -> Retrieved UWB Context -> LLM Reasoning and Synthesis -> HuskyAdvisor Response`

### Component Flow

1. The student submits a question.
2. The application loads the student's profile.
3. The query is enriched with profile details such as major, standing, completed courses, and career goals.
4. LangChain sends the query to a metadata-aware retriever.
5. Chroma returns UWB-relevant chunks such as electives, company descriptions, and degree guidance.
6. The LLM synthesizes a response grounded in retrieved evidence.
7. The final answer includes recommendations plus rationale tied to UWB context.

### Main Components

- `Profile Layer`: student preferences and academic state
- `Ingestion Layer`: PDFs, web pages, manually curated seed data
- `Chunking + Embeddings Layer`: converts documents into searchable vectors
- `Vector Store`: Chroma for local development
- `Retriever Layer`: SelfQueryRetriever or equivalent metadata-aware retriever
- `Reasoning Layer`: LLM prompt template with personalization
- `Response Layer`: formatted advising answer

## 5. Data Ingestion Strategy

| Source | Use | Method | Refresh | Trust | Notes |
|---|---|---|---|---|---|
| `uwb.edu` academic pages | official program and course context | HTML scraping/API/manual curation | monthly | high | best source for degree descriptions |
| departmental PDF degree sheets | requirements and planning | PDF parsing + manual verification | each quarter | high | PDF tables may parse poorly |
| course catalog pages | prerequisites and electives | HTML scraping/manual export | each quarter | high | stable, structured content |
| career fair and internship pages | local employer signals | HTML scraping/manual curation | monthly during hiring seasons | medium-high | may require cleanup |
| Handshake or similar | internship windows and skills | manual export if permitted | weekly in season | medium | may have access restrictions |
| professor review sources | teaching-style features | manual seed data or approved ingestion | infrequent | low-medium | use cautiously and label clearly |

### Ingestion Recommendation

For the class project, use a hybrid strategy:

- manually curate an initial seed dataset
- ingest a limited number of official UWB pages and PDFs
- treat opinion data as optional enrichment, not ground truth

## 6. Personalization Logic

Each answer should be filtered or re-ranked using a student profile.

### Required Profile Fields

```json
{
  "student_id": "uwb-001",
  "name": "Sample Student",
  "campus": "UW Bothell",
  "major": "CSSE",
  "class_standing": "Junior",
  "gpa": 3.42,
  "completed_credits": 105,
  "completed_courses": ["CSS 342", "CSS 360", "CSS 370"],
  "preferred_learning_style": "structured, project-based",
  "career_goals": ["software engineering", "aerospace systems"],
  "target_companies": ["Boeing"],
  "internship_timeline": "next summer"
}
```

### Profile Use Cases

- suppress courses whose prerequisites are unmet
- prioritize electives aligned with aerospace, systems, embedded, or large-scale engineering
- tailor project suggestions to the student's current quarter and skill maturity
- adjust professor suggestions to preferred workload and teaching style

## 7. Database Schema

### SQL-Oriented Schema

```sql
CREATE TABLE students (
  student_id TEXT PRIMARY KEY,
  name TEXT,
  campus TEXT,
  major TEXT,
  class_standing TEXT,
  gpa REAL,
  completed_credits INTEGER,
  preferred_learning_style TEXT,
  internship_timeline TEXT
);

CREATE TABLE student_goals (
  student_id TEXT,
  goal TEXT,
  FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE student_completed_courses (
  student_id TEXT,
  course_code TEXT,
  FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE courses (
  course_code TEXT PRIMARY KEY,
  title TEXT,
  level INTEGER,
  department TEXT,
  description TEXT,
  major_tags TEXT,
  career_tags TEXT,
  prerequisite_text TEXT,
  project_emphasis TEXT
);

CREATE TABLE professors (
  professor_id TEXT PRIMARY KEY,
  name TEXT,
  department TEXT,
  teaching_style_tags TEXT,
  sentiment_summary TEXT,
  source_confidence TEXT
);

CREATE TABLE local_tech_companies (
  company_id TEXT PRIMARY KEY,
  name TEXT,
  city TEXT,
  domain_focus TEXT,
  hiring_seasons TEXT,
  target_skills TEXT,
  notes TEXT
);

CREATE TABLE documents (
  doc_id TEXT PRIMARY KEY,
  source_type TEXT,
  source_url TEXT,
  title TEXT,
  content TEXT,
  trust_level TEXT,
  last_updated TEXT
);
```

### JSON Example For Courses

```json
{
  "course_code": "CSS 430",
  "title": "Operating Systems",
  "level": 400,
  "department": "CSS",
  "description": "Covers processes, memory, concurrency, and systems topics.",
  "major_tags": ["CSSE"],
  "career_tags": ["systems", "embedded", "aerospace", "backend"],
  "prerequisite_text": "CSS 342 and CSS 360",
  "project_emphasis": "medium-high"
}
```

## 8. RAG Pipeline Design

### Retrieval Objects

Store chunked documents with metadata such as:

- `entity_type`: course, professor, company, degree_sheet
- `major_tags`
- `career_tags`
- `course_level`
- `city`
- `source_type`
- `trust_level`

### Retrieval Strategy

1. Convert course/company/professor records into LangChain `Document` objects.
2. Embed records with an OpenAI embedding model.
3. Store vectors in Chroma.
4. Use `SelfQueryRetriever` so natural-language questions can become metadata filters.
5. Feed retrieved context plus student profile into the answer prompt.

### Why SelfQueryRetriever

It is a strong fit because the user asks questions like:

- "400-level electives"
- "for Boeing"
- "I am a junior CSSE student"

Those constraints map naturally to structured metadata such as course level, major tags, and career tags.

## 9. Professor Matching and Sentiment Strategy

This feature has the most risk and should be treated as optional in the MVP.

### Recommendation

- Use official instructor/course data as the base layer.
- Add opinion-based features only as tagged, low-confidence enrichment.
- Summarize sentiment into coarse descriptors such as:
  - lecture-heavy
  - project-heavy
  - approachable
  - fast-paced
  - tough grader

### Ethics

- clearly disclose that review data is subjective
- do not rank professors as universally good or bad
- avoid harmful or overly personal inferences
- prefer teaching-style matching over popularity ranking

## 10. Prototype Implementation Plan

### Phase 1: MVP Foundation

- Create sample data for courses, companies, and professors
- Build Python schemas and profile model
- Load records into Chroma
- Implement query answering with LangChain

### Phase 2: Better Grounding

- Add official UWB pages and degree-sheet PDFs
- Improve metadata tagging and chunk quality
- Add citation-style source reporting

### Phase 3: Personalization and Planning

- Generate quarter-by-quarter roadmaps
- Add prerequisite validation
- Add company-to-skill-to-course mapping

### Phase 4: Stretch Enhancements

- Add professor preference matching
- add web UI
- automate data refresh

## 11. Risks and Limitations

- live data sources may change or block scraping
- Handshake data may not be directly accessible
- professor reviews are subjective and may be biased
- sample data may oversimplify UWB offerings
- LLM responses can still hallucinate without strong retrieval grounding

## 12. Boilerplate Prototype Design

The prototype should:

- define sample UWB-flavored records
- create `Document` objects with metadata
- build a local Chroma vector store
- use `SelfQueryRetriever`
- answer a Boeing-oriented elective question

### Expected Query

`I'm a Junior CSSE student at UWB; which 400-level electives should I take if I want to work at Boeing?`

### Expected Answer Shape

The answer should mention likely systems-oriented or aerospace-relevant electives, explain why each one helps, and tie the recommendation back to Boeing-style engineering environments.

## 13. Suggested Final-Project Positioning

For presentation, describe HuskyAdvisor as:

"A UWB-specific advising AI that combines local academic knowledge, regional employer mapping, and student personalization to make course and career planning more actionable."
