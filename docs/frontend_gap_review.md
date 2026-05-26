# HuskyAdvisor Frontend Gap Review

## Purpose

This document records what the current website already does and what still needs to change before the frontend truly reflects the HuskyAdvisor project story.

## What Is Working

- the website launches locally
- the landing page clearly says HuskyAdvisor
- the site mentions UWB and Husky advising
- the visual layout is cleaner and more intentional than a placeholder blank page
- the landing page communicates the high-level purpose of the project

## What Still Feels Incomplete

### 1. Frontend Is Still Mostly A Shell

The landing page looks real, but it is still more of a project shell than a working advising product. It introduces the idea well, but it does not yet prove the full HuskyAdvisor workflow.

### 2. Real Backend-Driven Results Are Not Yet Visible

The main value of HuskyAdvisor is the recommendation engine. Right now, the website needs to show:
- real course recommendations
- real company alignment
- real internship-prep guidance
- real roadmap output

These should come from the backend rather than static placeholder content.

### 3. Persona-Based Testing Is Not Yet Reflected In The UI

The project already has sample personas and expected outputs, but the current frontend does not yet visibly show that those scenarios are being used.

### 4. Project Scope Needs Stronger Signals In Results Pages

The site should clearly communicate:
- this is UWB-focused advising support
- this is not official advising approval
- this is not a live internship board

That language matters because it keeps the project honest and aligned with the actual MVP.

## Highest-Value Frontend Next Steps

1. Wire the profile form to the FastAPI endpoints
2. Replace static or placeholder result content with backend-driven outputs
3. Add company alignment and internship-prep sections to the actual user flow
4. Render evidence and cautions in a clear visual format
5. Test the UI using the sample personas

## Why This Matters

Once the frontend uses the real HuskyAdvisor logic, the project will feel much more like a complete final product and much less like separate frontend and backend prototypes.
