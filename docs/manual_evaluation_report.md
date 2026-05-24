# HuskyAdvisor Manual Evaluation Report

## Purpose

This document records a first-pass manual evaluation of the current HuskyAdvisor CLI prototype. The goal is to show whether the system produces relevant, grounded, actionable, and honest recommendations.

## Evaluation Criteria

- **Relevant:** Does the answer match the student’s goal?
- **Grounded:** Does it use UWB-style course and company information?
- **Actionable:** Does it give next steps instead of vague commentary?
- **Honest:** Does it avoid pretending to know live internships or official advising decisions?

## Evaluation Samples

### 1. Profile Demo

**Command:**

```bash
PYTHONPATH=src python3 -m huskyadvisor.main --mode profile-demo
```

**Observed result:**  
The system recommended:

- CSS 430 Operating Systems
- CSS 427 Embedded Systems
- EE 450 Embedded Systems Design

**Assessment:**

- Relevant: strong
- Grounded: strong
- Actionable: strong
- Honest: medium-high

**Reasoning:**  
The output aligns well with a Boeing-oriented CSSE profile and uses both recent-term and company-mapping signals.

### 2. Company Demo

**Command:**

```bash
PYTHONPATH=src python3 -m huskyadvisor.main --mode company-demo
```

**Observed result:**  
The system recommended:

- Boeing
- Amazon Bellevue
- Microsoft Redmond

**Assessment:**

- Relevant: strong
- Grounded: medium-high
- Actionable: medium
- Honest: strong

**Reasoning:**  
This output is useful because it connects coursework to regional employers without pretending it is a live job feed.

### 3. Internship Demo

**Command:**

```bash
PYTHONPATH=src python3 -m huskyadvisor.main --mode internship-demo
```

**Observed result:**  
The system generated:

- recommended courses
- project suggestions
- target companies
- suggested skills

**Assessment:**

- Relevant: strong
- Grounded: medium
- Actionable: strong
- Honest: strong

**Reasoning:**  
This mode gives good preparation guidance, but it is based on manually designed playbooks rather than live internship listings.

## Overall MVP Evaluation

### Current Strengths

- The project gives more than generic AI advice
- Recommendations are tied to UWB-style structured data
- Outputs are practical enough to be demoed
- The project is fairly honest about its limits

### Current Weaknesses

- Some tags and mappings are still manually inferred
- Applied Computing and EE coverage can still grow
- The current experience is CLI-based rather than a polished website

## Next Evaluation Tasks

1. Run all 10 prompts in `docs/evaluation_question_bank.md`
2. Record pass/fail notes for each
3. Compare outputs before and after future dataset updates
4. Turn the strongest outputs into screenshots for the project website
