# HuskyAdvisor

HuskyAdvisor is a specialized AI assistant for the University of Washington Bothell community. It uses Retrieval-Augmented Generation (RAG) to answer hyper-local academic, career, and course-planning questions using UWB-specific data.

This starter project includes:

- An improved project prompt
- A technical design document
- A project website content draft
- A data and metadata plan
- A Python prototype architecture
- A local advising engine for offline/demo-friendly use
- A LangChain + Chroma starter script for the RAG path
- Sample UWB-flavored data for local testing

## Project Structure

- `docs/improved_prompt.md`: upgraded version of the original Gemini prompt
- `docs/technical_design_document.md`: system design, schemas, and implementation plan
- `docs/project_website_content.md`: draft copy for the public-facing project website
- `docs/data_and_metadata_plan.md`: dataset scope, metadata rules, and next data tasks
- `docs/catalog_integration_notes.md`: notes on integrating an external UWB course catalog source
- `docs/evaluation_question_bank.md`: test prompts and expected-answer notes for HuskyAdvisor
- `docs/matiyas_weekly_contribution_log.md`: example contribution log for the data/documentation role
- `docs/system_overview.md`: execution flow and file-level architecture overview
- `data/`: JSON profile and sample UWB course data
- `data/company_course_mapping.json`: explicit company-to-course recommendations
- `data/internship_prep_playbooks.json`: internship-prep guidance tracks
- `data/local_tech_companies.json`: seed dataset for local company alignment
- `requirements.txt`: Python dependencies
- `src/huskyadvisor/models.py`: profile and metadata schemas
- `src/huskyadvisor/json_data.py`: loader for JSON student/course records
- `src/huskyadvisor/sample_data.py`: sample courses, professors, and companies
- `src/huskyadvisor/advisor.py`: local recommendation engine for electives, majors, and roadmaps
- `src/huskyadvisor/formatter.py`: response formatting helpers
- `src/huskyadvisor/vector_store.py`: document loading and Chroma setup
- `src/huskyadvisor/retrieval.py`: retriever construction
- `src/huskyadvisor/main.py`: prototype entrypoint
- `scripts/ingest_local_data.py`: optional local JSON-to-Chroma ingestion script

## Quick Start

1. Create a virtual environment and install dependencies if you want the full LangChain RAG demo.
2. Add your OpenAI API key to the environment for the `llm-demo` mode:

```bash
export OPENAI_API_KEY="your-key-here"
```

3. Run the prototype:

```bash
PYTHONPATH=src python3 -m huskyadvisor.main
```

4. Try other modes:

```bash
PYTHONPATH=src python3 -m huskyadvisor.main --mode major
PYTHONPATH=src python3 -m huskyadvisor.main --mode roadmap
PYTHONPATH=src python3 -m huskyadvisor.main --mode profile-demo
PYTHONPATH=src python3 -m huskyadvisor.main --mode company-demo
PYTHONPATH=src python3 -m huskyadvisor.main --mode internship-demo
PYTHONPATH=src python3 -m huskyadvisor.main --mode llm-demo
```

## Example Query

The starter script is wired to answer:

`I'm a Junior CSSE student at UWB; which 400-level electives should I take if I want to work at Boeing?`

## Notes

- The sample data is intentionally lightweight for a class project starter.
- Real deployment should replace the sample dataset with scraped or curated UWB sources.
- RateMyProfessor and course-evaluation data may involve legal, ethical, or privacy constraints, so production ingestion should be reviewed carefully.
- The default CLI modes work without an API call; only `--mode llm-demo` requires an OpenAI API key and installed LangChain dependencies.
- The `profile-demo` mode uses `data/student_profile.json` and `data/uwb_courses_sample.json`, which came from the imported teammate branch and are now integrated into the main project.
- The `company-demo` mode shows the next-step career alignment layer by matching a student profile to a small local company dataset.
- The `internship-demo` mode shows a structured preparation plan that connects likely tracks, courses, skills, and project ideas.

## Data / Documentation Work

If you are presenting the data/documentation contribution area, the strongest files to point to are:

- `data/uwb_courses_sample.json`
- `data/uwb_recent_css_catalog_summary.json`
- `docs/data_and_metadata_plan.md`
- `docs/catalog_integration_notes.md`
- `docs/evaluation_question_bank.md`
- `docs/matiyas_weekly_contribution_log.md`
- `docs/system_overview.md`
- `docs/project_website_content.md`
- `docs/technical_design_document.md`
