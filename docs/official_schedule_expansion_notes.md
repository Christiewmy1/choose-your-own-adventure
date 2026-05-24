# HuskyAdvisor Official Schedule Expansion Notes

## Purpose

This document explains the new official Spring 2026 schedule snapshot that was added to HuskyAdvisor.

## What Was Added

A new dataset was added:

- `data/uwb_spring_2026_schedule_snapshot.json`

It summarizes selected Spring 2026 course offerings from the public UW Bothell Time Schedule pages, especially for:

- CSS 300-level core courses
- CSS 400-level electives
- Applied Computing capstone
- CSSE capstone
- one Bothell engineering course relevant to technical planning

## Why This Helps

Before this addition, HuskyAdvisor mostly knew:
- what a course is
- what career tags it has
- whether it was recently offered

Now it can also know:
- whether a course was officially offered in Spring 2026
- which sections existed
- what times they met
- whether the class was open or closed when the public page was published
- whether the section was hybrid, lab-based, or project-based

## Best Project Uses

This data can support future HuskyAdvisor features like:
- recommending courses that are actually available this quarter
- helping students avoid night classes if they prefer daytime schedules
- warning students when a course is usually offered only in limited sections
- showing that recommendations are grounded in real UW Bothell scheduling data

## Official Sources Used

- `https://www.washington.edu/students/timeschd/pub/B/SPR2026/css.html`
- `https://www.washington.edu/students/timeschd/pub/B/SPR2026/bengr.html`

## Suggested Next Step

The next logical improvement is to connect this schedule snapshot to the recommendation engine so HuskyAdvisor can prefer courses that are both relevant **and** actually offered in the current quarter.
