# HuskyAdvisor Data Coverage Audit

## Purpose

This document summarizes what the current HuskyAdvisor dataset covers well, what is only partially covered, and what is still missing. It is meant to keep the team realistic about MVP quality and to guide future work.

## Current Strengths

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

Applied Computing is present, but not yet as rich as CSSE.

Current strengths:
- database-related paths
- web/software development
- cloud-aligned recommendations

Current limitation:
- fewer distinct Applied Computing-specific pathways are represented
- some recommendations still rely on broadly shared CSS courses rather than more specialized program nuance

### EE Coverage

EE is represented, but still thinner than it should be for a strong major-comparison experience.

Current strengths:
- embedded systems direction
- hardware/software systems language

Current limitation:
- fewer EE-specific records than CSSE
- less depth in circuits, signals, and broader hardware pathways
- current recommendations may over-weight cross-listed or systems-adjacent CSS courses

## Current Gaps

### Data Gaps

- more Applied Computing course variety
- more EE-specific upper-division records
- more official source links across the dataset
- more precise prerequisites for several records
- more structured quarter-plan examples

### Recommendation Gaps

- recommendations are still stronger for systems/software paths than for analytics or broader EE paths
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

It does **not** yet support a claim that HuskyAdvisor is:
- a complete UWB advising system
- a real-time internship recommender
- equally deep across every major pathway

## Recommended Next Data Priorities

1. Add 5 to 8 more Applied Computing and EE records
2. Add source URLs to more high-priority courses
3. Tighten prerequisite text for frequently recommended electives
4. Add 2 to 3 quarter-plan examples in structured form
5. Verify that website content uses the same language as the data and recommendation engine
