# HuskyAdvisor Multi-Quarter Schedule Notes

## Purpose

This document explains the new multi-quarter official schedule dataset added for HuskyAdvisor.

## What Was Added

A broader schedule file was added:

- `data/uwb_2026_multi_quarter_schedule_snapshot.json`

It expands HuskyAdvisor beyond a single Spring 2026 snapshot by combining selected public schedule offerings from:

- Winter 2026
- Spring 2026
- Summer 2026
- Autumn 2026

## Why This Is Better Than A Single-Term Snapshot

A one-term snapshot is useful, but it can make the project look too narrow. A multi-quarter schedule view lets HuskyAdvisor support stronger planning ideas like:

- which courses show up repeatedly across quarters
- whether a course is usually daytime, evening, hybrid, or summer-intensive
- whether a course looks seasonal or recurring
- how students might plan several quarters ahead instead of only one

## What This Enables

This dataset makes it easier for future HuskyAdvisor versions to:

- prefer courses with recurring availability
- help students think beyond one quarter
- compare schedule patterns for major planning
- make roadmap suggestions more realistic

## Official Public Sources Used

- `https://www.washington.edu/students/timeschd/pub/B/WIN2026/css.html`
- `https://www.washington.edu/students/timeschd/pub/B/SPR2026/css.html`
- `https://www.washington.edu/students/timeschd/pub/B/SUM2026/css.html`
- `https://www.washington.edu/students/timeschd/pub/B/AUT2026/css.html`
- `https://www.washington.edu/students/timeschd/pub/B/SPR2026/bengr.html`

## Best Next Step

The next strong improvement is to make the recommendation engine aware of both:

- relevance to student goals
- recurring quarter availability

That would let HuskyAdvisor recommend courses that are not only a good fit, but also more likely to be available when a student actually needs them.
