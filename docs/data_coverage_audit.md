# HuskyAdvisor Data Coverage Audit

## Purpose

This document summarizes what the current HuskyAdvisor dataset covers well, what is only partially covered, and what is still missing. It is meant to keep the team realistic about MVP quality and to guide future work.

## Current Strengths

### Scale

The main course dataset now contains more than 100 course records, combining:
- a smaller curated advising-focused subset
- a larger catalog/schedule-derived CSS expansion layer

This is a major improvement over the earlier small seed dataset because the project now has enough breadth to feel more like a real academic planning system.

### CSSE Coverage

The dataset is currently strongest for CSSE-oriented recommendations.

Well-covered themes:
- software engineering
- operating systems
- networking and distributed systems
- testing and quality assurance
- AI and cloud-related electives

Representative examples:
- `CSS 360`
- `CSS 430`
- `CSS 432`
- `CSS 436`
- `CSS 458`

### Career Alignment Coverage

The current project has enough data to support believable alignment for:
- Boeing
- Microsoft
- Amazon
- T-Mobile
- Google

These companies have matching:
- target skills
- domain notes
- company-to-course relationships
- internship-prep pathways

### Demo Readiness

The current data is good enough for:
- course recommendation demos
- company alignment demos
- internship-prep demos
- persona-based testing

## Partial Coverage

### Applied Computing

Applied Computing is now one of the stronger supported majors.

Current strengths:
- database-related paths
- web/software development
- cloud-aligned recommendations
- BIS-backed business systems and analytics pathways

Current limitation:
- fewer distinct Applied Computing-specific pathways are represented
- some recommendations still rely on broadly shared CSS courses rather than more specialized program nuance

### EE Coverage

EE is now much stronger than earlier versions of the project and has a more believable engineering progression.

Current strengths:
- embedded systems direction
- hardware/software systems language
- stronger major-specific course grouping
- official-curriculum-derived foundation records like `B EE 215`, `B EE 233`, `B EE 235`, and `B EE 425`

Current limitation:
- still fewer EE-specific records than CSSE
- some advanced EE subfields are still not represented
- current recommendations can still lean on shared systems courses when goals are broad

### New Supported Pathways

The project now explicitly supports additional UWB pathways that fit HuskyAdvisor's computing/career mission:

- `Computer Engineering`
- `Data Visualization`
- `Business Administration` (technology-facing MIS / analytics / innovation side only)

These are supported through organized major-to-course mappings built from official UWB major descriptions plus shared CSS, BIS, math, and EE records already in the project dataset.

Current strengths:
- the recommendation engine can now recognize these majors as valid supported inputs
- shared courses are organized more honestly instead of being hidden inside generic CSS-only logic
- the recommendation flow can distinguish between hybrid engineering, analytics, and business-technology pathways more clearly
- Data Visualization and Business Administration now have explicit course tags in the main dataset instead of relying only on inferred mappings

Current limitation:
- support is still narrower for Data Visualization and Business Administration than for CSSE because the project does not yet contain a wide IAS or full business catalog
- Computer Engineering is still modeled as a hybrid of EE and CSS rather than a fully separate CompE curriculum file

## Current Gaps

### Data Gaps

- many of the newly added CSS records still use placeholder metadata and need refinement over time
- more EE-specific upper-division records
- more Data Visualization-specific IAS course records
- more Business Administration tech-track course records
- more official source links across the dataset
- more precise prerequisites for several records
- more structured quarter-plan examples

### Recommendation Gaps

- recommendations are now much closer in quality across the supported majors, but systems/software paths are still slightly stronger than analytics or business-tech paths
- company alignment is believable, but not yet tied to live opportunity data
- the project can suggest preparation pathways, but not real current internship postings

### Website Gaps

- the website scaffold is not yet aligned to the actual HuskyAdvisor data/content
- placeholder or generic examples still need to be replaced with project-specific ones
- the frontend needs to use the persona and copy docs already prepared

## MVP Quality Assessment

If the team presents the project honestly, the current dataset supports a strong MVP story for:
- UWB course recommendations
- local company alignment
- internship-preparation planning
- broad CSS catalog awareness with a much larger record count

It does **not** yet support a claim that HuskyAdvisor is:
- a complete UWB advising system
- a real-time internship recommender
- equally deep across every newly supported major pathway

## Recommended Next Data Priorities

1. Add more IAS and business-tech course records with stronger metadata
2. Add source URLs to more high-priority courses
3. Tighten prerequisite text for frequently recommended electives
4. Add 2 to 3 quarter-plan examples in structured form
5. Verify that website content uses the same language as the data and recommendation engine
