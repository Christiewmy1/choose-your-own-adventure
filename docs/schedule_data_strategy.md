# HuskyAdvisor Schedule Data Strategy

## Purpose

This document explains how the new official schedule datasets should be interpreted and why they matter for HuskyAdvisor.

## Current Schedule Data Layers

HuskyAdvisor now has three different schedule-related data layers:

### 1. Recent Term Summary

- `data/uwb_recent_css_catalog_summary.json`

This gives a lightweight recent-offering signal.

### 2. Spring 2026 Official Snapshot

- `data/uwb_spring_2026_schedule_snapshot.json`

This gives more detailed section-level information for one specific quarter.

### 3. Multi-Quarter 2026 Snapshot

- `data/uwb_2026_multi_quarter_schedule_snapshot.json`

This gives a broader planning view across Winter, Spring, Summer, and Autumn 2026.

### 4. Recurring Pattern Summary

- `data/recurring_course_patterns.json`

This simplifies the multi-quarter schedule into reusable planning signals.

## Why This Matters

Without schedule data, HuskyAdvisor can only say:
- this course seems relevant

With schedule data, HuskyAdvisor can begin saying:
- this course seems relevant
- it appears in multiple quarters
- it is usually offered in the evening or afternoon
- it may be easier to plan around than a rare or seasonal course

## Best Future Uses

These files support future features like:
- preferring courses with recurring availability
- helping students plan multiple quarters ahead
- supporting simple schedule preference filters
- making roadmap suggestions more realistic

## What The Team Should Avoid

The project should not claim:
- live registration accuracy
- guaranteed future availability
- perfect current enrollment status

These are planning datasets, not live registrar data feeds.

## Recommended Next Step

Use `recurring_course_patterns.json` as a lightweight signal in recommendation scoring before trying to build a more complex real-time scheduling system.
