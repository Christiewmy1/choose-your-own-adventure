# HuskyAdvisor Simulation Coverage Report

## Coverage Summary

- Total simulated student cases: 58
- Majors covered: CSSE (11), Applied Computing (11), Electrical Engineering (9), Computer Engineering (7), Data Visualization (11), Business Administration (9)
- Standings covered: Freshman (13), Sophomore (9), Junior (16), Senior (9), Graduate (11)
- Recommendation quality counts: Strong=58

## Course Areas Exercised

- Unique recommended course codes observed: 26
- Most frequent recommendations: CSS 436 (17), EE 450 (15), CSS 427 (13), CSS 481 (12), CSS 475 (12), CSS 430 (11), CSS 370 (10), BIS 315 (9), BIS 445 (7), CSS 486 (6)

## Patterns That Looked Good

- Completed-course filtering held up across messy text inputs and structured inputs.
- Freshman and sophomore profiles were no longer treated exactly like late-stage students.
- Placeholder catalog entries were less likely to outrank curated, richer courses.
- Roadmaps stopped repeating courses already marked as completed.
- Newer supported majors now produced visibly different recommendation patterns instead of collapsing into the same CSSE-heavy output.

## Patterns Still Looking Weak

- No major quality flags were raised in the current simulation run.

## Recommendation

- Next improvement should focus on adding more IAS and business-tech course records so Data Visualization and Business Administration can rely less on shared CSS courses.
