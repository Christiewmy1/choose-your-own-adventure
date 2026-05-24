# HuskyAdvisor Project Website Content

## Hero Section

**Title:** HuskyAdvisor  
**Tagline:** AI-powered academic and career guidance for UW Bothell students

**Short description:**  
HuskyAdvisor helps UW Bothell students choose majors, compare electives, and connect courses to career goals using a personalized AI advising workflow grounded in UWB-specific data.

**Primary call to action:**  
Try the demo

**Secondary call to action:**  
View the technical design

## Problem Section

UW Bothell students often have to piece together advice from course catalog pages, degree requirement PDFs, advising websites, and word of mouth. That makes academic planning slow, confusing, and hard to personalize. HuskyAdvisor was created to bring those pieces together into one student-friendly tool.

## Why It Matters

- Students need clearer guidance on how majors differ in practice.
- Elective choices can strongly affect internship readiness.
- Local employers value different skill sets, but students do not always see how courses connect to those jobs.
- Advising information exists, but it is scattered across too many places.

## What HuskyAdvisor Does

- Recommends courses based on a student's major, standing, and career goals
- Compares majors such as CSSE, Applied Computing, and EE
- Suggests quarter-by-quarter next steps
- Connects academic choices to local career targets like Boeing and other regional employers

## How The AI Works

HuskyAdvisor is not just a chatbot. Its AI is part of the actual recommendation logic.

1. A student enters a question and profile information.
2. The system loads UW Bothell-specific course and advising data.
3. The retrieval and recommendation layers filter records based on academic status and career goals.
4. The AI returns a more personalized answer with reasoning.

**Architecture summary:**  
`Student Query -> Profile Context -> UWB Data Retrieval -> Recommendation Logic -> HuskyAdvisor Response`

## Data Section

The current MVP uses a curated Spring 2026 dataset that includes:

- sample UWB course records
- major-aligned metadata
- prerequisite fields
- career tags
- student profile inputs

The long-term goal is to replace more of the seed data with verified university sources and refreshable pipelines.

## Demo Section

**Example question:**  
"I'm a junior CSSE student at UW Bothell and I want to work at Boeing. Which 400-level electives should I take?"

**Example output:**  
HuskyAdvisor recommends systems, testing, and embedded-related courses, then explains why those courses match the student's goals.

## Team Section

- **Matiyas Dawit:** Data and documentation lead
- **Christie Yiu:** Frontend and UX lead
- **Sio Hang Yiu:** AI and backend lead

## Technical Stack

- Frontend: Next.js or React
- Backend: Python + FastAPI
- AI orchestration: LangChain
- Vector store: ChromaDB
- Structured data: JSON seed datasets

## User Guide

1. Enter student details such as major, class standing, completed courses, and career target.
2. Ask a question about courses, majors, or planning.
3. Review the recommendations and explanation.
4. Use the output as planning support, not as official degree approval.

## Footer Links

- GitHub repository
- Live demo
- Technical design document
- Course project information
