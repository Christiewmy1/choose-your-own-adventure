# Deep QA 500+ Scenario Report

## Summary

- Scenario profiles tested: 560
- Passed scenarios: 560
- Failed scenarios: 0
- API contract failures: 0
- Data integrity failures: 0
- Public backend check failures: not run in this local-only report

## Coverage

- Majors covered: CSSE (65), Computer Science and Software Engineering (65), Applied Computing (65), Electrical Engineering (65), Computer Engineering (65), Data Visualization (65), Business Administration (65), Informatics (65), Biology (40)
- Standings covered: Freshman (117), Sophomore (117), Junior (117), Senior (105), Graduate (104)
- Unique target company/field inputs: 37
- Goal tags covered: data (172), cloud (130), backend (87), security (86), embedded (86), analytics (86), software engineering (44), networking (43), infrastructure (43), aerospace (43), systems (43), dashboards (43), business systems (43), digital transformation (43), product (43), healthcare (43), privacy (43), gaming (43), graphics (43), interactive software (43), ai (43), machine learning (43), financial technology (43), retail tech (43), e-commerce (43), streaming media (43), distributed systems (43), automotive software (43), consumer platforms (43), mobile (43)
- Unique recommended course codes observed: 28
- Most common course recommendations: CSS 436 (156), CSS 475 (120), CSS 370 (108), BIS 315 (102), CSS 430 (90), CSS 486 (85), EE 450 (78), BIS 445 (59), CSS 432 (55), CSS 481 (55), CSS 342 (54), STMATH 308 (49)

## Failure Types

- No scenario-level invariant failures.

## API Contract Check

- Passed.

## Data Integrity Check

- Passed.

## Public Backend Check

- Skipped in this deterministic local run. Use `python3 scripts/run_deep_qa.py --scenarios 560 --public` after redeploying the backend.

## First 25 Failed Scenarios

- No failed scenarios.

## Honest Weak Spots

- This stress test validates deterministic engine behavior and API shape; it does not prove official degree accuracy.
- Public endpoint checks depend on current network availability and deployment state.
- Crawl4AI is validated as a data-ingestion/normalization pipeline; crawled facts still require human review before becoming trusted advising data.
